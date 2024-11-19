from counter import Counter
from streams import StreamSettings
from timeout_manager import TimeoutManager

class SlidingWindow:
    def __init__(self):
        self.sequence_id_counter = Counter(0)
        self.stream_settings = StreamSettings()
        self.timeout_manager = TimeoutManager()

    def set_cipher_key(self, key: bytes):
        """Sets the reliable substreams RC4 cipher keys."""
        self.stream_settings.encryption_algorithm.set_key(key)

    def next_outgoing_sequence_id(self) -> int:
        """Returns the next outgoing sequence ID."""
        return self.sequence_id_counter.next()

    def decrypt(self, data: bytes) -> bytes:
        """Decrypts the provided data with the substreams decipher."""
        return self.stream_settings.encryption_algorithm.decrypt(data)

    def encrypt(self, data: bytes) -> bytes:
        """Encrypts the provided data with the substreams cipher."""
        return self.stream_settings.encryption_algorithm.encrypt(data)