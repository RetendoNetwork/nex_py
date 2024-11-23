from abc import ABC, abstractmethod


class Algorithm(ABC):
    @abstractmethod
    def compress(self, payload: bytes) -> bytes: pass

    @abstractmethod
    def decompress(self, payload: bytes) -> bytes: pass

    @abstractmethod
    def copy(self): pass