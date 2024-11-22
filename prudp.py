from anynet import udp, tls, websocket, util, scheduler, streams, queue
from typing import List, Callable, Optional
from Crypto.Cipher import ARC4
from collections import defaultdict
import hashlib
from threading import Timer, Lock
import threading
import socket
import time
from abc import ABC, abstractmethod
from datetime import datetime

from timeout import Timeout
from streams import StreamIn
from rmc import RMC
from virtual_port import VirtualPort
from sliding_window import SlidingWindow
from constants.stream_type import StreamType
from nex_types.pid import PID
from stream_settings import StreamSettings
from mutex_map import MutexMap
from counter import Counter
from rtt import RTT


class PRUDPPacketFlags:
    PACKET_FLAG_ACK = 0x1
    PACKET_FLAG_RELIABLE = 0x2
    PACKET_FLAG_NEED_ACK = 0x4
    PACKET_FLAG_HAS_SIZE = 0x8
    PACKET_FLAG_MULTI_ACK = 0x200

class PRUDPPacketTypes:
    SYN_PACKET = 0x0
    CONNECT_PACKET = 0x1
    DATA_PACKET = 0x2
    DISCONNECT_PACKET = 0x3
    PING_PACKET = 0x4

class ConnectionState:
    STATE_NOT_CONNECTED = 0x0
    STATE_CONNECTING = 0x1
    STATE_CONNECTED = 0x2
    STATE_DISCONNECTING = 0x3
    STATE_FAUTLY = 0x4

class ConnectionInterface(ABC):
    @abstractmethod
    def endpoint(self) -> 'EndpointInterface': pass

    @abstractmethod
    def address(self) -> socket.AddressFamily: pass

    @abstractmethod
    def pid(self) -> PID: pass

    @abstractmethod
    def set_pid(self, pid: PID): pass

class EndpointInterface(ABC):
    @abstractmethod
    def access_key(self) -> str: pass

    @abstractmethod
    def set_access_key(self, access_key): pass

    @abstractmethod
    def send(self, packet: 'PacketInterface'): pass

    @abstractmethod
    def byte_stream_settings(self) -> StreamSettings: pass

    @abstractmethod
    def set_byte_stream_settings(self, settings: StreamSettings): pass

    @abstractmethod
    def use_verbose_rmc(self) -> bool: pass

    @abstractmethod
    def enable_verbose_rmc(self, enabled: bool): pass

class PacketDispatchQueue:
    def __init__(self):
        self.queue = {}
        self.next_expected_sequence_id = Counter(2) 

    def queue(self, packet: 'PRUDPPacketInterface'):
        self.queue[packet.sequence_id()] = packet

    def get_next_to_dispatch(self):
        packet = self.queue.get(self.next_expected_sequence_id.value)
        if packet:
            return packet, True
        return None, False

    def dispatched(self, packet: 'PRUDPPacketInterface'):
        self.next_expected_sequence_id.next()
        del self.queue[packet.sequence_id()]

    def purge(self):
        self.queue.clear()

class PacketInterface(ABC):
    @abstractmethod
    def sender(self) -> ConnectionInterface: pass

    @abstractmethod
    def payload(self) -> List[bytearray]: pass

    @abstractmethod
    def set_payload(self, payload: List[bytearray]) -> None: pass

    @abstractmethod
    def rmc_message(self) -> Optional[RMC]: pass

    @abstractmethod
    def set_rmc_message(self, message: RMC) -> None: pass
	
class PRUDPV0Settings:
    def __init__(self, 
                 is_quazal_mode: bool = False,
                 encrypted_connect: bool = False,
                 legacy_connection_signature: bool = False,
                 use_enhanced_checksum: bool = False,
                 connection_signature_calculator: Optional[Callable] = None,
                 signature_calculator: Optional[Callable] = None,
                 data_signature_calculator: Optional[Callable] = None,
                 checksum_calculator: Optional[Callable] = None):
        self.is_quazal_mode = is_quazal_mode
        self.encrypted_connect = encrypted_connect
        self.legacy_connection_signature = legacy_connection_signature
        self.use_enhanced_checksum = use_enhanced_checksum
        self.connection_signature_calculator = connection_signature_calculator
        self.signature_calculator = signature_calculator
        self.data_signature_calculator = data_signature_calculator
        self.checksum_calculator = checksum_calculator

class PRUDPV1Settings:
    def __init__(self, 
                 legacy_connection_signature: bool = False,
                 connection_signature_calculator: Optional[Callable] = None,
                 signature_calculator: Optional[Callable] = None):
        self.legacy_connection_signature = legacy_connection_signature
        self.connection_signature_calculator = connection_signature_calculator
        self.signature_calculator = signature_calculator

