'''
Created on Dec 14, 2015

@author: spatel78745
'''

from clisock import *

HOST = ''     # Server host
CPORT = 50006 # Port for client-socket tests to connect to
SPORT = 50007 # Port for external server to connect to

MESSAGES = [
    'This is a message',
    'And one more message',
    'And this is goodbye'
]

class Ditch(Exception): pass

def banner(txt, size=3): print('=' * size, txt, '=' * size)

def pf(res, ret, testSummary):
    print('res=%s, ret=%s' % ('pass' if res else 'fail', ret))
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
        conn = c.connect()
    except OSError as ose:
        return False, ose
    else:
        return True, conn
    
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
# Setup
    testSummary = 'connect() to an invalid server'
    print('BEGIN', testSummary)
    
# Test and report
    res, ret = connectToServer(HOST, CPORT)
    
    pf(not res, ret, testSummary)
    
# Teardown
    if res: ret.close()

def testConnectToServer():
# Setup
    testSummary = 'connect() to valid server'
    print('BEGIN', testSummary)

    input('Start a server on [:%d]. Press <Enter> when done\n' % CPORT)
    
# Test and report
    res, ret = connectToServer(HOST, CPORT)
    
    pf(res, ret, testSummary)

# Teardown
    if res: ret.close()

def testReadChar():
# Setup
    testSummary = 'read() a character from the socket'
    print('BEGIN', testSummary)
    
    input('Start a server on [:%d]. Press <Enter> when done\n' % CPORT)
    res, ret = connectToServer(HOST, CPORT)
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
    print('BEGIN', testSummary)
    
    input('Start a server on [:%d]. Press <Enter> when done\n' % CPORT)
    res, ret = connectToServer(HOST, CPORT)
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
    print('BEGIN', testSummary)
    
# Test and report
    input('Start a server on [:%d]. Press <Enter> when done\n' % CPORT)
    res, conn = connectToServer(HOST, CPORT)
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
    print('BEGIN', testSummary)
    
    DELAY = 1
    
# Test and report
    input('Start a server on [:%d]. Press <Enter> when done\n' % CPORT)
    res, conn = connectToServer(HOST, CPORT)
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
        
def testServerSocket():
# Setup
    testSummary = 'Test server socket'
    print('BEGIN', testSummary)
    
# Test and report
    ss = ServerSocket()
    
def testSuite():    
    testConnectNoServer()
    testConnectToServer()
    testReadChar()
    testReadCharServerDies()
    testReadline()
    testWriteline()
        
if __name__ == '__main__':
    print('Running test suite')
    testSuite()
