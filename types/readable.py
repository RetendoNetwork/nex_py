from abc import ABC, abstractmethod
from typing import List, Tuple


class Readable(ABC):

    @abstractmethod
    def string_length_size(self) -> int:
        """Returns the size of the length field for rdv::String types. Only 2 and 4 are valid."""
        pass

    @abstractmethod
    def pid_size(self) -> int:
        """Returns the size of the length fields for nn::nex::PID types. Only 4 and 8 are valid."""
        pass

    @abstractmethod
    def use_structure_header(self) -> bool:
        """Returns whether or not Structure types should use a header."""
        pass

    @abstractmethod
    def remaining(self) -> int:
        """Returns the number of bytes left unread in the buffer."""
        pass

    @abstractmethod
    def read_remaining(self) -> List[bytes]:
        """Reads the remaining data from the buffer."""
        pass

    @abstractmethod
    def read(self, length: int) -> Tuple[bytes, Exception]:
        """Reads up to length bytes of data from the buffer.
        Returns a tuple with data and error if read fails."""
        pass

    @abstractmethod
    def read_primitive_uint8(self) -> Tuple[int, Exception]:
        """Reads a primitive uint8.
        Returns a tuple with value and error if read fails."""
        pass

    @abstractmethod
    def read_primitive_uint16_le(self) -> Tuple[int, Exception]:
        """Reads a primitive uint16 (Little Endian).
        Returns a tuple with value and error if read fails."""
        pass

    @abstractmethod
    def read_primitive_uint32_le(self) -> Tuple[int, Exception]:
        """Reads a primitive uint32 (Little Endian).
        Returns a tuple with value and error if read fails."""
        pass

    @abstractmethod
    def read_primitive_uint64_le(self) -> Tuple[int, Exception]:
        """Reads a primitive uint64 (Little Endian).
        Returns a tuple with value and error if read fails."""
        pass

    @abstractmethod
    def read_primitive_int8(self) -> Tuple[int, Exception]:
        """Reads a primitive int8.
        Returns a tuple with value and error if read fails."""
        pass

    @abstractmethod
    def read_primitive_int16_le(self) -> Tuple[int, Exception]:
        """Reads a primitive int16 (Little Endian).
        Returns a tuple with value and error if read fails."""
        pass

    @abstractmethod
    def read_primitive_int32_le(self) -> Tuple[int, Exception]:
        """Reads a primitive int32 (Little Endian).
        Returns a tuple with value and error if read fails."""
        pass

    @abstractmethod
    def read_primitive_int64_le(self) -> Tuple[int, Exception]:
        """Reads a primitive int64 (Little Endian).
        Returns a tuple with value and error if read fails."""
        pass

    @abstractmethod
    def read_primitive_float32_le(self) -> Tuple[float, Exception]:
        """Reads a primitive float32 (Little Endian).
        Returns a tuple with value and error if read fails."""
        pass

    @abstractmethod
    def read_primitive_float64_le(self) -> Tuple[float, Exception]:
        """Reads a primitive float64 (Little Endian).
        Returns a tuple with value and error if read fails."""
        pass

    @abstractmethod
    def read_primitive_bool(self) -> Tuple[bool, Exception]:
        """Reads a primitive bool.
        Returns a tuple with value and error if read fails."""
        pass