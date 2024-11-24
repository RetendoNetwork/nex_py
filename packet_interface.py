from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Fix the circular import error
if TYPE_CHECKING:
    from nex.rmc import RMC
    from nex.connection_interface import ConnectionInterface


class PacketInterface(ABC):
    @abstractmethod
    def sender(self) -> 'ConnectionInterface': pass
    
    @abstractmethod
    def payload(self): pass
    
    @abstractmethod
    def set_payload(self, payload: bytes): pass
    
    @abstractmethod
    def rmc_message(self) -> 'RMC': pass
    
    @abstractmethod
    def set_rmc_message(self, message: 'RMC'): pass