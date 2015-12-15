import socket
import inspect
import time

class RemoteSocketClosedError(OSError):
    def __init__(self):
        Exception.__init__(self, 'Remote socket closed')
        
class Ditch(Exception): pass
        
"""
Java-style client socket. You can use it to connect to a server socket, or a
ServerSocket (yet to be written) will pass one of these back when
a client socket connects to it and you can use it to pass messages
"""
class ClientSocket:
    STATE_CONNECTED = 'connected'
    STATE_DISCONNECTED = 'disconnected'
    
    """
    Returns a string description of the connection
    """
    def __str__(self):
        return '%s:%d %s' % (self.host, self.port, self.state)

    def log(self, msg, caller = None):
        caller = inspect.stack()[1][3] if caller is None else caller
##        return '%s %s %s [%s]' % (datetime.datetime.now(), caller, msg, self)
        return '%s [%s] [%s]' % (caller, msg, self)
    
    def dlog(self, msg):
        if __debug__: print('DBG:', self.log(msg, inspect.stack()[1][3]))
        
    def __init__(self, host='', port=''):
        self.host = host
        self.port = port
        self.state = ClientSocket.STATE_DISCONNECTED
        self.dlog('New instance')

    def setSocket(self, sock):
        self.sock = sock

    """
    Connects to a server socket

    Pre:
    - host and port have values

    Post:
    - If there's an error, raises OSError
    - If successful, self.sock is connected
    """
    def connect(self):
        for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                      socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socktype, proto)
            except OSError:
                self.sock = None
                continue
            
            try:
                self.sock.connect(sa)
            except OSError:
                self.sock.close()
                self.sock = None
                continue
            break
        
        if self.sock is None:
            raise OSError(self.log('Failed to connect'))

        self.state = ClientSocket.STATE_CONNECTED
        self.dlog('Connected')

    """
    Immediately closes the connection
    """
    def close(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.state = ClientSocket.STATE_DISCONNECTED
            self.dlog('Closed')
        except OSError as ose:
            self.dlog('Benign error (%s)' % str(ose))

    """
    Reads a character from this socket

    Pre:
    - self.sock is connected

    Post:
    - If the character is read successfully, returns it as a string
    - If the remote end closes, raises OSError
    - If there is an exception, closes the socket and propagates the exception
    """
    def read(self):
        try:
            c = self.sock.recv(1)
            if not c: raise RemoteSocketClosedError
        except OSError:
            self.sock.close()
            raise
        else:
            return c.decode()

    """
    Reads a line from this socket.

    Parameters:
    - keepEndl: if True, retains the end-of-line terminator
    
    Preconditions:
    - self.sock is a connected socket

    Postconditions:
    - If the function successfully reads a line, returns that line as a string
    - If there is an exception, closes the socket and propagates the exception

    Algorithm:
       While True:
        Read a character from the socket (throws)
        If the character is '', close the socket and throw an exception
        If the character is '\n', break
        Append the character to a byte array
    """
    def readline(self, keepEndl=False):
        line = ''
        while True:
            # TODO: Is this efficient? It creates lots of garbage
            line += self.read()
            # TODO: assumes UTF-8 and single-byte characters...or something
            # Make this more internationalized...or something
            if line.endswith('\n'): break
        return line if keepEndl else line.rstrip()

    def write(self, data):
        self.sock.sendall(data.encode()) # throws

    def writeline(self, data):
        self.write(data + '\n')
        
                   
HOST = ''            # Server host
PORT = 50006         # Server port

MESSAGES = [
    'This is a message',
    'And one more message',
    'And this is goodbye'
]

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
            time.sleep(DELAY)
            print(dt)
    except OSError as ose:
        ret, res = False, ose
    else:
        inp = input('Do you see the above strings on the server side?')
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
        
testSuite()

