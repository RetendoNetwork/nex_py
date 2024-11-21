from typing import Optional


def import_module():
    global HPPServer, HPPClient, PID
    from nex.hpp_server import HPPServer
    from nex.hpp_client import HPPClient
    from nex.nex_types.pid import PID

class HPPClient:
    def __init__(self, address: Optional[str], endpoint: 'HPPServer'):
        """
        Represents a single HPP client.

        :param address: The client's IP address as a string.
        :param endpoint: The server the client is connecting to.
        :param pid: The client's NEX PID (unique identifier for each account).
        """
        self._address = address
        self._endpoint = endpoint
        self._pid = PID()

    def endpoint(self) -> 'HPPServer':
        """Returns the server the client is connecting to."""
        return self._endpoint

    def address(self) -> Optional[str]:
        """Returns the client's address."""
        return self._address

    def pid(self) -> 'PID':
        """Returns the client's NEX PID."""
        return self._pid

    def set_pid(self, pid: 'PID'):
        """Sets the client's NEX PID."""
        self._pid = pid