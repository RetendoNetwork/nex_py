import socket
import threading
import time
import random
import struct
from abc import ABC, abstractmethod

from library_version import LibraryVersions
from streams import StreamSettings
from prudp_v0_settings import PRUDPV0Settings
from prudp_v1_settings import PRUDPV1Settings
from prudp_packet_interface import PRUDPPacketInterface
from mutex_map import MutexMap
from packet_interface import PacketInterface
from socket_connection import SocketConnection
from prudp_endpoint import PRUDPEndPoint
from constants.prudp_packet_flags import PACKET_FLAG_ACK, PACKET_FLAG_HAS_SIZE, PACKET_FLAG_MULTI_ACK, PACKET_FLAG_NEEDS_ACK, PACKET_FLAG_RELIABLE
from constants.prudp_packet_types import PING_PACKET, SYN_PACKET, DATA_PACKET, CONNECT_PACKET, DISCONNECT_PACKET


class PRUDPServer:
    def __init__(self):
        self.udp_socket = None
        self.websocket_server = None
        self.endpoints = MutexMap(PRUDPEndPoint)
        self.connections = MutexMap(SocketConnection)
        self.supported_functions = 0
        self.access_key = str
        self.kerberos_ticket_version = 0
        self.session_key_length = 32
        self.fragment_size = 1300
        self.prudpv1_connection_signature_key = self.init_prudpv1_connection_signature_key()
        self.library_versions = LibraryVersions()
        self.byte_stream_settings = StreamSettings()
        self.prudpv0_settings = PRUDPV0Settings()
        self.prudpv1_settings = PRUDPV1Settings
        self.use_verbose_rmc = False # Or bool maybe

    def bind_prudp_endpoint(self, endpoint):
        if endpoint.stream_id in self.endpoints:
            print(f"Tried to bind already existing PRUDPEndPoint {endpoint.stream_id}")
            return
        endpoint.server = self
        self.endpoints[endpoint.stream_id] = endpoint

    def listen(self, port: int):
        self.listen_udp(port)

    def listen_udp(self, port: int):
        udp_address = ("", port)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(udp_address)

        quit_event = threading.Event()

        for _ in range(threading.cpu_count()):
            threading.Thread(target=self.listen_datagram, args=(quit_event,)).start()

        quit_event.wait()

    def listen_datagram(self, quit_event):
        while not quit_event.is_set():
            try:
                packet_data, addr = self.udp_socket.recvfrom(64000)
                self.handle_socket_message(packet_data, addr, None)
            except Exception as e:
                print(e)
                quit_event.set()

    def listen_websocket(self, port: int):
        # Implement WebSocket server functionality here
        pass

    def listen_websocket_secure(self, port: int, cert_file, key_file):
        # Implement secure WebSocket server functionality here
        pass

    def init_prudpv1_connection_signature_key(self):
        return random.randbytes(16)

    def handle_socket_message(self, packet_data, address, websocket_connection):
        packets = self.decode_packets(packet_data)
        for packet in packets:
            threading.Thread(target=self.process_packet, args=(packet, address, websocket_connection)).start()

    def decode_packets(self, packet_data):
        # Implement packet decoding logic here
        return []

    def process_packet(self, packet: PRUDPPacketInterface, address, websocket_connection):
        stream_id = packet.destination_virtual_port_stream_id()
        if stream_id not in self.endpoints:
            print(f"Client {address} trying to connect to unbound PRUDPEndPoint {stream_id}")
            return

        endpoint = self.endpoints[stream_id]
        endpoint.process_packet(packet, address, websocket_connection)

    def send(self, packet: PacketInterface):
        if isinstance(packet, PRUDPPacketInterface):
            data = packet.payload()
            fragments = len(data) // self.fragment_size

            fragment_id = 1
            for i in range(fragments + 1):
                if len(data) <= self.fragment_size:
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

    def send_packet(self, packet: PRUDPPacketInterface):
        packet_copy = packet.copy()
        connection = packet_copy.sender()

        if not packet_copy.has_flag(PACKET_FLAG_ACK) and not packet_copy.has_flag(PACKET_FLAG_MULTI_ACK):
            if packet_copy.has_flag(PACKET_FLAG_RELIABLE):
                sliding_window = connection.sliding_window(packet_copy.substream_id())
                packet_copy.set_sequence_id(sliding_window.next_outgoing_sequence_id())
            elif packet_copy.type() == DATA_PACKET:
                packet_copy.set_sequence_id(connection.outgoing_unreliable_sequence_id_counter.next())
            elif packet_copy.type() == PING_PACKET:
                packet_copy.set_sequence_id(connection.outgoing_ping_sequence_id_counter.next())
                connection.last_sent_ping_time = time.time()
            else:
                packet_copy.set_sequence_id(0)

        packet_copy.set_session_id(connection.server_session_id)

        if packet_copy.type() == DATA_PACKET and not packet_copy.has_flag(PACKET_FLAG_ACK) and not packet_copy.has_flag(PACKET_FLAG_MULTI_ACK):
            if packet_copy.has_flag(PACKET_FLAG_RELIABLE):
                sliding_window = connection.sliding_window(packet_copy.substream_id())
                payload = packet_copy.payload()

                compressed_payload = sliding_window.stream_settings.compression_algorithm.compress(payload)
                encrypted_payload = sliding_window.stream_settings.encryption_algorithm.encrypt(compressed_payload)

                packet_copy.set_payload(encrypted_payload)
            else:
                if packet_copy.version() != 2:
                    packet_copy.set_payload(packet_copy.process_unreliable_crypto())

        if self.prudpv1_settings.legacy_connection_signature:
            packet_copy.set_signature(packet_copy.calculate_signature(connection.session_key, connection.signature))
        else:
            packet_copy.set_signature(packet_copy.calculate_signature(connection.session_key, connection.server_connection_signature))

        packet_copy.increment_send_count()
        packet_copy.set_sent_at(time.time())

        if packet_copy.has_flag(PACKET_FLAG_RELIABLE) and packet_copy.has_flag(PACKET_FLAG_NEEDS_ACK):
            sliding_window = connection.sliding_window(packet_copy.substream_id())
            sliding_window.timeout_manager.schedule_packet_timeout(packet_copy)

        self.send_raw(packet_copy.sender().socket, packet_copy.bytes())

    def send_raw(self, socket_connection: SocketConnection, data):
        if isinstance(socket_connection.address, tuple):
            self.udp_socket.sendto(data, socket_connection.address)
        else:
            socket_connection.websocket_connection.send(data)

    def set_fragment_size(self, fragment_size):
        self.fragment_size = fragment_size