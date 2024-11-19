from anynet import streams
from crunch import Buffer

from library_version import LibraryVersions


class StreamIn:
    def __init__(self, data, library_versions: LibraryVersions, settings: 'StreamSettings'):
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

class StreamOut:
    def __init__(self, library_versions, settings):
        self.buffer = Buffer()
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

    def copy_new(self):
        return StreamOut(self.library_versions, self.settings)

    def write(self, data):
        self.buffer.grow(len(data))
        self.buffer.write_bytes_next(data)

    def write_uint8(self, u8):
        self.buffer.grow(1)
        self.buffer.write_byte_next(u8)

    def write_uint16_le(self, u16):
        self.buffer.grow(2)
        self.buffer.write_u16_le_next([u16])

    def write_uint32_le(self, u32):
        self.buffer.grow(4)
        self.buffer.write_u32_le_next([u32])

    def write_uint64_le(self, u64):
        self.buffer.grow(8)
        self.buffer.write_u64_le_next([u64])

    def write_int8(self, s8):
        self.buffer.grow(1)
        self.buffer.write_byte_next(s8)

    def write_int16_le(self, s16):
        self.buffer.grow(2)
        self.buffer.write_u16_le_next([s16])

    def write_int32_le(self, s32):
        self.buffer.grow(4)
        self.buffer.write_u32_le_next([s32])

    def write_int64_le(self, s64):
        self.buffer.grow(8)
        self.buffer.write_u64_le_next([s64])

    def write_float32_le(self, f32):
        self.buffer.grow(4)
        self.buffer.write_f32_le_next([f32])

    def write_float64_le(self, f64):
        self.buffer.grow(8)
        self.buffer.write_f64_le_next([f64])

    def write_bool(self, b):
        b_var = 1 if b else 0
        self.buffer.grow(1)
        self.buffer.write_byte_next(b_var)
	
class StreamSettings:
    def __init__(self, string_length_size=2, pid_size=4, use_structure_header=False):
        """
        Initializes the ByteStreamSettings with default or provided values.
        
        :param string_length_size: The size for the string length (default is 2).
        :param pid_size: The size for the PID (default is 4).
        :param use_structure_header: Flag indicating if the structure header should be used (default is False).
        """
        self.string_length_size = string_length_size
        self.pid_size = pid_size
        self.use_structure_header = use_structure_header