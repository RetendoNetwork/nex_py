import time

class Timeout:
    def __init__(self):
        self._timeout = None
        self._ctx = None
        self._cancel = None
    
    def set_rto(self, timeout):
        """Sets the timeout field on this instance"""
        self._timeout = timeout
    
    def rto(self):
        """Gets the timeout field of this instance"""
        return self._timeout
    
    @staticmethod
    def new_timeout():
        """Creates a new Timeout instance"""
        return Timeout()