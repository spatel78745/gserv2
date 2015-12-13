import socket
import sys
import inspect
import datetime

class RemoteSocketClosedError(OSError):
    def __init__(self):
        Exception.__init__(self, 'Remote socket closed')

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
        if __debug__: print(self.log(msg, inspect.stack()[1][3]))
        
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
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.state = ClientSocket.STATE_DISCONNECTED
        self.dlog('Closed')

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
##
##    """
##    Reads a line from this socket.
##
##    Parameters:
##    - keepEndl: if True, retains the end-of-line terminator
##    
##    Preconditions:
##    - self.sock is a connected socket
##
##    Postconditions:
##    - If the function successfully reads a line, returns that line as a string
##    - If there is an exception, closes the socket and propagates the exception
##
##    Algorithm:
##       While True:
##        Read a character from the socket (throws)
##        If the character is '', close the socket and throw an exception
##        If the character is '\n', break
##        Append the character to a byte array
##    """
##    def readline(self, keepEndl=False):
##        line = ''
##        while True:
##            line += read(self)
##            # TODO: assumes UTF-8 and single-byte characters...or something
##            # Make this more internationalized...or something
##            if line.endswith('\n'): break
##        return line if keepEndl else line.rstrip()
##
##    def write(self, data):
##        self.sock.sendall(data.encode()) # throws
##
##    def writeline(self, data):
##        write(self, data + '\n')
##
##    def close(self):
##        if not self.sock is None: self.sock.close()
    
                    
HOST = ''            # Server host
PORT = 50006         # Server port
PORT_NO_SERVER=50007

MESSAGES = [
    'This is a message',
    'And one more message',
    'And this is goodbye'
]

def banner(txt, size=3): print('=' * size, txt, '=' * size)

def pf(result, testSummary, exception=None):
    errMsg = 'None' if exception is None else exception
    resMsg = 'pass' if result else 'fail'
    print('test = "%s", result = %s, err = %s'
          % (testSummary,  resMsg, errMsg))

def testConnectNoServer():
    testSummary = 'connect() to an invalid server'
    c = ClientSocket(HOST, PORT_NO_SERVER)
    try:
        c.connect()
    except OSError as ose:
        pf(True, testSummary, ose)
    else:
        pf(False, testSummary)

def testConnectToServer():
    testSummary = 'connect() to valid server'
    input('Start a server on [:%d]. Press <Enter> when done\n' % PORT)
    c = ClientSocket(HOST, PORT)
    try:
        c.connect()
    except OSError as ose:
        pf(False, testSummary, ose)
    else:
        pf(True, testSummary)
        c.close()

def testReadChar():
    testSummary = 'read() a character from the socket'
    input('Start a server on [:%d]. Press <Enter> when done\n' % PORT)
    c = ClientSocket(HOST, PORT)
    try:
        c.connect()
    except OSError as ose:
        pf(False, testSummary, ose)
        return

    input('Send a Z from the server. Press <Enter> when done')
    err = None
    try:
        res = c.read()
    except OSError as ose:
        err = ose

    if err:
        pf(False, testSummary, err)
        c.close()
        return
    
    if res != 'Z':
        pf(False, testSummary, 'expected Z, got %s', res)

    pf(True, testSummary, 'expected Z, got %s', res)

    print('Wait 5 seconds, then terminate the server')
    try:
        res = c.read()
    except RemoteSocketClosedError as rsce:
        pf(True, testSummary, rsce)
    except OSError as ose:
        pf(False, testSummary, ose)
    else:
        pf(False, testSummary, 'No exception')
            
##def testIo():
##    c = ClientSocket(HOST, PORT);
##    try:            c.connect()
##    except OSError: pf(False)
##    else:
##        pf(True)
##        c.close()
##        
##    
##    msg = c.readline()
##    while msg != 'stop':
##        print('received ', msg)
##        c.writeline('Echo=>' + msg)
##    

if __name__ == '__main__':
##    testConnectNoServer()
##    testConnectToServer()
    testReadChar()    
