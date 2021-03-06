import socket
import util

class RemoteSocketClosedError(OSError):
    def __init__(self):
        Exception.__init__(self, 'Remote socket closed')

class BadAddressError(Exception):
    def __init__(self, address):
        Exception.__init__(self, 'Bad address: ' + address)
     
class Connection(util.Util):
    STATE_CONNECTED = 'connected'
    STATE_DISCONNECTED = 'disconnected'
    
    def __str__(self):
        return self.state
    
    def __init__(self, conn):
        self.conn = conn
        self.state = ClientSocket.STATE_DISCONNECTED
                
    """
    Immediately closes the connection
    """
    def close(self):
        try:
            self.conn.shutdown(socket.SHUT_RDWR)
            self.conn.close()
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
            c = self.conn.recv(1)
            if not c:
                """
                Don't need to close the socket here. The following raise will
                be caught, and the handler will close the socket before 
                re-raising it...caught this as a bug when I saw a double
                close. This is super-tricky stuff.
                """
                raise RemoteSocketClosedError
            
        except OSError:
            self.close()
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
        self.conn.sendall(data.encode()) # throws

    def writeline(self, data):
        self.write(data + '\n')
        
"""
Java-style client socket. You can use it to connect to a server socket, or a
ServerSocket (yet to be written) will pass one of these back when
a client socket connects to it and you can use it to pass messages
"""
class ClientSocket(Connection, util.Util):    
    """
    Returns a string description of the connection
    """
    def __str__(self):
        return '%s:%s' % (self.addr, self.conn)

    def __init__(self, host=None, port=None):
        self.addr = (host, port)
        self.conn = None
        
        self.dlog('new')
        
    """
    Connects to a server socket

    Pre:
    - host and port have values

    Post:
    - If there's an error, raises OSError
    - If successful, self.sock is connected
    """
    def connect(self):
        return Connection(socket.create_connection(self.addr))
        self.dlog('Connected')
            
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
        conn, address = self.sockobj.accept()
        self.connections.append((conn, address))
        return Connection(conn)
        
    def close(self): self.sockobj.close()
    
# In fact, I think we can ditch all the classes and just have this function?
def getConnection(address):
    parts = address.split(':')
    
    # Assumption: len will be 2 iff there is one colon
    if len(parts) != 2: raise BadAddressError(address)
    host, port = parts
    
    # This should throw if port isn't an int
    port = int(port)
    
    # Has a host: it's a client socket
    if host:
        print('Connecting to', address)
        cs = ClientSocket(host)
        return cs.connect()
    
    # No host: it's a server socket
    ss = ServerSocket(port)
    print('Waiting for connection on', address)
    c = ss.accept()
    ss.close()
    
    return c
