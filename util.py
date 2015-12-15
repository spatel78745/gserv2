'''
Created on Dec 14, 2015

@author: spatel78745
'''
import inspect

class Util:
    def log(self, msg, caller = None):
        caller = inspect.stack()[1][3] if caller is None else caller
##        return '%s %s %s [%s]' % (datetime.datetime.now(), caller, msg, self)
        return '%s [%s] [%s]' % (caller, msg, self)
    
    def dlog(self, msg):
        if __debug__: print('DBG:', self.log(msg, inspect.stack()[1][3]))
        
