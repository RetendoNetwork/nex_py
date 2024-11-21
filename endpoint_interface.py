from abc import ABC, abstractmethod
from typing import Optional


def import_module():
    global Error, PacketInterface, LibraryVersions, StreamSettings
    from nex.error import Error
    from nex.packet_interface import PacketInterface
    from nex.library_version import LibraryVersions
    from nex.streams import StreamSettings

class EndpointInterface(ABC):
    @abstractmethod
    def access_key(self) -> str:
        """Returns the access key of the endpoint."""
        pass

    @abstractmethod
    def set_access_key(self, access_key: str):
        """Sets the access key of the endpoint."""
        pass

    @abstractmethod
    def send(self, packet: 'PacketInterface'):
        """Sends a packet through the endpoint."""
        pass

    @abstractmethod
    def library_versions(self) -> 'LibraryVersions':
        """Returns the library versions of the endpoint."""
        pass

    @abstractmethod
    def byte_stream_settings(self) -> 'StreamSettings':
        """Returns the byte stream settings for the endpoint."""
        pass

    @abstractmethod
    def set_byte_stream_settings(self, settings: 'StreamSettings'):
        """Sets the byte stream settings for the endpoint."""
        pass

    @abstractmethod
    def use_verbose_rmc(self) -> bool:
        """Returns whether verbose RMC is enabled."""
        pass

    @abstractmethod
    def enable_verbose_rmc(self, enabled: bool):
        """Enables or disables verbose RMC."""
        pass

    @abstractmethod
    def emit_error(self, err: 'Error'):
        """Emits an error for the endpoint."""
        pass