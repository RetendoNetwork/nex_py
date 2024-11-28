import time
import os
import hashlib
import threading
import socket
import concurrent.futures
from enum import IntEnum, unique
from Crypto.Cipher import ARC4
from typing import Callable, List, Optional
from websockets.client import ClientProtocol

from nex_logger.logger import Logger
from nex.connection_interface import ConnectionInterface
from nex.stream_type import StreamType
from nex.stream_settings import StreamSettings
from nex.timeout import Timeout
from nex.byte_stream import ByteStreamIn
from nex.virtual_port import VirtualPort
from nex.rmc import RMC
from nex.account import Account
from nex.counter import Counter
from library_version import LibraryVersions
from byte_stream import ByteStreamSettings
from packet_interface import PacketInterface
from mutex import MutexMap


logger = Logger()

@unique
class PRUDPPacketTypes(IntEnum):
    SYN_PACKET = 0x0
    CONNECT_PACKET= 0x1
    DATA_PACKET = 0x2
    DISCONNECT_PACKET = 0x3
    PING_PACKET = 0x4


class SlidingWindow:
    pass


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


class PRUDPPacketInterface:
    def copy(self) -> 'PRUDPPacketInterface': pass

    def version(self) -> int: pass

    def bytes(self) -> bytes: pass

    def set_sender(self, sender: ConnectionInterface): pass

    def sender(self) -> ConnectionInterface: pass

    def flags(self, flag): pass

    def has_flag(self, flag) -> bool: pass

    def add_flag(self, flag): pass

    def set_type(self, packet_type): pass

    def type(self): pass

    def set_source_virtual_port_stream_type(self, stream_type: StreamType): pass

    def source_virtual_port_stream_type(self) -> StreamType: pass

    def set_source_virtual_port_stream_id(self, port): pass

    def source_virtual_port_stream_id(self): pass

    def set_destination_virtual_port_stream_type(self, stream_type: StreamType): pass

    def destination_virtual_port_stream_type(self) -> StreamType: pass

    def set_destination_virtual_port_stream_id(self, port): pass

    def destination_virtual_port_stream_id(self): pass

    def session_id(self): pass

    def set_session_id(self, session_id): pass

    def sub_stream_id(self): pass

    def set_sub_stream_id(self, sub_stream_id): pass

    def sequence_id(self): pass

    def set_sequence_id(self, sequence_id): pass

    def payload(self): pass

    def set_payload(self, payload): pass

    def rmc_message(self) -> RMC: pass

    def set_rmc_message(self, message: RMC): pass

    def send_count(self): pass

    def increment_send_count(self): pass

    def sent_at(self) -> time.time: pass

    def set_sent_at(self, time: time.time): pass

    def get_timeout(self) -> Timeout: pass

    def set_timeout(self, timeout: Timeout): pass

    def decode(self): pass

    def set_signature(self, signature): pass

    def calculate_connection_signature(self, addr): pass

    def calculate_signature(self, session_key, connection_signature): pass

    def decrypt_payload(self): pass

    def get_connection_signature(self): pass

    def set_connection_signature(self, connection_signature): pass

    def get_fragment_id(self): pass

    def set_fragment_id(self, fragment_id): pass

    def process_unreliable_crypto(self): pass


class PRUDPPacketV0:
    pass


class PRUDPPacketV1:
    pass


class PRUDPPacketLite:
    pass


