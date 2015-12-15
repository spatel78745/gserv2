import socket
import time
import util

class RemoteSocketClosedError(OSError):
    def __init__(self):
        Exception.__init__(self, 'Remote socket closed')
        
"""
Java-style client socket. You can use it to connect to a server socket, or a
ServerSocket (yet to be written) will pass one of these back when
a client socket connects to it and you can use it to pass messages
"""
class ClientSocket(util.Util):
    STATE_CONNECTED = 'connected'
    STATE_DISCONNECTED = 'disconnected'
    
    """
    Returns a string description of the connection
    """
    def __str__(self):
        return '%s:%d %s' % (self.host, self.port, self.state)

    def __init__(self, host='', port=''):
        self.host = host
        self.port = port
        self.state = ClientSocket.STATE_DISCONNECTED
        self.dlog('New instance')

    def setSocket(self, accConn):
        self.sock = accConn[0]
        self.host = accConn[1][0]
        self.port = accConn[1][1]
        self.state = ClientSocket.STATE_CONNECTED

    """
    Connects to a server socket

    Pre:
    - host and port have values

    Post:
    - If there's an error, raises OSError
    - If successful, self.sock is connected
    """
    def connect(self):
        for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC,
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
                 
class ServerSocket(util.Util):
    def __init__(self, port, backlog=5):
        self.port = port
        self.sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockobj.bind(('', port))
        self.sockobj.listen(backlog)
        self.connections = []
        
    def __str__(self):
        return 'port=%d connections=%s' % (self.port, str(self.connections))
        
    def accept(self):
        accConn = self.sockobj.accept()
        cliSock = ClientSocket()
        cliSock.setSocket(accConn)
        self.connections.append(cliSock)

ss = ServerSocket(50007)
print(ss)
ss.accept()
print(ss)
