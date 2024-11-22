from abc import ABC, abstractmethod
from copy import deepcopy


class EncryptionAlgorithm(ABC):
    @abstractmethod
    def key(self) -> bytes:
        pass

    @abstractmethod
    def set_key(self, key: bytes) -> None:
        pass

    @abstractmethod
    def encrypt(self, payload: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, payload: bytes) -> bytes:
        pass

    def copy(self) -> 'EncryptionAlgorithm':
        return deepcopy(self)