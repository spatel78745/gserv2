'''
Created on Dec 14, 2015

@author: spatel78745
'''

from clisock import *

HOST = ''            # Server host
PORT = 50006         # Server port

MESSAGES = [
    'This is a message',
    'And one more message',
    'And this is goodbye'
]

class Ditch(Exception): pass

def banner(txt, size=3): print('=' * size, txt, '=' * size)

def pf(res, ret, testSummary):
    print('test="%s", res=%s, ret=%s'
          % (testSummary,  
             'pass' if res else 'fail', 
             ret))
    return res
    
"""
Connects to a server

Params:
- host: hostname
- port: port

Post:
- If successful, returns (True, socket connection)
- Otherwise, returns (False, error)

The second element of the tuple is a printable object
"""
def connectToServer(host, port):
    c = ClientSocket(host, port)
    try:
        c.connect()
    except OSError as ose:
        return False, ose
    else:
        return True, c
    
def readline(conn, expected, keepEndl):
    try:
        line = conn.readline(keepEndl)
    except OSError as ose:
        return False,  ose
    else:
        def strip(line): return line[:-1] if line.endswith('\n') else line
        def tr(line): 
            return strip(line) + '<endl>' if line.endswith('\n') else line
        
        got = tr(line)
        expected = strip(expected) + '<endl>' if keepEndl else expected
        
        res = got == expected
        ret = 'Got (%s), expected (%s)' % (got, expected)
        
        return res, ret
        
def testConnectNoServer():
    testSummary = 'connect() to an invalid server'
    
    res, ret = connectToServer(HOST, PORT)
    
    pf(not res, ret, testSummary)
    
    if res: ret.close()

def testConnectToServer():
# Setup
    testSummary = 'connect() to valid server'
    input('Start a server on [:%d]. Press <Enter> when done\n' % PORT)
    
# Test and report
    res, ret = connectToServer(HOST, PORT)
    
    pf(res, ret, testSummary)

# Teardown
    if res: ret.close()

def testReadChar():
# Setup
    testSummary = 'read() a character from the socket'
    
    input('Start a server on [:%d]. Press <Enter> when done\n' % PORT)
    res, ret = connectToServer(HOST, PORT)
    if not res: 
        pf(res, ret, testSummary)
        return
    else: conn = ret
     
# Test and report
    input('Send a Z from the server. Press <Enter> when done')
    try:
        c = conn.read()
    except OSError as ose:
        res = False
        ret = ose
    else:
        res = c == 'Z'
        ret = 'Expected %c, received %c' % ('Z', c)
        
    pf(res, ret, testSummary)

# Teardown
    conn.close()    
        
def testReadCharServerDies():
# Setup
    testSummary = 'Server dies while client is blocked in read()'
    
    input('Start a server on [:%d]. Press <Enter> when done\n' % PORT)
    res, ret = connectToServer(HOST, PORT)
    if not res: 
        pf(res, ret, testSummary)
        return
    else: conn = ret

# Test and report
    print('Wait 5 seconds, then terminate the server')
    try:
        conn.read()
    except RemoteSocketClosedError as rsce:
        res = True
        ret = 'read() threw RemoteSocketClosedError: %s' % rsce
    except OSError as ose:
        res = False
        ret ="read() threw %s, should've thrown RemoteSocketClosed" % ose
    else:
        res = False
        ret ="read() succeeded, should've thrown RemoteSocketClosed"
        
    pf(res, ret, testSummary)
    
# Teardown
    conn.close()
    
def testReadline():
# Setup
    testSummary = 'Test readline()'
    
# Test and report
    input('Start a server on [:%d]. Press <Enter> when done\n' % PORT)
    res, conn = connectToServer(HOST, PORT)
    if not pf(res, conn, testSummary): return
       
    def askForLines(lines, keepEndl):
        for expected in lines:
            print("Type '%s'" % expected.rstrip(), "and press enter")
            res, ret = readline(conn, expected, keepEndl)
            if not pf(res, ret, testSummary): raise Ditch
            
    try:    
        lines = ['abc', '123', 'def']
        askForLines(lines, False)
        
        lines = [l + '\n' for l in lines]
        askForLines(lines, True)
    finally:
        conn.close()
        
def testWriteline():
# Setup
    testSummary = 'Test write'
    DELAY = 5
    
# Test and report
    input('Start a server on [:%d]. Press <Enter> when done\n' % PORT)
    res, conn = connectToServer(HOST, PORT)
    if not pf(res, conn, testSummary): return

    deepThoughts = ['All composite phenomena are impermanent',
                    'All contaminated things and events are unsatisfactory',
                    'All phenomena are empty and self-less']
    try:
        for dt in deepThoughts:
            conn.writeline(dt)
            print(dt)
            time.sleep(DELAY)
    except OSError as ose:
        ret, res = False, ose
    else:
        inp = input('Do you see the above strings on the server side (y/n)? ')
        res = inp.lower().startswith('y')
        ret = 'User saw all strings written to the socket'
    finally:    
        pf(res, ret, testSummary)
        conn.close()
    

def testSuite():    
#     testConnectNoServer()
#     testConnectToServer()
#     testReadChar()
#     testReadCharServerDies()
#     testReadline()
    testWriteline()
        
if __name__ == '__main__':
    testSuite()
