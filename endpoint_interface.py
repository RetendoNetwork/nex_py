from abc import ABC, abstractmethod

from nex.packet_interface import PacketInterface
from nex.library_version import LibraryVersions
from nex.byte_stream_settings import ByteStreamSettings
from nex.error import Error


class EndpointInterface(ABC):
    @abstractmethod
    def access_key(self) -> str: pass

    @abstractmethod
    def set_access_key(self, access_key: str): pass

    @abstractmethod
    def send(self, packet: PacketInterface): pass

    @abstractmethod
    def library_versions(self) -> LibraryVersions: pass

    @abstractmethod
    def byte_stream_settings(self) -> ByteStreamSettings: pass

    @abstractmethod
    def set_byte_stream_settings(self, settings: ByteStreamSettings): pass

    @abstractmethod
    def use_verbose_rmc(self) -> bool: pass

    @abstractmethod
    def enable_verbose_rmc(self, enabled: bool): pass

    @abstractmethod
    def emit_error(self, err: Error): pass