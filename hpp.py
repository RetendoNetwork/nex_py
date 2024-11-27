import socket
import hmac
import hashlib
from threading import Event
from binascii import unhexlify
import ssl
import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Callable, List, Optional

from nex.nex_types.pid import PID
from nex.rmc import RMC
from nex.connection_interface import ConnectionInterface
from nex_logger.logger import Logger
from nex.library_version import LibraryVersions
from nex.byte_stream import ByteStreamSettings
from nex.service_protocol import ServiceProtocol
from nex.packet_interface import PacketInterface
from nex.account import Account
from nex.kerberos import derive_kerberos_key


class HPPClient:
    def __init__(self, address: socket.AddressFamily, endpoint: Optional['HPPServer'] = None):
        self._address = address
        self._endpoint = endpoint
        self._pid = PID()

    def endpoint(self) -> 'HPPServer':
        return self._endpoint

    def address(self) -> Optional[str]:
        return self._address

    def pid(self) -> PID:
        return self._pid

    def set_pid(self, pid: PID):
        self._pid = pid

    @classmethod
    def new_hpp_client(cls, address: socket.AddressFamily, server: 'HPPServer') -> 'HPPClient':
        return cls(address, server)
    

class HPPPacket:
    def __init__(self, sender: HPPClient, payload: Optional[bytes]):
        self._sender = sender
        self.access_key_signature = bytes
        self.password_signature = bytes
        self._payload = payload
        self.message = RMC()
        self.processed = Event()

    def sender(self) -> ConnectionInterface:
        return self._sender

    def payload(self) -> bytes:
        return self._payload

    def set_payload(self, payload: bytes) -> None:
        self._payload = payload

    def validate_access_key_signature(self, signature: str) -> Optional[Exception]:
        try:
            self.access_key_signature = unhexlify(signature)
        except Exception as e:
            return Exception(f"Failed to decode access key signature. {e}")

        try:
            calculated_signature = self.calculate_access_key_signature()
        except Exception as e:
            return Exception(f"Failed to calculate access key signature. {e}")

        if calculated_signature != self.access_key_signature:
            return Exception("Access key signature does not match")

        return None

    def calculate_access_key_signature(self) -> bytes:
        access_key = self.sender().endpoint().access_key()
        access_key_bytes = unhexlify(access_key)

        signature = self.calculate_signature(self.payload, access_key_bytes)
        return signature

    def validate_password_signature(self, signature: str) -> Optional[Exception]:
        try:
            self.password_signature = unhexlify(signature)
        except Exception as e:
            return Exception(f"Failed to decode password signature. {e}")

        try:
            calculated_signature = self.calculate_password_signature()
        except Exception as e:
            return Exception(f"Failed to calculate password signature. {e}")

        if calculated_signature != self.password_signature:
            return Exception("Password signature does not match")

        return None

    def calculate_password_signature(self) -> bytes:
        sender = self.sender()
        pid = sender.pid()
        account = sender.endpoint().account_details_by_pid(pid)
        if not account:
            raise Exception("PID does not exist")

        key = derive_kerberos_key(pid, account.password)
        signature = self.calculate_signature(self.payload, key)
        return signature

    def calculate_signature(self, buffer: bytes, key: bytes) -> bytes:
        mac = hmac.new(key, buffer, hashlib.md5)
        return mac.digest()

    def rmc_message(self) -> Optional[RMC]:
        return self.message

    def set_rmc_message(self, message: RMC):
        self.message = message

    @staticmethod
    def new_hpp_packet(client: HPPClient, payload: bytes):
        hpp_packet = HPPPacket(client, payload)
        if payload:
            rmc_message = RMC.new_rmc_request(client.endpoint())
            try:
                rmc_message.from_bytes(payload)
            except Exception as e:
                raise Exception(f"Failed to decode HPP request. {e}")
            hpp_packet.set_rmc_message(rmc_message)
        return hpp_packet, None


class HPPServer:
    def __init__(self):
        self.server = http.server()
        self.access_key = ""
        self.library_versions = LibraryVersions()
        self.data_handlers: List[Callable] = []
        self.error_event_handlers: List[Callable] = []
        self.byte_stream_settings = ByteStreamSettings()
        self.account_details_by_pid = None
        self.account_details_by_username = None
        self.use_verbose_rmc = bool
    
    def account_details_by_pid(self, pid: PID) -> Account: pass
    def account_details_by_username(self, username) -> Account: pass

    def register_service_protocol(self, protocol: ServiceProtocol):
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
        self.server = HTTPServer(('', port), lambda *args: self.handle_request(*args))
        print(f"Starting server on port {port}")
        self.server.serve_forever()

    def listen_secure(self, port: int, cert_file: str, key_file: str):
        self.server = HTTPServer(('', port), lambda *args: self.handle_request(*args))
        self.server.socket = ssl.wrap_socket(self.server.socket, certfile=cert_file, keyfile=key_file, server_side=True)
        print(f"Starting secure server on port {port}")
        self.server.serve_forever()

    def send(self, packet: PacketInterface):
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

    def set_byte_stream_settings(self, byte_stream_settings: ByteStreamSettings):
        self.byte_stream_settings = byte_stream_settings

    def use_verbose_rmc(self):
        return self.use_verbose_rmc

    def enable_verbose_rmc(self, enable: bool):
        self.use_verbose_rmc = enable