import math
import time
from threading import Lock


alpha = 1.0 / 8.0
beta = 1.0 / 4.0
k = 4.0

class RTT:
    def __init__(self):
        self.lock = Lock()
        self.last_rtt = 0.0
        self.average = 0.0
        self.variance = 0.0
        self.initialized = False

    def adjust(self, next_rtt: float) -> None:
        with self.lock:
            if self.initialized:
                self.variance = (1.0 - beta) * self.variance + beta * abs(self.variance - next_rtt)
                self.average = (1.0 - alpha) * self.average + alpha * next_rtt
            else:
                self.last_rtt = next_rtt
                self.variance = next_rtt / 2
                self.average = next_rtt + k * self.variance
                self.initialized = True

    def get_rtt_smoothed_avg(self) -> float:
        return self.average / 16

    def get_rtt_smoothed_dev(self) -> float:
        return self.variance / 8

    def initialized(self) -> bool:
        return self.initialized

    def average_duration(self) -> float:
        return self.average

    @staticmethod
    def new_rtt() -> 'RTT':
        return RTT()
