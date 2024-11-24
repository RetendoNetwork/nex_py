import binascii

from nex.nex_types.writable import Writable
from nex.nex_types.readable import Readable


class Buffer(bytes):
    def write_to(self, writable: Writable):
        length = len(self)
        writable.write_uint32_le(length)
        if length > 0:
            writable.write(self)

    def extract_from(self, readable: Readable):
        length, err = readable.read_uint32_le()
        if err:
            raise ValueError(f"Failed to read NEX Buffer length: {err}")
        
        value, err = readable.read(length)
        if err:
            raise ValueError(f"Failed to read NEX Buffer data: {err}")

        return Buffer(value)

    def copy(self):
        return Buffer(self)

    def equals(self, other):
        if not isinstance(other, Buffer):
            return False
        return self == other

    def copy_ref(self):
        return self.copy()

    def deref(self):
        return self

    def __str__(self):
        return binascii.hexlify(self).decode()