from abc import ABC, abstractmethod
from typing import Any

from packet_interface import PacketInterface
from endpoint_interface import EndpointInterface


class ServiceProtocol(ABC):
    """
    ServiceProtocol represents a NEX service capable of handling PRUDP/HPP packets.
    """

    @abstractmethod
    def handle_packet(self, packet: PacketInterface) -> None:
        """
        Handle the incoming packet.
        
        :param packet: The packet to be handled.
        """
        pass

    @abstractmethod
    def endpoint(self) -> EndpointInterface:
        """
        Returns the endpoint associated with the service.
        """
        pass

    @abstractmethod
    def set_endpoint(self, endpoint: EndpointInterface) -> None:
        """
        Set the endpoint for the service.
        
        :param endpoint: The endpoint to be set.
        """
        pass