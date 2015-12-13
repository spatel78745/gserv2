'''
Created on Nov 21, 2015

@author: spatel78745
'''
import os, time, sys
from socket import *
myHost = ''
myPort = 50008

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))
sockobj.listen()

def now():
    return time.ctime(time.time())

activeChildren = []
def reapChildren():
    while activeChildren:
        pid, stat = os.waitpid(0, os.WNOHANG)
        if not pid: break
        activeChildren.remove(pid)
        
def handleClient(connection):
    while True:
        print('Waiting for data')
        data = connection.recv(1024)
        print("Read ", data)
        if not data: break
        reply = 'Echo=> %s at %s' % (data, now())
        connection.send(reply.encode())
    connection.close()
    os._exit(0)
    
def dispatcher():
    while True:
        print('Waiting for connection.')
        connection, address = sockobj.accept()
        print('Server connected by ', address, end = ' ')
        print('at', now())
        reapChildren()
        childPid = os.fork()
        if childPid == 0:
            handleClient(connection)
        else:
            activeChildren.append(childPid)

print (__name__)
if __name__ == '__main__':
    dispatcher()
            

