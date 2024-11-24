import socket
from abc import ABC, abstractmethod

from nex.endpoint_interface import EndpointInterface
from nex.nex_types.pid import PID


class ConnectionInterface(ABC):
    @abstractmethod
    def endpoint(self) -> EndpointInterface: pass

    @abstractmethod
    def address(self) -> socket.AddressFamily: pass

    @abstractmethod
    def pid(self) -> PID: pass

    @abstractmethod
    def set_pid(self, pid: PID): pass