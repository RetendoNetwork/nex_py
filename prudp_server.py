import asyncio
import random
import struct
import socket
import time
import ssl
from websockets import serve
from collections import defaultdict
from threading import Lock

from nex_logger.logger import Logger
from constants.prudp_packet_flags import PACKET_FLAG_HAS_SIZE, PACKET_FLAG_RELIABLE, PACKET_FLAG_NEEDS_ACK
from library_version import LibraryVersions
from byte_stream_settings import ByteStreamSettings
from prudp_v0_settings import PRUDPV0Settings
from prudp_v1_settings import PRUDPV1Settings
from mutex_map import MutexMap


# Constants (to be adjusted based on the original Go constants)
STREAM_TYPE_RELAY = 1
STREAM_TYPE_PRUDP_LITE = 2
MAX_FRAGMENT_SIZE = 1300

class PRUDPServer:
    def __init__(self):
        self.udp_socket = None  # UDP socket (not initialized)
        self.websocket_server = None  # WebSocket server (not initialized)
        self.endpoints = MutexMap()  # MutexMap for PRUDP endpoints
        self.connections = MutexMap()  # MutexMap for socket connections
        self.supported_functions = 0  # Default value for supported functions (uint32)
        self.access_key = ""  # Default empty access key string
        self.kerberos_ticket_version = 0  # Default Kerberos ticket version
        self.session_key_length = 32  # Default session key length
        self.fragment_size = MAX_FRAGMENT_SIZE  # Default fragment size (1300 bytes)
        self.prudp_v1_connection_signature_key = bytearray(16)  # 16-byte array
        self.library_versions = LibraryVersions()  # Library versions instance
        self.byte_stream_settings = ByteStreamSettings()  # Byte stream settings instance
        self.prudp_v0_settings = PRUDPV0Settings()  # PRUDPv0 settings instance
        self.prudp_v1_settings = PRUDPV1Settings()  # PRUDPv1 settings instance
        self.use_verbose_rmc = False  # Default value for verbose RMC flag

    def bind_prudp_endpoint(self, endpoint):
        if endpoint.stream_id in self.endpoints:
            Logger.warning(f"Tried to bind already existing PRUDPEndPoint {endpoint.stream_id}")
            return
        endpoint.server = self
        self.endpoints[endpoint.stream_id] = endpoint

    def listen_udp(self, port):
        self.init_prudp_v1_connection_signature_key()
        loop = asyncio.get_event_loop()

        # Create UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(('', port))

        # Run listening loop
        asyncio.ensure_future(self.listen_datagram())
        loop.run_forever()

    def init_prudp_v1_connection_signature_key(self):
        if len(self.prudp_v1_connection_signature_key) != 16:
            self.prudp_v1_connection_signature_key = bytes([random.randint(0, 255) for _ in range(16)])

    async def listen_datagram(self):
        while True:
            data, addr = self.udp_socket.recvfrom(64000)
            if data:
                await self.handle_socket_message(data, addr)

    async def handle_socket_message(self, packet_data, address):
        # Simulated processing based on packet data (a more complete implementation would parse and process the data)
        if packet_data[0] == 0x80:
            # Handle PRUDPLite
            pass
        elif packet_data[:2] == b'\xEA\xD0':
            # Handle PRUDPv1
            pass
        else:
            # Handle PRUDPv0
            pass
        await self.process_packet(packet_data, address)

    async def process_packet(self, packet, address):
        stream_id = struct.unpack("!H", packet[:2])[0]  # Example unpacking
        if stream_id not in self.endpoints:
            Logger.warning(f"Client {address} trying to connect to unbound PRUDPEndPoint {stream_id}")
            return

        endpoint = self.endpoints[stream_id]
        # Further processing (this needs to be implemented as in your Go code)
        pass

    def send(self, packet):
        # Fragment the packet and send via UDP or WebSocket
        data = packet.payload
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
            time.sleep(0.016)  # Sleep for 16ms between fragments

    def send_packet(self, packet):
        # Send a packet (either UDP or WebSocket)
        connection = packet.sender()
        if isinstance(connection, WebSocketConnection):
            self.send_websocket_packet(connection, packet)
        else:
            self.send_udp_packet(connection, packet)

    def send_websocket_packet(self, connection, packet):
        # Assuming websocket send via WebSocketConnection
        pass

    def send_udp_packet(self, connection, packet):
        # Send UDP packet
        pass

    def set_fragment_size(self, fragment_size):
        self.fragment_size = fragment_size


class WebSocketConnection:
    def __init__(self, websocket):
        self.websocket = websocket