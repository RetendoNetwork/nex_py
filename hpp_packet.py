import hmac
import hashlib
import binascii
from typing import Optional

from hpp_client import HPPClient
from connection_interface import ConnectionInterface
from rmc_message import RMCMessage, RMCRequest


class HPPPacket:
    def __init__(self, sender: HPPClient, payload: Optional[bytes] = None):
        self.sender = sender
        self.access_key_signature = b""
        self.password_signature = b""
        self.payload = payload
        self.message = None
        self.processed = False

        if payload is not None:
            rmc_message = RMCRequest(sender.endpoint())
            err = rmc_message.from_bytes(payload)
            if err:
                raise Exception(f"Failed to decode HPP request: {err}")
            self.set_rmc_message(rmc_message)

    def sender(self) -> 'ConnectionInterface':
        return self.sender

    def payload(self) -> bytes:
        return self.payload

    def set_payload(self, payload: bytes) -> None:
        self.payload = payload

    def validate_access_key_signature(self, signature: str) -> None:
        try:
            signature_bytes = binascii.unhexlify(signature)
        except binascii.Error as err:
            raise Exception(f"Failed to decode access key signature: {err}")

        self.access_key_signature = signature_bytes

        calculated_signature, err = self.calculate_access_key_signature()
        if err:
            raise Exception(f"Failed to calculate access key signature: {err}")

        if calculated_signature != self.access_key_signature:
            raise Exception("Access key signature does not match")

    def calculate_access_key_signature(self) -> bytes:
        access_key = self.sender.endpoint().access_key()

        try:
            access_key_bytes = binascii.unhexlify(access_key)
        except binascii.Error as err:
            raise err

        signature, err = self.calculate_signature(self.payload, access_key_bytes)
        if err:
            raise err

        return signature

    def validate_password_signature(self, signature: str) -> None:
        try:
            signature_bytes = binascii.unhexlify(signature)
        except binascii.Error as err:
            raise Exception(f"Failed to decode password signature: {err}")

        self.password_signature = signature_bytes

        calculated_signature, err = self.calculate_password_signature()
        if err:
            raise Exception(f"Failed to calculate password signature: {err}")

        if calculated_signature != self.password_signature:
            raise Exception("Password signature does not match")

    def calculate_password_signature(self) -> bytes:
        sender = self.sender()
        pid = sender.pid()
        account = sender.endpoint().account_details_by_pid(pid)
        if account is None:
            raise Exception("PID does not exist")

        key = self.derive_kerberos_key(pid, account.password.encode())

        signature, err = self.calculate_signature(self.payload, key)
        if err:
            raise err

        return signature

    def calculate_signature(self, buffer: bytes, key: bytes) -> bytes:
        mac = hmac.new(key, buffer, hashlib.md5)
        return mac.digest()

    def rmc_message(self) -> Optional[RMCMessage]:
        return self.message

    def set_rmc_message(self, message: RMCMessage) -> None:
        self.message = message

    def derive_kerberos_key(self, pid: int, password: bytes) -> bytes:
        # Placeholder for the actual implementation of key derivation logic
        return password  # You can replace this with the actual key derivation logic