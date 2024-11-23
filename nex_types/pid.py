from .readable import Readable
from .writable import Writable


class PID:
    def __init__(self, pid: int):
        self.pid = pid

    def write_to(self, writable: Writable):
        if writable.pid_size() == 8:
            writable.write_uint64_le(self.pid)
        else:
            writable.write_uint32_le(int(self.pid))

    def extract_from(self, readable: Readable):
        if readable.pid_size() == 8:
            self.pid = readable.read_uint64_le()
        else:
            self.pid = readable.read_uint32_le()

    def copy(self):
        return PID(self.pid)

    def equals(self, other):
        if not isinstance(other, PID):
            return False
        return self.pid == other.pid

    def copy_ref(self):
        return self.copy()

    def deref(self):
        return self.pid

    def __str__(self):
        return self.format_to_string(0)

    def format_to_string(self, indentation_level: int):
        indentation_values = "\t" * (indentation_level + 1)
        indentation_end = "\t" * indentation_level

        return f"PID{{\n{indentation_values}pid: {self.pid}\n{indentation_end}}}"

    @staticmethod
    def new_pid(input: int):
        return PID(input)