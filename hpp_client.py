import socket
from typing import Optional

from nex_types.pid import PID
from hpp_server import HPPServer


class HPPClient:
    def __init__(self, address: socket.AddressFamily, endpoint: Optional['HPPServer'] = None):
        self._address = address
        self._endpoint = endpoint
        self._pid = PID()

    def endpoint(self) -> 'HPPServer':
        return self._endpoint

    def address(self) -> Optional[str]:
        return self._address

    def pid(self) -> PID:
        return self._pid

    def set_pid(self, pid: PID):
        self._pid = pid

    @classmethod
    def new_hpp_client(cls, address: socket.AddressFamily, server: 'HPPServer') -> 'HPPClient':
        return cls(address, server)