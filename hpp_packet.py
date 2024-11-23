import hmac
import hashlib
from typing import Optional
from threading import Event
from binascii import unhexlify

from hpp_client import HPPClient
from rmc import RMC
from nex_types.pid import PID
from connection_interface import ConnectionInterface


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

        key = self.derive_kerberos_key(pid, account.password.encode())
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
    def new_hpp_packet(client, payload: bytes):
        hpp_packet = HPPPacket(client, payload)
        if payload:
            rmc_message = RMC.new_rmc_request(client.endpoint())
            try:
                rmc_message.from_bytes(payload)
            except Exception as e:
                raise Exception(f"Failed to decode HPP request. {e}")
            hpp_packet.set_rmc_message(rmc_message)
        return hpp_packet