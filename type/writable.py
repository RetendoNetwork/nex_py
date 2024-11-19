from abc import ABC, abstractmethod

class Writable(ABC):
    @abstractmethod
    def string_length_size(self):
        """
        Returns the size of the length field for String types.
        Only 2 and 4 are valid.
        """
        pass

    @abstractmethod
    def pid_size(self):
        """
        Returns the size of the length fields for PID types.
        Only 4 and 8 are valid.
        """
        pass

    @abstractmethod
    def use_structure_header(self):
        """
        Returns whether or not Structure types should use a header.
        """
        pass

    @abstractmethod
    def copy_new(self):
        """
        Returns a new Writable with the same settings, but an empty buffer.
        """
        pass

    @abstractmethod
    def write(self, data):
        """
        Writes the provided data to the buffer.
        """
        pass

    @abstractmethod
    def write_uint8(self, value):
        """
        Writes a primitive Python uint8.
        """
        pass

    @abstractmethod
    def write_uint16_le(self, value):
        """
        Writes a primitive Python uint16.
        """
        pass

    @abstractmethod
    def write_uint32_le(self, value):
        """
        Writes a primitive Python uint32.
        """
        pass

    @abstractmethod
    def write_uint64_le(self, value):
        """
        Writes a primitive Python uint64.
        """
        pass

    @abstractmethod
    def write_int8(self, value):
        """
        Writes a primitive Python int8.
        """
        pass

    @abstractmethod
    def write_int16_le(self, value):
        """
        Writes a primitive Python int16.
        """
        pass

    @abstractmethod
    def write_int32_le(self, value):
        """
        Writes a primitive Python int32.
        """
        pass

    @abstractmethod
    def write_int64_le(self, value):
        """
        Writes a primitive Python int64.
        """
        pass

    @abstractmethod
    def write_float32_le(self, value):
        """
        Writes a primitive Python float32.
        """
        pass

    @abstractmethod
    def write_float64_le(self, value):
        """
        Writes a primitive Python float64.
        """
        pass

    @abstractmethod
    def write_bool(self, value):
        """
        Writes a primitive Python bool.
        """
        pass

    @abstractmethod
    def bytes(self):
        """
        Returns the data written to the buffer.
        """
        pass