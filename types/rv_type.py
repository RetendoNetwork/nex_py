from abc import ABC, abstractmethod
from typing import Any

from writable import Writable
from readable import Readable


class RVType(ABC):
    
    @abstractmethod
    def write_to(self, writable: Writable) -> None:
        pass

    @abstractmethod
    def extract_from(self, readable: Readable) -> None:
        pass

    @abstractmethod
    def copy(self) -> RVType:
        pass

    @abstractmethod
    def equals(self, other: RVType) -> bool:
        pass
