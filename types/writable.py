from abc import ABC, abstractmethod
from typing import Any


class Writable(ABC):
    
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
    def copy_new(self) -> 'Writable':
        """Returns a new Writable with the same settings, but an empty buffer."""
        pass

    @abstractmethod
    def write(self, data: bytes) -> None:
        """Writes the provided data to the buffer."""
        pass

    @abstractmethod
    def write_primitive_uint8(self, value: int) -> None:
        """Writes a primitive uint8."""
        pass

    @abstractmethod
    def write_primitive_uint16_le(self, value: int) -> None:
        """Writes a primitive uint16 (Little Endian)."""
        pass

    @abstractmethod
    def write_primitive_uint32_le(self, value: int) -> None:
        """Writes a primitive uint32 (Little Endian)."""
        pass

    @abstractmethod
    def write_primitive_uint64_le(self, value: int) -> None:
        """Writes a primitive uint64 (Little Endian)."""
        pass

    @abstractmethod
    def write_primitive_int8(self, value: int) -> None:
        """Writes a primitive int8."""
        pass

    @abstractmethod
    def write_primitive_int16_le(self, value: int) -> None:
        """Writes a primitive int16 (Little Endian)."""
        pass

    @abstractmethod
    def write_primitive_int32_le(self, value: int) -> None:
        """Writes a primitive int32 (Little Endian)."""
        pass

    @abstractmethod
    def write_primitive_int64_le(self, value: int) -> None:
        """Writes a primitive int64 (Little Endian)."""
        pass

    @abstractmethod
    def write_primitive_float32_le(self, value: float) -> None:
        """Writes a primitive float32 (Little Endian)."""
        pass

    @abstractmethod
    def write_primitive_float64_le(self, value: float) -> None:
        """Writes a primitive float64 (Little Endian)."""
        pass

    @abstractmethod
    def write_primitive_bool(self, value: bool) -> None:
        """Writes a primitive bool."""
        pass

    @abstractmethod
    def bytes(self) -> bytes:
        """Returns the data written to the buffer."""
        pass