from typing import Optional


class HPPClient:
    def __init__(self, address: Optional[str], endpoint: 'HPPServer', pid: Optional[int] = None):
        """
        Represents a single HPP client.

        :param address: The client's IP address as a string.
        :param endpoint: The server the client is connecting to.
        :param pid: The client's NEX PID (unique identifier for each account).
        """
        self._address = address
        self._endpoint = endpoint
        self._pid = pid

    def endpoint(self) -> 'HPPServer':
        """Returns the server the client is connecting to."""
        return self._endpoint

    def address(self) -> Optional[str]:
        """Returns the client's address."""
        return self._address

    def pid(self) -> Optional[int]:
        """Returns the client's NEX PID."""
        return self._pid

    def set_pid(self, pid: int):
        """Sets the client's NEX PID."""
        self._pid = pid

    @staticmethod
    def new_hpp_client(address: str, server: 'HPPServer') -> 'HPPClient':
        """
        Creates and returns a new client using the provided IP address and server.

        :param address: The client's IP address as a string.
        :param server: The server the client is connecting to.
        
        :return: A new HPPClient instance.
        """
        return HPPClient(address=address, endpoint=server)