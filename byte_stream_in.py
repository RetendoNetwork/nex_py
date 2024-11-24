from anynet import streams
from crunch.buffer import Buffer

from nex.byte_stream_settings import ByteStreamSettings
from nex.library_version import LibraryVersions


class ByteStreamIn:
    def __init__(self, data, library_versions: LibraryVersions, settings: ByteStreamSettings):
        self.buffer = Buffer(data)
        self.library_versions = library_versions
        self.settings = settings

    def string_length_size(self):
        size = 2
        if self.settings:
            size = self.settings.string_length_size
        return size

    def pid_size(self):
        size = 4
        if self.settings:
            size = self.settings.pid_size
        return size

    def use_structure_header(self):
        use_structure_header = False
        if self.settings:
            use_structure_header = self.settings.use_structure_header
        return use_structure_header

    def remaining(self):
        return len(self.buffer.bytes()[self.buffer.byte_offset():])

    def read_remaining(self):
        return self.read(self.remaining())

    def read(self, length):
        if self.remaining() < length:
            raise ValueError("Read is out of bounds")
        return self.buffer.read_bytes_next(length)

    def read_uint8(self):
        if self.remaining() < 1:
            raise ValueError("Not enough data to read uint8")
        return self.buffer.read_byte_next()

    def read_uint16_le(self):
        if self.remaining() < 2:
            raise ValueError("Not enough data to read uint16")
        return self.buffer.read_u16_le_next(1)[0]

    def read_uint32_le(self):
        if self.remaining() < 4:
            raise ValueError("Not enough data to read uint32")
        return self.buffer.read_u32_le_next(1)[0]

    def read_uint64_le(self):
        if self.remaining() < 8:
            raise ValueError("Not enough data to read uint64")
        return self.buffer.read_u64_le_next(1)[0]

    def read_int8(self):
        if self.remaining() < 1:
            raise ValueError("Not enough data to read int8")
        return self.buffer.read_byte_next()

    def read_int16_le(self):
        if self.remaining() < 2:
            raise ValueError("Not enough data to read int16")
        return self.buffer.read_u16_le_next(1)[0]

    def read_int32_le(self):
        if self.remaining() < 4:
            raise ValueError("Not enough data to read int32")
        return self.buffer.read_u32_le_next(1)[0]

    def read_int64_le(self):
        if self.remaining() < 8:
            raise ValueError("Not enough data to read int64")
        return self.buffer.read_u64_le_next(1)[0]

    def read_float32_le(self):
        if self.remaining() < 4:
            raise ValueError("Not enough data to read float32")
        return self.buffer.read_f32_le_next(1)[0]

    def read_float64_le(self):
        if self.remaining() < 8:
            raise ValueError("Not enough data to read float64")
        return self.buffer.read_f64_le_next(1)[0]

    def read_bool(self):
        if self.remaining() < 1:
            raise ValueError("Not enough data to read bool")
        return self.buffer.read_byte_next() == 1