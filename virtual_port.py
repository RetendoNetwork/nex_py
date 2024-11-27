from nex.constants.stream_type import StreamType


class VirtualPort:
    def __init__(self, value=0):
        self.value = value

    def set_stream_type(self, stream_type: StreamType):
        self.value = (self.value & 0x0F) | (stream_type.value << 4)

    def get_stream_type(self) -> StreamType:
        return StreamType(self.value >> 4)

    def set_stream_id(self, stream_id):
        self.value = (self.value & 0xF0) | (stream_id & 0x0F)

    def get_stream_id(self):
        return (self.value & 0xF)