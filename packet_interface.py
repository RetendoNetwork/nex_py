from typing import List

# Define the PacketInterface-like structure as a set of functions that a packet should implement

def data() -> List[bytearray]:
    """Returns the data in the packet as a byte array"""
    pass

def sender() -> 'Client':
    """Returns the sender (Client object) of the packet"""
    pass

def set_version(version: int):
    """Sets the version of the packet"""
    pass

def version() -> int:
    """Returns the version of the packet"""
    pass

def set_source(source: int):
    """Sets the source of the packet"""
    pass

def source() -> int:
    """Returns the source of the packet"""
    pass

def set_destination(destination: int):
    """Sets the destination of the packet"""
    pass

def destination() -> int:
    """Returns the destination of the packet"""
    pass

def set_type(packet_type: int):
    """Sets the type of the packet"""
    pass

def packet_type() -> int:
    """Returns the type of the packet"""
    pass

def set_flags(bitmask: int):
    """Sets the flags of the packet"""
    pass

def flags() -> int:
    """Returns the flags of the packet"""
    pass

def has_flag(flag: int) -> bool:
    """Checks if a particular flag is set on the packet"""
    pass

def add_flag(flag: int):
    """Adds a flag to the packet"""
    pass

def clear_flag(flag: int):
    """Clears a flag from the packet"""
    pass

def set_session_id(session_id: int):
    """Sets the session ID for the packet"""
    pass

def session_id() -> int:
    """Returns the session ID of the packet"""
    pass

def set_signature(signature: List[bytearray]):
    """Sets the signature for the packet"""
    pass

def signature() -> List[bytearray]:
    """Returns the signature of the packet"""
    pass

def set_sequence_id(sequence_id: int):
    """Sets the sequence ID of the packet"""
    pass

def sequence_id() -> int:
    """Returns the sequence ID of the packet"""
    pass

def set_connection_signature(connection_signature: List[bytearray]):
    """Sets the connection signature for the packet"""
    pass

def connection_signature() -> List[bytearray]:
    """Returns the connection signature of the packet"""
    pass

def set_fragment_id(fragment_id: int):
    """Sets the fragment ID for the packet"""
    pass

def fragment_id() -> int:
    """Returns the fragment ID of the packet"""
    pass

def set_payload(payload: List[bytearray]):
    """Sets the payload of the packet"""
    pass

def payload() -> List[bytearray]:
    """Returns the payload of the packet"""
    pass

def decrypt_payload() -> Exception:
    """Decrypts the payload of the packet"""
    pass

def rmc_request() -> 'RMCRequest':
    """Returns an RMCRequest from the packet"""
    pass

def to_bytes() -> List[bytearray]:
    """Converts the packet to bytes"""
    pass