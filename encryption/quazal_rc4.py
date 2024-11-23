from typing import List
from Crypto.Cipher import ARC4


class QuazalRC4:
    def __init__(self):
        self.key = b""
        self.cipher = None
        self.decipher = None
        self.ciphered_count = 0
        self.deciphered_count = 0

    def get_key(self) -> bytes:
        return self.key

    def set_key(self, key: bytes) -> None:
        self.key = key
        self.cipher = ARC4.new(key)
        self.decipher = ARC4.new(key)

    def encrypt(self, payload: bytes) -> bytes:
        self.set_key(b"CD&ML")
        ciphered = self.cipher.encrypt(payload)
        self.ciphered_count += len(payload)
        return ciphered

    def decrypt(self, payload: bytes) -> bytes:
        self.set_key(b"CD&ML")
        deciphered = self.decipher.decrypt(payload)
        self.deciphered_count += len(payload)
        return deciphered

    def copy(self) -> 'QuazalRC4':
        copied = QuazalRC4()
        copied.set_key(self.key)

        for _ in range(self.ciphered_count):
            copied.cipher.encrypt(b"\x00")

        for _ in range(self.deciphered_count):
            copied.decipher.encrypt(b"\x00")

        copied.ciphered_count = self.ciphered_count
        copied.deciphered_count = self.deciphered_count

        return copied