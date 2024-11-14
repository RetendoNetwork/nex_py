from abc import ABC, abstractmethod


class Algorithm(ABC):
    """
    Define all the methods a compression algorithm should have.
    """

    @abstractmethod
    def compress(self, payload: bytes) -> bytes:
        """
        Compresses the given payload and returns the compressed data.
        """
        pass

    @abstractmethod
    def decompress(self, payload: bytes) -> bytes:
        """
        Decompresses the given payload and returns the decompressed data.
        """
        pass

    @abstractmethod
    def copy(self):
        """
        Returns a copy of the algorithm.
        """
        pass