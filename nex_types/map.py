from readable import Readable
from writable import Writable


class Map:
    def __init__(self):
        self.map = {}

    def write_type(self, t: 'Map', writable: Writable):
        if hasattr(t, "write_to"):
            t.write_to(writable)

    def write_to(self, writable: Writable):
        writable.write_uint32_le(len(self.map))
        for key, value in self.map.items():
            self.write_type(key, writable)
            self.write_type(value, writable)

    def extract_type(self, t: 'Map', readable: Readable):
        if hasattr(t, "extract_from"):
            return t.extract_from(readable)
        else:
            raise TypeError(f"Unsupported Map type {type(t)}")

    def extract_from(self, readable: Readable):
        length, err = readable.read_uint32_le()
        if err:
            return err

        extracted = Map()

        for _ in range(length):
            key = type(next(iter(self.map)))
            if err := self.extract_type(key, readable):
                return err
            value = type(self.map[key])
            if err := self.extract_type(value, readable):
                return err
            extracted.map[key] = value

        self.map = extracted.map
        return None

    def copy_type(self, t: 'Map'):
        if hasattr(t, "copy"):
            return t.copy()
        return None

    def copy(self):
        copied = Map()
        for key, value in self.map.items():
            copied.map[self.copy_type(key)] = self.copy_type(value)
        return copied

    def types_equal(self, t1: 'Map', t2):
        if hasattr(t1, "equals") and hasattr(t2, "equals"):
            return t1.equals(t2)
        return False

    def equals(self, other):
        if not isinstance(other, Map):
            return False
        if len(self.map) != len(other.map):
            return False
        for key, value in self.map.items():
            if key not in other.map or not self.types_equal(value, other.map[key]):
                return False
        return True

    def copy_ref(self):
        return self.copy()

    def deref(self):
        return self

    def __str__(self):
        return self.format_to_string(0)

    def format_to_string(self, indentation_level):
        indentation_values = "\t" * (indentation_level + 1)
        indentation_end = "\t" * indentation_level
        if not self.map:
            return "{}\n"
        items = ",\n".join(
            f"{indentation_values}{key}: {value}" for key, value in self.map.items()
        )
        return f"{{\n{items}\n{indentation_end}}}\n"