class PRUDPPacket:
    def __init__(self, server: 'PRUDPServer', sender: 'PRUDPConnection', read_stream: ByteStreamIn, version, source_virtual_port: VirtualPort, destination_virtual_port: VirtualPort, packet_type, flags, session_id, substream_id, signature, sequence_id, connection_signature, fragment_id, payload, message: RMC, send_count, sent_at: time.time, timeout: Timeout):
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

    def set_sender(self, sender: ConnectionInterface):
        self.sender = sender

    def get_sender(self) -> ConnectionInterface:
        return self.sender

    def get_flags(self):
        return self.flags

    def has_flag(self, flag) -> bool:
        return self.flags & flag != 0

    def add_flag(self, flag):
        self.flags |= flag

    def set_type(self, packet_type):
        self.packet_type = packet_type

    def get_type(self):
        return self.packet_type

    def set_source_virtual_port_stream_type(self, stream_type: StreamType):
        self.source_virtual_port.set_stream_type(stream_type)

    def get_source_virtual_port_stream_type(self) -> StreamType:
        return self.source_virtual_port.get_stream_type()

    def set_source_virtual_port_stream_id(self, port):
        self.source_virtual_port.set_stream_id(port)

    def get_source_virtual_port_stream_id(self):
        return self.source_virtual_port.get_stream_id()

    def set_destination_virtual_port_stream_type(self, stream_type: StreamType):
        self.destination_virtual_port.set_stream_type(stream_type)

    def get_destination_virtual_port_stream_type(self) -> StreamType:
        return self.destination_virtual_port.get_stream_type()

    def set_destination_virtual_port_stream_id(self, port):
        self.destination_virtual_port.set_stream_id(port)

    def get_destination_virtual_port_stream_id(self):
        return self.destination_virtual_port.get_stream_id()

    def get_session_id(self):
        return self.session_id

    def set_session_id(self, session_id):
        self.session_id = session_id

    def get_substream_id(self):
        return self.substream_id

    def set_substream_id(self, substream_id):
        self.substream_id = substream_id

    def set_signature(self, signature: bytes):
        self.signature = signature

    def get_sequence_id(self):
        return self.sequence_id

    def set_sequence_id(self, sequence_id):
        self.sequence_id = sequence_id

    def get_payload(self) -> bytes:
        return self.payload

    def set_payload(self, payload: bytes):
        self.payload = payload

    def decrypt_payload(self) -> bytes:
        payload = self.payload

        if self.packet_type == PRUDPPacketTypes.DATA_PACKET:
            sliding_window = self.sender.sliding_window(self.get_substream_id())
            payload = sliding_window.stream_settings.encryption_algorithm.decrypt(payload)

        return payload

    def get_connection_signature(self) -> bytes:
        return self.connection_signature

    def set_connection_signature(self, connection_signature: bytes):
        self.connection_signature = connection_signature

    def get_fragment_id(self):
        return self.fragment_id

    def set_fragment_id(self, fragment_id):
        self.fragment_id = fragment_id

    def get_rmc_message(self) -> RMC:
        return self.message

    def set_rmc_message(self, message: RMC):
        self.message = message

    def get_send_count(self):
        return self.send_count

    def increment_send_count(self):
        self.send_count += 1

    def get_sent_at(self):
        return self.sent_at

    def set_sent_at(self, sent_at_time: time.time):
        self.sent_at = sent_at_time

    def get_timeout(self) -> Timeout:
        return self.timeout

    def set_timeout(self, timeout: Timeout):
        self.timeout = timeout

    def combine_keys(self, key1, key2):
        return hashlib.md5(key1 + key2).digest()
		
    def unreliable_packet_base_key(self, key):
        part1 = self.combine_keys(key, bytes.fromhex("18d8233437e4e3fe"))
        part2 = self.combine_keys(key, bytes.fromhex("233e600123cdab80"))
        return part1 + part2

    def process_unreliable_crypto(self) -> bytes:
        unique_key = bytearray(self.unreliable_packet_base_key)
        unique_key[0] = (unique_key[0] + self.sequence_id) & 0xFF
        unique_key[1] = (unique_key[1] + (self.sequence_id >> 8)) & 0xFF
        unique_key[31] = (unique_key[31] + self.session_id) & 0xFF

        cipher = ARC4.new(bytes(unique_key))
        ciphered = cipher.encrypt(bytes(self.payload))

        return ciphered


class PRUDPConnection:
    pass


