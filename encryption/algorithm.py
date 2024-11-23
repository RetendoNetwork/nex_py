from abc import ABC, abstractmethod
from typing import List


class Algorithm(ABC):
    @abstractmethod
    def key(self) -> List[int]: pass

    @abstractmethod
    def set_key(self, key: List[int]) -> None: pass

    @abstractmethod
    def encrypt(self, payload: List[int]) -> List[int]: pass

    @abstractmethod
    def decrypt(self, payload: List[int]) -> List[int]: pass

    @abstractmethod
    def copy(self) -> 'Algorithm': pass