from readable import Readable
from writable import Writable

class PID:
    def __init__(self, value):
        self.value = value

    def write_to(self, writable: Writable):
        if writable.pid_size() == 8:
            writable.write_uint64_le(self.value)
        else:
            writable.write_uint32_le(self.value)

    def extract_from(self, readable: Readable):
        if readable.pid_size() == 8:
            self.value, err = readable.read_uint64_le()
        else:
            self.value, err = readable.read_uint32_le()

        if err:
            raise ValueError("Error reading PID")

        return None

    def copy(self):
        return PID(self.value)

    def equals(self, other):
        if not isinstance(other, PID):
            return False
        return self.value == other.value

    def copy_ref(self):
        return self.copy()

    def deref(self):
        return self

    def __str__(self):
        return self.format_to_string(0)

    def format_to_string(self, indentation_level):
        indentation_values = "\t" * (indentation_level + 1)
        indentation_end = "\t" * indentation_level

        return f"PID{{\n{indentation_values}pid: {self.value}\n{indentation_end}}}"