class PRUDPEndPoint:
    def __init__(self, server: 'PRUDPServer', stream_id, default_stream_settings: StreamSettings, is_secure_endpoint=False):
        self.server = server
        self.stream_id = stream_id
        self.default_stream_settings = default_stream_settings
        self.connections = threading.Lock()
        self.packet_handlers = {}
        self.packet_event_handlers = {}
        self.connection_ended_event_handlers = []
        self.error_event_handlers = []
        self.connection_id_counter = Counter()
        self.server_account = Account()
        self.account_details_by_pid = None # TODO
        self.account_details_by_username = None # TODO
        self.is_secure_endpoint = is_secure_endpoint
        self.calc_retransmission_timeout_callback = None # TODO

    def on(self, name, handler):
        if name not in self.packet_event_handlers:
            self.packet_event_handlers[name] = []

        self.packet_event_handlers[name].append(handler)

    def on_data(self, handler):
        self.on("data", handler)

    def on_error(self, handler):
        self.error_event_handlers.append(handler)

    def on_disconnect(self, handler):
        self.on("disconnect", handler)
    
    def access_key(self) -> str:
        return self.server.access_key
    
    def set_access_key(self, access_key: str):
        self.server.access_key = access_key

    def send(self, packet: PacketInterface):
        self.server.send(packet)

    def library_versions(self) -> LibraryVersions:
        return self.server.library_versions

    def byte_stream_settings(self) -> ByteStreamSettings:
        return self.server.byte_stream_settings 


class SocketConnection:
    # https://github.com/aratz-lasa/websockets/blob/17b3f47549b6f752a1be07fa1ba3037cb59c7d56/src/websockets/client.py#L42
    def __init__(self, server: 'PRUDPServer', address: str, websocket_connection: Optional[ClientProtocol] = None):
        self.server = server
        self.address = address
        self.websocket_connection = websocket_connection
        self.connections = MutexMap()

    def __repr__(self):
        return f"SocketConnection(address={self.address}, connections={len(self.connections._map)})"

    @classmethod
    def new_socket_connection(server: 'PRUDPServer', address: str, websocket_connection: Optional[ClientProtocol] = None) -> 'SocketConnection':
        return SocketConnection(server, address, websocket_connection)


class UDPConnection:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (host, port)
        self.socket.bind(self.address)

    def send(self, data):
        if isinstance(data, str):
            data = data.encode()
        self.socket.sendto(data, self.address)

    def receive(self):
        data, addr = self.socket.recvfrom(1024)
        return data.decode()

    def close(self):
        self.socket.close()

    def resolve_udp_addr(self, host: str, port: int) -> tuple:
        ip_addr = socket.gethostbyname(host)
        udp_addr = (ip_addr, port)
        return udp_addr

    def listen_udp(host, port, buffer_size=1024):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        sock.bind((host, port))
        print(f"Listening on {host}:{port}")
        
        while True:
            data, addr = sock.recvfrom(buffer_size)
            print(f"message sended of {addr}: {data.decode()}")
            
            sock.sendto(f"Response of {host}:{port}".encode(), addr)


