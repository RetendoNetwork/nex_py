from nex.nex_types.rv_type import RVType, RVTypePtr
from nex.nex_types.writable import Writable
from nex.nex_types.readable import Readable


class String:
    def __init__(self, value=""):
        self.value = value

    def write_to(self, writable: Writable):
        self.value += "\x00"
        str_length = len(self.value)

        if writable.string_length_size() == 4:
            writable.write_uint32_le(str_length)
        else:
            writable.write_uint16_le(str_length)

        writable.write(self.value.encode())

    def extract_from(self, readable: Readable):
        if readable.string_length_size() == 4:
            length = readable.read_uint32_le()
        else:
            length = readable.read_uint16_le()

        if length > readable.remaining():
            raise ValueError("NEX string length longer than data size")

        string_data = readable.read(length)
        str_value = string_data.decode().rstrip("\x00")
        self.value = str_value

    def copy(self) -> RVType:
        return String(self.value)

    def equals(self, other: RVType) -> bool:
        if not isinstance(other, String):
            return False
        return self.value == other.value

    def copy_ref(self) -> RVTypePtr:
        copied = self.copy()
        return copied

    def deref(self) -> RVType:
        return self

    def __str__(self):
        return f'"{self.value}"'

    def new_string(input_value):
        return String(input_value)