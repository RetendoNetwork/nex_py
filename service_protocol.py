from typing import Protocol

from nex.packet_interface import PacketInterface
from nex.endpoint_interface import EndpointInterface


class ServiceProtocol(Protocol):
    def handle_packet(self, packet: PacketInterface) -> None: pass

    def get_endpoint(self) -> EndpointInterface: pass

    def set_endpoint(self, endpoint: EndpointInterface) -> None: pass