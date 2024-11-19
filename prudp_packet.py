import time
from Crypto.Cipher import ARC4
from typing import Optional, List

from virtual_port import VirtualPort
from prudp_server import PRUDPServer
from prudp_connection import PRUDPConnection
from rmc import RMCMessage
from timeout import Timeout
from streams import StreamIn


# Constants for packet types
DATA_PACKET = 1  # Example constant, add more as necessary

# Assuming the existence of other required classes like PRUDPServer, PRUDPConnection, VirtualPort, ByteStreamIn, etc.

class PRUDPPacket:
    def __init__(self, server: PRUDPServer, sender: PRUDPConnection, read_stream: StreamIn, version, source_virtual_port: VirtualPort, destination_virtual_port: VirtualPort, packet_type, flags, session_id, substream_id, signature, sequence_id, connection_signature, fragment_id, payload, message: RMCMessage, send_count, sent_at: time.time, timeout: Timeout):
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

    def decrypt_payload(self):
        payload = self.payload
        if self.packet_type == DATA_PACKET:
            sliding_window = self.sender.sliding_window(self.substream_id)
            payload, _ = sliding_window.stream_settings.encryption_algorithm.decrypt(payload)
        return payload

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