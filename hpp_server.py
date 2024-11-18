import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from ssl import wrap_socket
import json

from hpp_packet import HPPPacket
from hpp_client import HPPClient
from library_version import LibraryVersions
from byte_stream_settings import ByteStreamSettings
from service_protocol import ServiceProtocol
from error import Error
from packet_interface import PacketInterface


class HPPServer:
    def __init__(self):
        self.server = None
        self.access_key = ""
        self.library_versions = LibraryVersions()
        self.data_handlers = []
        self.error_event_handlers = []
        self.byte_stream_settings = ByteStreamSettings()
        self.account_details_by_pid = None
        self.account_details_by_username = None
        self.use_verbose_rmc = bool

    def register_service_protocol(self, protocol: 'ServiceProtocol'):
        protocol.set_endpoint(self)
        self.on_data(protocol.handle_packet)

    def on_data(self, handler):
        self.data_handlers.append(handler)

    def emit_error(self, error: 'Error'):
        for handler in self.error_event_handlers:
            threading.Thread(target=handler, args=(error,)).start()

    def handle_request(self, req, client_addr):
        if req['method'] != "POST":
            return 400

        pid_value = req['headers'].get("pid")
        if pid_value is None:
            return 400

        token = req['headers'].get("token")
        if token is None:
            return 400

        access_key_signature = req['headers'].get("signature1")
        if access_key_signature is None:
            return 400

        password_signature = req['headers'].get("signature2")
        if password_signature is None:
            return 400

        try:
            pid = int(pid_value)
        except ValueError:
            return 400

        rmc_request_string = req['form'].get("file", "")
        rmc_request_bytes = bytes(rmc_request_string, 'utf-8')

        try:
            client = HPPClient(client_addr, self)
            client.set_pid(pid)
            hpp_packet = HPPPacket(client, rmc_request_bytes)
        except Exception as e:
            print(f"Error: {e}")
            return 400

        try:
            hpp_packet.validate_access_key_signature(access_key_signature)
        except Exception as e:
            print(f"Error: {e}")
            return 400

        try:
            hpp_packet.validate_password_signature(password_signature)
        except Exception as e:
            print(f"Error: {e}")
            error_response = self.create_error_response()
            return error_response

        for data_handler in self.data_handlers:
            threading.Thread(target=data_handler, args=(hpp_packet,)).start()

        return self.handle_packet_response(hpp_packet)

    def handle_packet_response(self, hpp_packet: HPPPacket):
        if hpp_packet.payload:
            return hpp_packet.payload
        return None

    def listen(self, port):
        server_address = ('', port)
        self.server = HTTPServer(server_address, self)
        print(f"Starting server on port {port}..")
        self.server.serve_forever()

    def listen_secure(self, port, cert_file, key_file):
        pass # TODO - Add HPP Server Listen with secure TLS server.

    def send(self, packet: PacketInterface):
        if isinstance(packet, HPPPacket):
            packet.message['IsHPP'] = True
            packet.payload = packet.message['Bytes']()

            packet.processed.put(True)

    def library_versions(self):
        return self.library_versions

    def access_key(self):
        return self.access_key

    def set_access_key(self, access_key):
        self.access_key = access_key

    def byte_stream_settings(self):
        return self.byte_stream_settings

    def set_byte_stream_settings(self, byte_stream_settings: ByteStreamSettings):
        self.byte_stream_settings = byte_stream_settings

    def use_verbose_rmc(self):
        return self.use_verbose_rmc

    def enable_verbose_rmc(self, enable):
        self.use_verbose_rmc = enable

    @staticmethod
    def create_error_response():
        return b"Error Response"