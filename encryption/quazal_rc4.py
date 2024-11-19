from typing import List
from Crypto.Cipher import ARC4


class QuazalRC4:
    """
    QuazalRC4 encrypts data with RC4. Each iteration uses a new cipher instance. The key is always 'CD&ML'.
    """

    def __init__(self):
        """Initializes a new instance of QuazalRC4 encryption."""
        self.key = b""
        self.cipher = None
        self.decipher = None
        self.ciphered_count = 0
        self.deciphered_count = 0

    def get_key(self) -> bytes:
        """
        Returns the encryption key.

        :return: The key as bytes.
        """
        return self.key

    def set_key(self, key: bytes) -> None:
        """
        Sets the encryption key and updates the ciphers.

        :param key: The encryption key as bytes.
        :raises ValueError: If the key is invalid.
        """
        self.key = key
        self.cipher = ARC4.new(key)
        self.decipher = ARC4.new(key)

    def encrypt(self, payload: bytes) -> bytes:
        """
        Encrypts the payload with the outgoing QuazalRC4 stream.

        :param payload: The data to encrypt as bytes.
        :return: The encrypted data as bytes.
        """
        self.set_key(b"CD&ML")
        ciphered = self.cipher.encrypt(payload)
        self.ciphered_count += len(payload)
        return ciphered

    def decrypt(self, payload: bytes) -> bytes:
        """
        Decrypts the payload with the incoming QuazalRC4 stream.

        :param payload: The data to decrypt as bytes.
        :return: The decrypted data as bytes.
        """
        self.set_key(b"CD&ML")
        deciphered = self.decipher.decrypt(payload)
        self.deciphered_count += len(payload)
        return deciphered

    def copy(self) -> 'QuazalRC4':
        """
        Returns a copy of the algorithm while retaining its state.

        :return: A new instance of QuazalRC4 with the same state.
        """
        copied = QuazalRC4()
        copied.set_key(self.key)

        # Sync the cipher states by advancing the streams
        for _ in range(self.ciphered_count):
            copied.cipher.encrypt(b"\x00")

        for _ in range(self.deciphered_count):
            copied.decipher.encrypt(b"\x00")

        copied.ciphered_count = self.ciphered_count
        copied.deciphered_count = self.deciphered_count

        return copied