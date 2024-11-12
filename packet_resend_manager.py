import time
from threading import Lock

# Helper to simulate Counter
class Counter:
    def __init__(self, start_value=0):
        self.value = start_value
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.value += 1
            return self.value

# Helper for MutexMap
class MutexMap:
    def __init__(self):
        self.data = {}
        self.lock = Lock()

    def set(self, key, value):
        with self.lock:
            self.data[key] = value

    def get(self, key):
        with self.lock:
            return self.data.get(key)

    def delete(self, key):
        with self.lock:
            if key in self.data:
                del self.data[key]

    def clear(self, callback):
        with self.lock:
            for key, value in list(self.data.items()):
                callback(key, value)
                del self.data[key]

# Constants for Timeout handling
TIMEOUT_TIME = 5  # Example timeout duration
TIMEOUT_INCREMENT = 2  # Example timeout increment
MAX_ITERATIONS = 5  # Example max iterations

# Functions for PendingPacket
def begin_timeout_timer(pending_packet):
    def timeout_loop():
        while True:
            time.sleep(pending_packet["timeout"])

            # Check for quit signal
            if pending_packet["quit"]:
                break

            # Handle timeout logic
            client = pending_packet["packet"].get("sender")()
            server = client.get("server")()

            if pending_packet["iterations"].increment() > pending_packet["max_iterations"]:
                # Max iterations reached, assume client is dead
                server.timeout_kick(client)
                stop_timeout_timer(pending_packet)
                return
            else:
                if pending_packet["timeout_inc"] != 0:
                    pending_packet["timeout"] += pending_packet["timeout_inc"]

                # Resend the packet
                server.send_raw(client.get("address")(), pending_packet["packet"].get("bytes")())

    # Start the timer in a separate thread
    threading.Thread(target=timeout_loop, daemon=True).start()

def stop_timeout_timer(pending_packet):
    if pending_packet["ticking"]:
        pending_packet["quit"] = True
        pending_packet["ticking"] = False

# Functions for PacketResendManager
def add_packet_resend_manager(resend_manager, packet):
    pending_packet = {
        "ticking": True,
        "quit": False,
        "packet": packet,
        "iterations": Counter(0),
        "timeout": resend_manager["timeout_time"],
        "timeout_inc": resend_manager["timeout_inc"],
        "max_iterations": resend_manager["max_iterations"],
    }

    # Add to pending pool
    resend_manager["pending"].set(packet.get("sequence_id")(), pending_packet)

    # Start the timeout timer
    begin_timeout_timer(pending_packet)

def remove_packet_resend_manager(resend_manager, sequence_id):
    cached = resend_manager["pending"].get(sequence_id)
    if cached:
        stop_timeout_timer(cached)
        resend_manager["pending"].delete(sequence_id)

def clear_packet_resend_manager(resend_manager):
    resend_manager["pending"].clear(stop_timeout_timer)

# Function to create a new PacketResendManager
def new_packet_resend_manager(timeout_time, timeout_increment, max_iterations):
    return {
        "pending": MutexMap(),
        "timeout_time": timeout_time,
        "timeout_inc": timeout_increment,
        "max_iterations": max_iterations,
    }