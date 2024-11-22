import time
from contextlib import contextmanager


class Timeout:
    def __init__(self):
        self._timeout = None
        self._ctx = None
        self._cancel = None
    
    def set_rto(self, timeout):
        self._timeout = timeout
    
    def rto(self):
        return self._timeout