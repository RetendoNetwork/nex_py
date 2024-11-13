from enum import IntEnum

from constants.stream_type import StreamType


class VirtualPort:
    def __init__(self, value: int = 0):
        """
        Represents a VirtualPort for a PRUDP connection.
        
        :param value: The initial byte value of the virtual port.
        """
        self._value = value & 0xFF  # Ensure it's a byte-sized integer (0-255)

    def set_stream_type(self, stream_type: StreamType):
        """Sets the VirtualPort stream type."""
        self._value = (self._value & 0x0F) | (stream_type << 4)

    def stream_type(self) -> StreamType:
        """Returns the VirtualPort stream type."""
        return StreamType(self._value >> 4)

    def set_stream_id(self, stream_id: int):
        """Sets the VirtualPort stream ID."""
        self._value = (self._value & 0xF0) | (stream_id & 0x0F)

    def stream_id(self) -> int:
        """Returns the VirtualPort stream ID."""
        return self._value & 0x0F

    def __repr__(self):
        return f"VirtualPort(value={self._value})"