import time
from typing import List, Optional

from nex.connection_interface import ConnectionInterface
from nex.constants.stream_type import StreamType
from nex.timeout import Timeout
from nex.prudp_packet_interface import PRUDPPacketInterface
from nex.rmc import RMC


class PRUDPPacketInterface:
    def copy(self) -> PRUDPPacketInterface:
        pass
    
    def version(self) -> int:
        pass
    
    def bytes(self) -> List[bytearray]:
        pass
    
    def set_sender(self, sender: ConnectionInterface) -> None:
        pass
    
    def sender(self) -> ConnectionInterface:
        pass
    
    def flags(self) -> int:
        pass
    
    def has_flag(self, flag: int) -> bool:
        pass
    
    def add_flag(self, flag: int) -> None:
        pass
    
    def set_type(self, packet_type: int) -> None:
        pass
    
    def packet_type(self) -> int:
        pass
    
    def set_source_virtual_port_stream_type(self, stream_type: StreamType) -> None:
        pass
    
    def source_virtual_port_stream_type(self) -> StreamType:
        pass
    
    def set_source_virtual_port_stream_id(self, port: int) -> None:
        pass
    
    def source_virtual_port_stream_id(self) -> int:
        pass
    
    def set_destination_virtual_port_stream_type(self, stream_type: StreamType) -> None:
        pass
    
    def destination_virtual_port_stream_type(self) -> StreamType:
        pass
    
    def set_destination_virtual_port_stream_id(self, port: int) -> None:
        pass
    
    def destination_virtual_port_stream_id(self) -> int:
        pass
    
    def session_id(self) -> int:
        pass
    
    def set_session_id(self, session_id: int) -> None:
        pass
    
    def substream_id(self) -> int:
        pass
    
    def set_substream_id(self, substream_id: int) -> None:
        pass
    
    def sequence_id(self) -> int:
        pass
    
    def set_sequence_id(self, sequence_id: int) -> None:
        pass
    
    def payload(self) -> List[bytearray]:
        pass
    
    def set_payload(self, payload: List[bytearray]) -> None:
        pass
    
    def rmc_message(self) -> RMC:
        pass
    
    def set_rmc_message(self, message: RMC) -> None:
        pass
    
    def send_count(self) -> int:
        pass
    
    def increment_send_count(self) -> None:
        pass
    
    def sent_at(self) -> time.time:
        pass
    
    def set_sent_at(self, time: time.time) -> None:
        pass
    
    def get_timeout(self) -> Optional[Timeout]:
        pass
    
    def set_timeout(self, timeout: Timeout) -> None:
        pass
    
    def decode(self) -> Optional[Exception]:
        pass
    
    def set_signature(self, signature: List[bytearray]) -> None:
        pass
    
    def calculate_connection_signature(self, addr: 'net.addr') -> List[bytearray]:
        pass
    
    def calculate_signature(self, session_key: List[bytearray], connection_signature: List[bytearray]) -> List[bytearray]:
        pass
    
    def decrypt_payload(self) -> List[bytearray]:
        pass
    
    def get_connection_signature(self) -> List[bytearray]:
        pass
    
    def set_connection_signature(self, connection_signature: List[bytearray]) -> None:
        pass
    
    def get_fragment_id(self) -> int:
        pass
    
    def set_fragment_id(self, fragment_id: int) -> None:
        pass
    
    def process_unreliable_crypto(self) -> List[bytearray]:
        pass