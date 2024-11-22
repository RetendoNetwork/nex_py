from counter import Counter
from stream_settings import StreamSettings


class SlidingWindow:
    def __init__(self):
        self.sequence_id_counter = Counter(0)
        self.stream_settings = StreamSettings()

    def set_cipher_key(self, key: bytes):
        self.stream_settings.encryption_algorithm.set_key(key)

    def next_outgoing_sequence_id(self) -> int:
        return self.sequence_id_counter.next()

    def decrypt(self, data: bytes) -> bytes:
        return self.stream_settings.encryption_algorithm.decrypt(data)

    def encrypt(self, data: bytes) -> bytes:
        return self.stream_settings.encryption_algorithm.encrypt(data)