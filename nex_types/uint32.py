from nex.nex_types.rv_type import RVType, RVTypePtr
from nex.nex_types.writable import Writable
from nex.nex_types.readable import Readable
from nex.nex_types.string import String


class UInt32:
    def __init__(self, value=0):
        self.value = value

    def write_to(self, writable: Writable):
        writable.write_uint32_le(self.value)

    def extract_from(self, readable: Readable):
        value, err = readable.read_uint32_le()
        if err:
            raise ValueError(f"Failed to read UInt32 value. {err}")
        self.value = value

    def copy(self) -> RVType:
        return UInt32(self.value)

    def equals(self, other: RVType) -> bool:
        if not isinstance(other, UInt32):
            return False
        return self.value == other.value

    def copy_ref(self) -> RVTypePtr:
        return self.copy()

    def deref(self) -> RVType:
        return self

    def __str__(self):
        return str(self.value)

    def new_uint32(input_value):
        return UInt32(input_value)