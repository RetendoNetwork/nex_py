from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rmc import RMC
    from connection_interface import ConnectionInterface


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