import socket
from abc import ABC, abstractmethod

from endpoint_interface import EndpointInterface
from nex_types.pid import PID


class ConnectionInterface(ABC):
    @abstractmethod
    def endpoint(self) -> EndpointInterface:
        """Returns the endpoint associated with the connection."""
        pass

    @abstractmethod
    def address(self) -> socket.AddressFamily:
        """Returns the address of the connection."""
        pass

    @abstractmethod
    def pid(self) -> PID:
        """Returns the PID of the connection."""
        pass

    @abstractmethod
    def set_pid(self, pid: PID):
        """Sets the PID for the connection."""
        pass