class PRUDPEndpoint:
    pass

class PRUDPConnection:
    def __init__(self, socket):
        self.socket = socket
        self.endpoint = None
        self.connection_state = ConnectionState.STATE_NOT_CONNECTED
        self.id = 0 
        self.session_id = 0
        self.server_session_id = 0
        self.session_key = []
        self.pid = PID()
        self.default_prudp_version = int
        self.stream_type = StreamType()
        self.stream_id = 0
        self.stream_settings = StreamSettings()
        self.signature = []
        self.server_connection_signature = []
        self.unreliable_packet_base_key = []
        self.rtt = RTT()
        self.sliding_windows = MutexMap(SlidingWindow)
        self.packet_dispatch_queues = MutexMap(PacketDispatchQueue)
        self.incoming_fragment_buffers = MutexMap(bytearray)
        self.outgoing_unreliable_sequence_id_counter = Counter(1)
        self.outgoing_ping_sequence_id_counter = Counter(0)
        self.last_sent_ping_time = time.time()
        self.heartbeat_timer = Timer
        self.ping_kick_timer = Timer
        self.station_urls = []
        self.mutex = Lock()

    def endpoint(self):
        return self.endpoint

    def address(self):
        return self.socket.address

    def pid(self):
        return self.pid

    def set_pid(self, pid: PID):
        self.pid = pid

    def reset(self):
        self.connection_state = ConnectionState.STATE_NOT_CONNECTED
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
        max_silence_time = self.stream_settings.max_silence_time / 1000
        self.heartbeat_timer = threading.Timer(max_silence_time, self.send_ping)
        self.heartbeat_timer.start()

    def stop_heartbeat_timers(self):
        if self.ping_kick_timer:
            self.ping_kick_timer.cancel()
        if self.heartbeat_timer:
            self.heartbeat_timer.cancel()

    def send_ping(self):
        pass

class PRUDPPacket:
    def __init__(self, server: 'PRUDPServer', sender: PRUDPConnection, read_stream: StreamIn, version, source_virtual_port: VirtualPort, destination_virtual_port: VirtualPort, packet_type, flags, session_id, substream_id, signature, sequence_id, connection_signature, fragment_id, payload, message: RMC, send_count, sent_at: time.time, timeout: Timeout):
        self.server = server
        self.sender = sender
        self.read_stream = read_stream
        self.version = version
        self.source_virtual_port = source_virtual_port
        self.destination_virtual_port = destination_virtual_port
        self.packet_type = packet_type
        self.flags = flags
        self.session_id = session_id
        self.substream_id = substream_id
        self.signature = signature
        self.sequence_id = sequence_id
        self.connection_signature = connection_signature
        self.fragment_id = fragment_id
        self.payload = payload
        self.message = message
        self.send_count = send_count
        self.sent_at = sent_at
        self.timeout = timeout

    def set_sender(self, sender):
        self.sender = sender

    def get_sender(self):
        return self.sender

    def get_flags(self):
        return self.flags

    def has_flag(self, flag):
        return self.flags & flag != 0

    def add_flag(self, flag):
        self.flags |= flag

    def set_type(self, packet_type):
        self.packet_type = packet_type

    def get_type(self):
        return self.packet_type

    def set_source_virtual_port_stream_type(self, stream_type):
        self.source_virtual_port.set_stream_type(stream_type)

    def get_source_virtual_port_stream_type(self):
        return self.source_virtual_port.stream_type()

    def set_source_virtual_port_stream_id(self, port):
        self.source_virtual_port.set_stream_id(port)

    def get_source_virtual_port_stream_id(self):
        return self.source_virtual_port.stream_id()

    def set_destination_virtual_port_stream_type(self, stream_type):
        self.destination_virtual_port.set_stream_type(stream_type)

    def get_destination_virtual_port_stream_type(self):
        return self.destination_virtual_port.stream_type()

    def set_destination_virtual_port_stream_id(self, port):
        self.destination_virtual_port.set_stream_id(port)

    def get_destination_virtual_port_stream_id(self):
        return self.destination_virtual_port.stream_id()

    def get_session_id(self):
        return self.session_id

    def set_session_id(self, session_id):
        self.session_id = session_id

    def get_substream_id(self):
        return self.substream_id

    def set_substream_id(self, substream_id):
        self.substream_id = substream_id

    def set_signature(self, signature):
        self.signature = signature

    def get_sequence_id(self):
        return self.sequence_id

    def set_sequence_id(self, sequence_id):
        self.sequence_id = sequence_id

    def get_payload(self):
        return self.payload

    def set_payload(self, payload):
        self.payload = payload

    def get_connection_signature(self):
        return self.connection_signature

    def set_connection_signature(self, connection_signature):
        self.connection_signature = connection_signature

    def get_fragment_id(self):
        return self.fragment_id

    def set_fragment_id(self, fragment_id):
        self.fragment_id = fragment_id

    def get_rmc_message(self):
        return self.message

    def set_rmc_message(self, message):
        self.message = message

    def get_send_count(self):
        return self.send_count

    def increment_send_count(self):
        self.send_count += 1

    def get_sent_at(self):
        return self.sent_at

    def set_sent_at(self, sent_at):
        self.sent_at = sent_at

    def get_timeout(self):
        return self.timeout

    def set_timeout(self, timeout):
        self.timeout = timeout

    def process_unreliable_crypto(self):
        unique_key = self.sender.unreliable_packet_base_key
        unique_key[0] = (unique_key[0] + self.sequence_id) & 0xFF
        unique_key[1] = (unique_key[1] + (self.sequence_id >> 8)) & 0xFF
        unique_key[31] = (unique_key[31] + self.session_id) & 0xFF

        cipher = ARC4.new(bytes(unique_key))
        ciphered = cipher.encrypt(self.payload)

        return ciphered

