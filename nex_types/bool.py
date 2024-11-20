from nex.nex_types.readable import Readable
from nex.nex_types.writable import Writable


class Bool:
    def __init__(self, value):
        self.value = value

    def write_to(self, writable: Writable):
        writable.write_bool(self.value)

    def extract_from(self, readable: Readable):
        value = readable.read_bool()
        self.value = value

    def copy(self):
        return Bool(self.value)

    def equals(self, other):
        if not isinstance(other, Bool):
            return False
        return self.value == other.value

    def copy_ref(self):
        return self.copy()

    def deref(self):
        return self

    def __str__(self):
        return str(self.value).lower()