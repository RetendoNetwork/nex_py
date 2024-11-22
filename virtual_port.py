from constants.stream_type import StreamType


class VirtualPort:
    def __init__(self, value: int = 0):
        self._value = value & 0xFF

    def set_stream_type(self, stream_type: StreamType):
        self._value = (self._value & 0x0F) | (stream_type << 4)

    def stream_type(self) -> StreamType:
        return StreamType(self._value >> 4)

    def set_stream_id(self, stream_id: int):
        self._value = (self._value & 0xF0) | (stream_id & 0x0F)

    def stream_id(self) -> int:
        return self._value & 0x0F

    def __repr__(self):
        return f"VirtualPort(value={self._value})"