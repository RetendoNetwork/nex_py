from abc import ABC, abstractmethod


class Readable(ABC):
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
    def remaining(self):
        """
        Returns the number of bytes left unread in the buffer.
        """
        pass

    @abstractmethod
    def read_remaining(self):
        """
        Reads the remaining data from the buffer.
        """
        pass

    @abstractmethod
    def read(self, length):
        """
        Reads up to length bytes of data from the buffer.
        Returns an error if the read failed, such as if there was not enough data to read.
        """
        pass

    @abstractmethod
    def read_uint8(self):
        """
        Reads a primitive Python uint8.
        Returns an error if the read failed, such as if there was not enough data to read.
        """
        pass

    @abstractmethod
    def read_uint16_le(self):
        """
        Reads a primitive Python uint16.
        Returns an error if the read failed, such as if there was not enough data to read.
        """
        pass

    @abstractmethod
    def read_uint32_le(self):
        """
        Reads a primitive Python uint32.
        Returns an error if the read failed, such as if there was not enough data to read.
        """
        pass

    @abstractmethod
    def read_uint64_le(self):
        """
        Reads a primitive Python uint64.
        Returns an error if the read failed, such as if there was not enough data to read.
        """
        pass

    @abstractmethod
    def read_int8(self):
        """
        Reads a primitive Python int8.
        Returns an error if the read failed, such as if there was not enough data to read.
        """
        pass

    @abstractmethod
    def read_int16_le(self):
        """
        Reads a primitive Python int16.
        Returns an error if the read failed, such as if there was not enough data to read.
        """
        pass

    @abstractmethod
    def read_int32_le(self):
        """
        Reads a primitive Python int32.
        Returns an error if the read failed, such as if there was not enough data to read.
        """
        pass

    @abstractmethod
    def read_int64_le(self):
        """
        Reads a primitive Python int64.
        Returns an error if the read failed, such as if there was not enough data to read.
        """
        pass

    @abstractmethod
    def read_float32_le(self):
        """
        Reads a primitive Python float32.
        Returns an error if the read failed, such as if there was not enough data to read.
        """
        pass

    @abstractmethod
    def read_float64_le(self):
        """
        Reads a primitive Python float64.
        Returns an error if the read failed, such as if there was not enough data to read.
        """
        pass

    @abstractmethod
    def read_bool(self):
        """
        Reads a primitive Python bool.
        Returns an error if the read failed, such as if there was not enough data to read.
        """
        pass