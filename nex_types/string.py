from nex.nex_types.writable import Writable
from nex.nex_types.readable import Readable


class String:
    def __init__(self, value):
        self.value = value

    def write_to(self, writable: Writable):
        value = self.value + "\x00"
        str_length = len(value)

        if writable.string_length_size() == 4:
            writable.write_uint32_le(str_length)
        else:
            writable.write_uint16_le(str_length)

        writable.write(value.encode())

    def extract_from(self, readable: Readable):
        if readable.string_length_size() == 4:
            length = readable.read_uint32_le()
        else:
            length = readable.read_uint16_le()

        if readable.remaining() < length:
            raise ValueError("NEX string length longer than data size")

        string_data = readable.read(length).decode()
        self.value = string_data.rstrip("\x00")

    def copy(self):
        return String(self.value)

    def equals(self, other):
        if not isinstance(other, String):
            return False
        return self.value == other.value

    def copy_ref(self):
        return self.copy()

    def deref(self):
        return self

    def __str__(self):
        return f'"{self.value}"'