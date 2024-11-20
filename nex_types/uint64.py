from nex.nex_types.writable import Writable
from nex.nex_types.readable import Readable
from nex.nex_types.rv_type import RVType, RVTypePtr


class UInt64:
    def __init__(self, value=0):
        self.value = value

    def write_to(self, writable: Writable):
        writable.write_uint64_le(self.value)

    def extract_from(self, readable: Readable):
        value, err = readable.read_uint64_le()
        if err:
            raise ValueError(f"Failed to read UInt8 value: {err}")
        self.value = value

    def copy(self):
        return UInt64(self.value)

    def equals(self, other):
        if not isinstance(other, UInt64):
            return False
        return self.value == other.value

    def copy_ref(self) -> RVTypePtr:
        return self.copy()

    def deref(self) -> RVType:
        return self

    def __str__(self):
        return str(self.value)