class PRUDPServer:
    def __init__(self):
        self.udp_socket = None
        self.endpoints = MutexMap[PRUDPEndPoint]
        self.access_key = ""
        self.kerberos_ticket_version = int
        self.session_key_lengh = 32
        self.fragment_size = 1300
        self.library_versions = LibraryVersions()
        self.byte_stream_settings = ByteStreamSettings()
        self.prudpv0settings = PRUDPV0Settings()
        self.prudpv1settings = PRUDPV1Settings()
        self.use_verbos_rmc = bool

    def bind_prudp_endpoint(self, endpoint: PRUDPEndPoint):
        if self.endpoints.has(endpoint.stream_id):
          logger.warning("Tried to bind already existing PRUDPEndPoint %d", endpoint.stream_id)  
        
        endpoint.server = self
        self.endpoints.set(endpoint.stream_id, endpoint)

    async def send_raw(self, socket: SocketConnection, data):
        err = None

        if isinstance(socket.address, tuple):
            if self.udp_socket:
                try:
                    self.udp_socket.sendto(data, socket.address)
                except Exception as e:
                    err = e
        elif socket.websocket_connection:
            try:
                await socket.websocket_connection.send(data)
            except Exception as e:
                err = e

        if err:
            logger.error(str(err))

    def send_packet(self, packet: PRUDPPacketInterface):
        packet_copy = packet.copy()
        connection = packet_copy.sender()

        if not packet_copy.has_flag('PacketFlagAck') and not packet_copy.has_flag('PacketFlagMultiAck'):
            if packet_copy.has_flag('PacketFlagReliable'):
                sliding_window = connection.sliding_window(packet_copy.sub_stream_id())
                packet_copy.set_sequence_id(sliding_window.next_outgoing_sequence_id())
            elif packet_copy.type() == 'DataPacket':
                packet_copy.set_sequence_id(connection.outgoing_unreliable_sequence_id_counter.next())
            elif packet_copy.type() == 'PingPacket':
                packet_copy.set_sequence_id(connection.outgoing_ping_sequence_id_counter.next())
                connection.last_sent_ping_time = time.time()
            else:
                packet_copy.set_sequence_id(0)

        packet_copy.set_session_id(connection.server_session_id)

        if packet_copy.type() == 'DataPacket' and not packet_copy.has_flag('PacketFlagAck') and not packet_copy.has_flag('PacketFlagMultiAck'):
            if packet_copy.has_flag('PacketFlagReliable'):
                sliding_window = connection.sliding_window(packet_copy.sub_stream_id())
                payload = packet_copy.payload()

                try:
                    compressed_payload = sliding_window.stream_settings.compression_algorithm.compress(payload)
                    encrypted_payload = sliding_window.stream_settings.encryption_algorithm.encrypt(compressed_payload)
                    packet_copy.set_payload(encrypted_payload)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                if packet_copy.version() != 2:
                    packet_copy.set_payload(packet_copy.process_unreliable_crypto())

        if self.prudpv1settings.legacy_connection_signature:
            packet_copy.set_signature(packet_copy.calculate_signature(connection.session_key, connection.signature))
        else:
            packet_copy.set_signature(packet_copy.calculate_signature(connection.session_key, connection.server_connection_signature))

        packet_copy.increment_send_count()
        packet_copy.set_sent_at(time.time())

        if packet_copy.has_flag('PacketFlagReliable') and packet_copy.has_flag('PacketFlagNeedsAck'):
            sliding_window = connection.sliding_window(packet_copy.substream_id())
            sliding_window.timeout_manager.schedule_packet_timeout(packet_copy)

        self.send_raw(connection.socket, packet_copy.bytes())

    def send(self, packet: PacketInterface):
        if isinstance(packet, PRUDPPacketInterface):
            data = packet.payload()
            fragments = len(data) // self.fragment_size

            fragment_id = 1
            for i in range(fragments + 1):
                if len(data) < self.fragment_size:
                    packet.set_payload(data)
                    packet.set_fragment_id(0)
                else:
                    packet.set_payload(data[:self.fragment_size])
                    packet.set_fragment_id(fragment_id)

                    data = data[self.fragment_size:]
                    fragment_id += 1

                self.send_packet(packet)

                if i < fragments:
                    time.sleep(0.016)

    def listen(self, port: int):
        self.listen_udp(port)

    def listen_datagram():
        pass

    def listen_udp(self, port: int):
        udp_address = UDPConnection.resolve_udp_addr("udp", logger.info(":%d", port))
        socket = UDPConnection.listen_udp("udp", udp_address)

        self.udp_socket = socket

        quit = threading.Event()

        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = [executor.submit(self.listen_datagram) for _ in range(os.cpu_count())]

            for future in futures:
                future.result()

        quit.set()

    def set_fragment_size(self, fragment_size: int):
        self.fragment_size = fragment_size