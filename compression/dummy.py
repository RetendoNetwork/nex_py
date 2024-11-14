class Dummy:
    def compress(self, payload: bytes) -> bytes:
        """
        Does nothing and returns the payload as-is.
        """
        return payload

    def decompress(self, payload: bytes) -> bytes:
        """
        Does nothing and returns the payload as-is.
        """
        return payload

    def copy(self):
        """
        Returns a new instance of the Dummy compression algorithm.
        """
        return Dummy()