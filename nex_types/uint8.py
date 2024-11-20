from writable import Writable
from readable import Readable
from rv_type import RVType, RVTypePtr


class UInt8:
    def __init__(self, value=0):
        self.value = value

    def write_to(self, writable: Writable):
        writable.write_uint8(self.value)

    def extract_from(self, readable: Readable):
        value, err = readable.read_uint8()
        if err:
            raise ValueError(f"Failed to read UInt8 value: {err}")
        self.value = value

    def copy(self) -> RVType:
        return UInt8(self.value)

    def equals(self, other):
        if not isinstance(other, UInt8):
            return False
        return self.value == other.value

    def copy_ref(self) -> RVTypePtr:
        return self.copy()

    def deref(self) -> RVType:
        return self

    def __str__(self):
        return str(self.value)