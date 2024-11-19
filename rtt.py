import math
import threading
import time


ALPHA = 1.0 / 8.0
BETA = 1.0 / 4.0
K = 4.0


class RTT:
    def __init__(self):
        self.lock = threading.Lock()
        self.last_rtt = 0.0
        self.average = 0.0
        self.variance = 0.0
        self.initialized = False

    def adjust(self, next_rtt: float):
        """Updates the average RTT with the new value."""
        with self.lock:
            if self.initialized:
                self.variance = (1.0 - BETA) * self.variance + BETA * abs(self.variance - next_rtt)
                self.average = (1.0 - ALPHA) * self.average + ALPHA * next_rtt
            else:
                self.last_rtt = next_rtt
                self.variance = next_rtt / 2
                self.average = next_rtt + K * self.variance
                self.initialized = True

    def get_rtt_smoothed_avg(self) -> float:
        """Returns the smoothed average of this RTT."""
        return self.average / 16

    def get_rtt_smoothed_dev(self) -> float:
        """Returns the smoothed standard deviation of this RTT."""
        return self.variance / 8

    def initialized(self) -> bool:
        """Returns a bool indicating whether this RTT has been initialized."""
        return self.initialized

    def average(self) -> float:
        """Returns the current average RTT as a duration."""
        return self.average