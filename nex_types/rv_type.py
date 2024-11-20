from abc import ABC, abstractmethod
from typing import Any

from writable import Writable
from readable import Readable


class RVType(ABC):
    @abstractmethod
    def write_to(self, writable: Writable):
        pass

    @abstractmethod
    def copy(self) -> 'RVType':
        pass

    @abstractmethod
    def copy_ref(self) -> 'RVTypePtr':
        pass

    @abstractmethod
    def equals(self, other: 'RVType') -> bool:
        pass

class RVTypePtr(RVType):
    @abstractmethod
    def extract_from(self, readable: Readable) -> None:
        pass

    @abstractmethod
    def deref(self) -> RVType:
        pass
