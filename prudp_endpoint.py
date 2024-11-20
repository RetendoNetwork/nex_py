import threading
from collections import defaultdict
import time

from nex.constants.prudp_packet_flags import PACKET_FLAG_ACK, PACKET_FLAG_MULTI_ACK
from nex.counter import Counter
from nex.streams import StreamSettings
from nex.prudp_server import PRUDPServer
from nex.prudp_connection import PRUDPConnection
from nex.prudp_packet_interface import PRUDPPacketInterface
from nex.service_protocol import ServiceProtocol
from nex.account import Account
from nex.mutex_map import MutexMap

class PRUDPEndPoint:
    def __init__(self, server: PRUDPServer, stream_id, default_stream_settings: StreamSettings):
        self.server = server
        self.stream_id = stream_id
        self.default_stream_settings = default_stream_settings
        self.connections = MutexMap(PRUDPConnection)
        self.packet_handlers = {}
        self.packet_event_handlers = defaultdict(list)
        self.connection_ended_event_handlers = []
        self.error_event_handlers = []
        self.connection_id_counter = Counter()
        self.server_account = Account
        self.account_details_by_pid = None
        self.account_details_by_username = None
        self.is_secure_endpoint = False # Or maybe bool
        self.calc_retransmission_timeout_callback = None

    def register_service_protocol(self, protocol: ServiceProtocol):
        protocol.set_endpoint(self)
        self.on_data(protocol.handle_packet)

    def register_custom_packet_handler(self, packet_type, handler):
        self.packet_handlers[packet_type] = handler

    def on_data(self, handler):
        self.on("data", handler)

    def on_error(self, handler):
        self.error_event_handlers.append(handler)

    def on_disconnect(self, handler):
        self.on("disconnect", handler)

    def on_connection_ended(self, handler):
        self.connection_ended_event_handlers.append(handler)

    def on(self, name: str, handler):
        self.packet_event_handlers[name].append(handler)

    def emit(self, name: str, packet: PRUDPPacketInterface):
        for handler in self.packet_event_handlers[name]:
            handler(packet)

    def emit_connection_ended(self, connection: PRUDPConnection):
        for handler in self.connection_ended_event_handlers:
            handler(connection)

    def emit_error(self, error):
        for handler in self.error_event_handlers:
            handler(error)

    def delete_connection_by_id(self, cid):
        keys_to_delete = [key for key, conn in self.connections.items() if conn.id == cid]
        for key in keys_to_delete:
            del self.connections[key]

    def process_packet(self, packet: PRUDPPacketInterface, socket):
        stream_type = packet.source_virtual_port_stream_type()
        stream_id = packet.source_virtual_port_stream_id()
        discriminator = f"{socket.address}-{stream_type}-{stream_id}"
        connection = self.connections.get(discriminator)

        if connection is None:
            connection = PRUDPConnection(socket)
            connection.endpoint = self
            connection.id = self.connection_id_counter.next()
            connection.default_prudp_version = packet.version()
            connection.stream_type = stream_type
            connection.stream_id = stream_id
            connection.stream_settings = self.default_stream_settings.copy()
            self.connections[discriminator] = connection

        connection.lock()
        try:
            packet.set_sender(connection)

            if packet.has_flag(PACKET_FLAG_ACK) or packet.has_flag(PACKET_FLAG_MULTI_ACK):
                self.handle_acknowledgment(packet)
                return

            if packet.type() in self.packet_handlers:
                self.packet_handlers[packet.type()](packet)
            else:
                print(f"Unhandled packet type {packet.type()}")
        finally:
            connection.unlock()

    # TODO - Add other features later.