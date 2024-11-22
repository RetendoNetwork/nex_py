from abc import ABC, abstractmethod
from copy import deepcopy


class CompressionAlgorithm(ABC):
    @abstractmethod
    def compress(self, payload: bytes) -> bytes:
        pass

    @abstractmethod
    def decompress(self, payload: bytes) -> bytes:
        pass

    def copy(self) -> 'CompressionAlgorithm':
        return deepcopy(self)