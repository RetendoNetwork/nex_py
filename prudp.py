import time
import hashlib
from enum import IntEnum, unique
from Crypto.Cipher import ARC4
from typing import Callable, List, Optional

from nex.connection_interface import ConnectionInterface
from stream_type import StreamType
from nex.timeout import Timeout
from nex.byte_stream import ByteStreamIn
from nex.virtual_port import VirtualPort
from nex.rmc import RMC


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
    def compute_retransmit_timeout(packet: PRUDPPacketInterface):
        pass # TODO


class PRUDPServer:
    def __init__(self):
        self.session_key_lengh = 32
        self.kerberos_ticket_version = int

    def listen(self, port: int):
        self.listen_udp(port)

    def listen_udp(self, port: int):
        pass