from anynet import streams
from crunch.buffer import Buffer

from nex.byte_stream_settings import ByteStreamSettings
from nex.library_version import LibraryVersions


class ByteStreamOut:
    def __init__(self, library_versions: LibraryVersions, settings: ByteStreamSettings):
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
        return ByteStreamOut(self.library_versions, self.settings)

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