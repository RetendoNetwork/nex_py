import ssl
import logging
import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Callable, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from nex_logger.logger import Logger
    from library_version import LibraryVersions
    from byte_stream_settings import ByteStreamSettings
    from service_protocol import ServiceProtocol
    from hpp_client import HPPClient
    from packet_interface import PacketInterface
    from hpp_packet import HPPPacket
    from rmc import RMC


class HPPServer:
    def __init__(self):
        self.server = http.server()
        self.access_key = str
        self.library_versions = LibraryVersions()
        self.data_handlers: List[Callable] = []
        self.error_event_handlers: List[Callable] = []
        self.byte_stream_settings = ByteStreamSettings()
        self.account_details_by_pid = None
        self.account_details_by_username = None
        self.use_verbose_rmc = bool

    def register_service_protocol(self, protocol: 'ServiceProtocol'):
        protocol.set_endpoint(self)
        self.on_data(protocol.handle_packet)

    def on_data(self, handler: Callable):
        self.data_handlers.append(handler)

    def emit_error(self, err):
        for handler in self.error_event_handlers:
            handler(err)

    def handle_request(self, request: BaseHTTPRequestHandler):
        if request.command != "POST":
            request.send_response(400)
            request.end_headers()
            return

        pid_value = request.headers.get("pid")
        if not pid_value:
            request.send_response(400)
            request.end_headers()
            return

        token = request.headers.get("token")
        if not token:
            request.send_response(400)
            request.end_headers()
            return

        access_key_signature = request.headers.get("signature1")
        if not access_key_signature:
            request.send_response(400)
            request.end_headers()
            return

        password_signature = request.headers.get("signature2")
        if not password_signature:
            request.send_response(400)
            request.end_headers()
            return

        try:
            pid = int(pid_value)
        except ValueError:
            request.send_response(400)
            request.end_headers()
            return

        query = parse_qs(urlparse(request.path).query)
        rmc_request_string = query.get("file", [""])[0]
        rmc_request_bytes = rmc_request_string.encode('utf-8')

        client_address = request.client_address
        client = HPPClient(client_address, self)
        client.set_pid(pid)

        try:
            hpp_packet = HPPPacket(client, rmc_request_bytes)
        except Exception as e:
            Logger.error(e)
            request.send_response(400)
            request.end_headers()
            return

        try:
            if not hpp_packet.validate_access_key_signature(access_key_signature):
                raise ValueError("Access key signature validation failed")

            if not hpp_packet.validate_password_signature(password_signature):
                raise ValueError("Password signature validation failed")
        except Exception as e:
            Logger.error(e)
            rmc_message = hpp_packet.rmc_message()
            error_response = RMC(self, "ValidationError")
            error_response.call_id = rmc_message.call_id
            error_response.is_hpp = True

            request.send_response(200)
            request.end_headers()
            request.wfile.write(error_response.bytes())
            return

        for handler in self.data_handlers:
            handler(hpp_packet)

        hpp_packet.processed.wait()

        if hpp_packet.payload:
            request.send_response(200)
            request.end_headers()
            request.wfile.write(hpp_packet.payload)

    def listen(self, port: int):
        self.server = HTTPServer(('localhost', port), lambda *args: self.handle_request(*args))
        print(f"Starting server on port {port}")
        self.server.serve_forever()

    def listen_secure(self, port: int, cert_file: str, key_file: str):
        self.server = HTTPServer(('localhost', port), lambda *args: self.handle_request(*args))
        self.server.socket = ssl.wrap_socket(self.server.socket, certfile=cert_file, keyfile=key_file, server_side=True)
        print(f"Starting secure server on port {port}")
        self.server.serve_forever()

    def send(self, packet: 'PacketInterface'):
        if isinstance(packet, HPPPacket):
            packet.message.is_hpp = True
            packet.payload = packet.message.bytes()
            packet.processed.set()

    def library_versions(self):
        return self.library_versions

    def access_key(self):
        return self.access_key

    def set_access_key(self, access_key: str):
        self.access_key = access_key

    def byte_stream_settings(self):
        return self.byte_stream_settings

    def set_byte_stream_settings(self, byte_stream_settings: 'ByteStreamSettings'):
        self.byte_stream_settings = byte_stream_settings

    def use_verbose_rmc(self):
        return self.use_verbose_rmc

    def enable_verbose_rmc(self, enable: bool):
        self.use_verbose_rmc = enable