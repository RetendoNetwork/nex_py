import struct
from datetime import datetime

from writable import Writable
from readable import Readable


class DateTime:
    def __init__(self, value=0):
        self.value = value

    def write_to(self, writable: Writable):
        writable.write_uint64_le(self.value)

    def extract_from(self, readable: Readable):
        self.value, err = readable.read_uint64_le()
        if err:
            raise ValueError(f"Failed to read DateTime value: {err}")

    def copy(self):
        return DateTime(self.value)

    def equals(self, other):
        if not isinstance(other, DateTime):
            return False
        return self.value == other.value

    def copy_ref(self):
        return self.copy()

    def deref(self):
        return self

    def make(self, year, month, day, hour, minute, second):
        self.value = (second | (minute << 6) | (hour << 12) | (day << 17) | (month << 22) | (year << 26))
        return self

    def from_timestamp(self, timestamp):
        year = timestamp.year
        month = timestamp.month
        day = timestamp.day
        hour = timestamp.hour
        minute = timestamp.minute
        second = timestamp.second
        return self.make(year, month, day, hour, minute, second)

    def now(self):
        return self.from_timestamp(datetime.utcnow())

    def second(self):
        return self.value & 63

    def minute(self):
        return (self.value >> 6) & 63

    def hour(self):
        return (self.value >> 12) & 31

    def day(self):
        return (self.value >> 17) & 31

    def month(self):
        return (self.value >> 22) & 15

    def year(self):
        return self.value >> 26

    def standard(self):
        return datetime(self.year(), self.month(), self.day(), self.hour(), self.minute(), self.second())

    def __str__(self):
        return self.format_to_string(0)

    def format_to_string(self, indentation_level):
        indentation_values = "\t" * (indentation_level + 1)
        indentation_end = "\t" * indentation_level

        return (
            "DateTime{\n"
            f"{indentation_values}value: {self.value} ({self.standard().strftime('%Y-%m-%d %H:%M:%S')})\n"
            f"{indentation_end}}}"
        )