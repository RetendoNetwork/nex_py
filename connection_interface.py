import socket
from abc import ABC, abstractmethod
from typing import Optional

from endpoint_interface import EndpointInterface


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
    def pid(self) -> Optional[int]:
        """Returns the PID of the connection."""
        pass

    @abstractmethod
    def set_pid(self, pid: Optional[int]):
        """Sets the PID for the connection."""
        pass
