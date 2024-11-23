class Dummy:
    def compress(self, payload: bytes) -> bytes:
        return payload

    def decompress(self, payload: bytes) -> bytes:
        return payload

    def copy(self):
        return Dummy()