class PRUDPPacketInterface(ABC):
    @abstractmethod
    def copy(self) -> 'PRUDPPacketInterface': pass

    @abstractmethod
    def version(self) -> int: pass

    @abstractmethod
    def bytes(self) -> bytes: pass

    @abstractmethod
    def set_sender(self, sender: ConnectionInterface): pass

    @abstractmethod
    def sender(self) -> ConnectionInterface: pass

    @abstractmethod
    def flags(self) -> int: pass

    @abstractmethod
    def has_flag(self, flag: int) -> bool: pass

    @abstractmethod
    def add_flag(self, flag: int): pass

    @abstractmethod
    def set_type(self, packet_type: int): pass

    @abstractmethod
    def type(self) -> int: pass

    @abstractmethod
    def set_source_virtual_port_stream_type(self, stream_type: StreamType): pass

    @abstractmethod
    def source_virtual_port_stream_type(self) -> StreamType: pass

    @abstractmethod
    def set_source_virtual_port_stream_id(self, port: int): pass

    @abstractmethod
    def source_virtual_port_stream_id(self) -> int: pass

    @abstractmethod
    def set_destination_virtual_port_stream_type(self, stream_type: StreamType): pass

    @abstractmethod
    def destination_virtual_port_stream_type(self) -> StreamType: pass

    @abstractmethod
    def set_destination_virtual_port_stream_id(self, port: int): pass

    @abstractmethod
    def destination_virtual_port_stream_id(self) -> int: pass

    @abstractmethod
    def session_id(self) -> int: pass

    @abstractmethod
    def set_session_id(self, session_id: int): pass

    @abstractmethod
    def substream_id(self) -> int: pass

    @abstractmethod
    def set_substream_id(self, substream_id: int): pass

    @abstractmethod
    def sequence_id(self) -> int: pass

    @abstractmethod
    def set_sequence_id(self, sequence_id: int): pass

    @abstractmethod
    def payload(self) -> bytes: pass

    @abstractmethod
    def set_payload(self, payload: bytes): pass

    @abstractmethod
    def rmc_message(self) -> RMC: pass

    @abstractmethod
    def set_rmc_message(self, message: RMC): pass

    @abstractmethod
    def send_count(self) -> int: pass

    @abstractmethod
    def increment_send_count(self): pass

    @abstractmethod
    def sent_at(self) -> datetime: pass

    @abstractmethod
    def set_sent_at(self, sent_time: datetime): pass

    @abstractmethod
    def get_timeout(self) -> Timeout: pass

    @abstractmethod
    def set_timeout(self, timeout: Timeout): pass

    @abstractmethod
    def decode(self) -> Optional[Exception]: pass

    @abstractmethod
    def set_signature(self, signature: bytes): pass

    @abstractmethod
    def calculate_connection_signature(self, addr: str) -> bytes: pass

    @abstractmethod
    def calculate_signature(self, session_key: bytes, connection_signature: bytes) -> bytes: pass

    @abstractmethod
    def decrypt_payload(self) -> bytes: pass

    @abstractmethod
    def get_connection_signature(self) -> bytes: pass

    @abstractmethod
    def set_connection_signature(self, connection_signature: bytes): pass

    @abstractmethod
    def get_fragment_id(self) -> int: pass

    @abstractmethod
    def set_fragment_id(self, fragment_id: int): pass

    @abstractmethod
    def process_unreliable_crypto(self) -> bytes: pass
    
class PRUDPServer:
    pass