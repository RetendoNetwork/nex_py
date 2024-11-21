import hashlib
import time
import threading
from collections import defaultdict


def import_module():
    global PID, MutexMap, StreamType, Counter, RTT, StreamSettings, SlidingWindow, PacketDispatchQueue
    from nex.nex_types.pid import PID
    from nex.mutex_map import MutexMap
    from nex.constants.stream_type import StreamType
    from nex.counter import Counter
    from nex.rtt import RTT
    from nex.streams import StreamSettings
    from nex.sliding_window import SlidingWindow
    from nex.packet_dispatch_queue import PacketDispatchQueue

class PRUDPConnection:
    def __init__(self, socket):
        self.socket = socket  # * The connection's parent socket
        self.endpoint = None   # * The PRUDP endpoint the connection is connected to
        self.connection_state = "StateNotConnected"  # * Connection State
        self.id = 0  # * Connection ID
        self.session_id = 0  # * Random value generated at the start of the session.
        self.server_session_id = 0  # * Random value generated at the start of the session.
        self.session_key = []  # * Secret key generated at the start of the session.
        self.pid = PID()  # * PID of the user
        self.default_prudp_version = int  # * The PRUDP version
        self.stream_type = StreamType()  # * Stream type (PRUDP stream)
        self.stream_id = 0  # * Stream ID
        self.stream_settings = StreamSettings   # * Stream settings for this virtual connection
        self.signature = []  # * Connection signature for packets
        self.server_connection_signature = []  # * Signature for server-side packets
        self.unreliable_packet_base_key = []  # * Base key for encrypting unreliable DATA packets
        self.rtt = RTT()  # * Round-trip time object
        self.sliding_windows = MutexMap(SlidingWindow)  # * Sliding windows for packet streams
        self.packet_dispatch_queues = MutexMap(PacketDispatchQueue)  # * Inbound packet queues
        self.incoming_fragment_buffers = MutexMap(bytearray)  # * Incoming fragment buffers
        self.outgoing_unreliable_sequence_id_counter = Counter(1)
        self.outgoing_ping_sequence_id_counter = Counter(0)
        self.last_sent_ping_time = time.time()
        self.heartbeat_timer = None  # Heartbeat timer
        self.ping_kick_timer = None  # Ping kick timer
        self.station_urls = []  # * Station URLs
        self.mutex = threading.Lock()  # Mutex for locking connection state

    def endpoint(self):
        return self.endpoint

    def address(self):
        return self.socket.address

    def pid(self):
        return self.pid

    def set_pid(self, pid):
        self.pid = pid

    def reset(self):
        self.connection_state = "StateNotConnected"
        self.packet_dispatch_queues.clear()
        self.sliding_windows.clear()
        self.signature = []
        self.server_connection_signature = []
        self.session_key = []
        self.outgoing_unreliable_sequence_id_counter = Counter(1)
        self.outgoing_ping_sequence_id_counter = Counter(0)

    def cleanup(self):
        self.reset()
        self.stop_heartbeat_timers()
        self.socket.connections.delete(self.session_id)
        self.endpoint.emit_connection_ended(self)
        
        if len(self.socket.connections) == 0:
            self.endpoint.server.connections.delete(self.socket.address)
            # TODO: Add cleanup for socket closure event

    def initialize_sliding_windows(self, max_substream_id):
        self.sliding_windows = defaultdict(SlidingWindow)
        for i in range(max_substream_id + 1):
            self.create_sliding_window(i)

    def initialize_packet_dispatch_queues(self, max_substream_id):
        self.packet_dispatch_queues = defaultdict(PacketDispatchQueue)
        for i in range(max_substream_id + 1):
            self.create_packet_dispatch_queue(i)

    def create_sliding_window(self, substream_id):
        sliding_window = SlidingWindow()
        sliding_window.sequence_id_counter = Counter(0)  # Start at 0 for the first packet
        sliding_window.stream_settings = self.stream_settings.copy()
        self.sliding_windows[substream_id] = sliding_window
        return sliding_window

    def sliding_window(self, substream_id):
        return self.sliding_windows.get(substream_id, self.create_sliding_window(substream_id))

    def create_packet_dispatch_queue(self, substream_id):
        pdq = PacketDispatchQueue()
        self.packet_dispatch_queues[substream_id] = pdq
        return pdq

    def packet_dispatch_queue(self, substream_id):
        return self.packet_dispatch_queues.get(substream_id, self.create_packet_dispatch_queue(substream_id))

    def set_session_key(self, session_key):
        self.session_key = session_key
        for substream_id, sliding_window in self.sliding_windows.items():
            if substream_id == 0:
                sliding_window.set_cipher_key(session_key)
            else:
                modifier = len(session_key) // 2 + 1
                session_key_copy = bytearray(session_key)
                for i in range(len(session_key) // 2):
                    session_key_copy[i] = (session_key_copy[i] + (modifier - i)) & 0xFF
                sliding_window.set_cipher_key(session_key_copy)

        # Init base key for unreliable DATA packets
        part1 = hashlib.md5(session_key + bytes([0x18, 0xD8, 0x23, 0x34, 0x37, 0xE4, 0xE3, 0xFE])).digest()
        part2 = hashlib.md5(session_key + bytes([0x23, 0x3E, 0x60, 0x01, 0x23, 0xCD, 0xAB, 0x80])).digest()
        self.unreliable_packet_base_key = part1 + part2

    def reset_heartbeat(self):
        if self.ping_kick_timer:
            self.ping_kick_timer.cancel()

        if self.heartbeat_timer:
            self.heartbeat_timer = threading.Timer(self.stream_settings.max_silence_time / 1000, self.send_ping)
            self.heartbeat_timer.start()

    def lock(self):
        self.mutex.acquire()

    def unlock(self):
        self.mutex.release()

    def get_incoming_fragment_buffer(self, substream_id):
        return self.incoming_fragment_buffers.get(substream_id, bytearray())

    def set_incoming_fragment_buffer(self, substream_id, buffer):
        self.incoming_fragment_buffers[substream_id] = buffer

    def clear_outgoing_buffer(self, substream_id):
        self.incoming_fragment_buffers[substream_id] = bytearray()

    def start_heartbeat(self):
        # Heartbeat logic (simplified)
        max_silence_time = self.stream_settings.max_silence_time / 1000
        self.heartbeat_timer = threading.Timer(max_silence_time, self.send_ping)
        self.heartbeat_timer.start()

    def stop_heartbeat_timers(self):
        if self.ping_kick_timer:
            self.ping_kick_timer.cancel()
        if self.heartbeat_timer:
            self.heartbeat_timer.cancel()

    def send_ping(self):
        pass  # Pseudo-code for sending a ping packet