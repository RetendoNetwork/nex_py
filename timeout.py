import time


class Timeout:
    def __init__(self):
        self.timeout = 0
        self.ctx = None
        self.cancel = None

    def set_rto(self, timeout: float):
        self.timeout = timeout

    def rto(self) -> float:
        return self.timeout

    @classmethod
    def new_timeout(cls):
        return cls()