import struct

from readable import Readable
from writable import Writable


class PID:
    """
    PID represents a unique identifier for a user.
    Its size depends on the client version:
    - Legacy clients (WiiU/3DS) use a uint32.
    - Modern clients (Nintendo Switch) use a uint64.
    The value is always stored as a uint64.
    """

    def __init__(self, pid: int):
        self.pid = pid

    def write_to(self):
        """
        Writes the PID to the writable object.
        """
        if Writable.pid_size() == 8:
            Writable.write_primitive_uint64_le(self.pid)
        else:
            Writable.write_primitive_uint32_le(self.legacy_value())

    def extract_from(self):
        """
        Extracts the PID from the readable object.
        """
        try:
            if Readable.pid_size() == 8:
                self.pid = Readable.read_primitive_uint64_le()
            else:
                self.pid = Readable.read_primitive_uint32_le()
        except Exception as e:
            raise e

    def copy(self):
        """
        Returns a copy of the PID.
        """
        return PID(self.pid)

    def equals(self, other):
        """
        Checks if another instance is equal to this one.
        """
        if not isinstance(other, PID):
            return False
        return self.pid == other.pid

    def value(self):
        """
        Returns the PID value as uint64.
        """
        return self.pid

    def legacy_value(self):
        """
        Returns the PID value as uint32.
        """
        return self.pid & 0xFFFFFFFF

    def __str__(self):
        """
        Returns a string representation of the PID.
        """
        return self.format_to_string(0)

    def format_to_string(self, indentation_level: int):
        """
        Returns a formatted string representation with indentation.
        """
        indentation_values = "\t" * (indentation_level + 1)
        indentation_end = "\t" * indentation_level
        return (
            f"PID{{\n"
            f"{indentation_values}pid: {self.pid}\n"
            f"{indentation_end}}}"
        )