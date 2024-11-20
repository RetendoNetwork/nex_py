from typing import Callable, List, Optional
import threading
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import json

from nex.hpp_packet import HPPPacket
from nex.hpp_client import HPPClient
from nex.library_version import LibraryVersions
from nex.streams import StreamSettings
from nex.service_protocol import ServiceProtocol
from nex.error import CError
from nex.packet_interface import PacketInterface
from nex.nex_types.pid import PID


class HPPServer:
    def __init__(self):
        self.server = None
        self.access_key = str
        self.library_versions = LibraryVersions()
        self.data_handlers = []
        self.error_event_handlers = []
        self.byte_stream_settings = StreamSettings()
        self.account_details_by_pid = None
        self.account_details_by_username = None
        self.use_verbose_rmc = False # Or maybe bool

    def register_service_protocol(self, protocol: ServiceProtocol):
        protocol.set_endpoint(self)
        self.on_data(protocol.handle_packet)

    def on_data(self, handler):
        self.data_handlers.append(handler)

    def emit_error(self, error):
        for handler in self.error_event_handlers:
            handler(error)

    def handle_request(self, request_handler: BaseHTTPRequestHandler):
        if request_handler.command != "POST":
            request_handler.send_response(400)
            request_handler.end_headers()
            return

        pid_value = request_handler.headers.get("pid")
        if not pid_value:
            request_handler.send_response(400)
            request_handler.end_headers()
            return

        token = request_handler.headers.get("token")
        if not token:
            request_handler.send_response(400)
            request_handler.end_headers()
            return

        access_key_signature = request_handler.headers.get("signature1")
        if not access_key_signature:
            request_handler.send_response(400)
            request_handler.end_headers()
            return

        password_signature = request_handler.headers.get("signature2")
        if not password_signature:
            request_handler.send_response(400)
            request_handler.end_headers()
            return

        try:
            pid = int(pid_value)
        except ValueError:
            request_handler.send_response(400)
            request_handler.end_headers()
            return

        rmc_request_string = request_handler.rfile.read(int(request_handler.headers.get("Content-Length"))).decode()
        tcp_addr = request_handler.client_address

        client = HPPClient(tcp_addr, self)
        client.set_pid(PID(pid))

        hpp_packet = HPPPacket(client, rmc_request_string.encode())

        if not hpp_packet.validate_access_key_signature(access_key_signature):
            request_handler.send_response(400)
            request_handler.end_headers()
            return

        if not hpp_packet.validate_password_signature(password_signature):
            request_handler.send_response(400)
            request_handler.end_headers()
            return

        for data_handler in self.data_handlers:
            data_handler(hpp_packet)

        if hpp_packet.payload:
            request_handler.send_response(200)
            request_handler.end_headers()
            request_handler.wfile.write(hpp_packet.payload)

    def listen(self, port):
        self.server = HTTPServer(("0.0.0.0", port), self.create_handler())
        print(f"Server started on port {port}")
        self.server.serve_forever()

    def listen_secure(self, port, certfile, keyfile):
        self.server = HTTPServer(("0.0.0.0", port), self.create_handler())
        self.server.socket = ssl.wrap_socket(
            self.server.socket,
            certfile=certfile,
            keyfile=keyfile,
            server_side=True,
            ssl_version=ssl.PROTOCOL_TLSv1_1,
        )
        print(f"Secure server started on port {port}")
        self.server.serve_forever()

    def send(self, packet: PacketInterface):
        if isinstance(packet, HPPPacket):
            packet.message.is_hpp = True
            packet.payload = packet.message.Bytes()
            packet.processed = True

    def create_handler(self):
        server = self

        class HPPRequestHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                server.handle_request(self)

        return HPPRequestHandler

    def get_library_versions(self) -> LibraryVersions:
        return self.library_versions

    def set_access_key(self, access_key) -> str:
        self.access_key = access_key

    def get_access_key(self):
        return self.access_key

    def get_byte_stream_settings(self):
        return self.byte_stream_settings

    def set_byte_stream_settings(self, byte_stream_settings) -> StreamSettings:
        self.byte_stream_settings = byte_stream_settings

    def use_verbose_rmc(self):
        return self.use_verbose_rmc

    def enable_verbose_rmc(self, enable: bool):
        self.use_verbose_rmc = enable