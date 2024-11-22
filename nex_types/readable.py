from abc import ABC, abstractmethod


class Readable(ABC):
    @abstractmethod
    def string_length_size(self) -> int: pass

    @abstractmethod
    def pid_size(self) -> int: pass

    @abstractmethod
    def use_structure_header(self) -> bool: pass

    @abstractmethod
    def remaining(self): pass

    @abstractmethod
    def read_remaining(self): pass

    @abstractmethod
    def read(self, length): pass

    @abstractmethod
    def read_uint8(self): pass

    @abstractmethod
    def read_uint16_le(self): pass

    @abstractmethod
    def read_uint32_le(self): pass

    @abstractmethod
    def read_uint64_le(self): pass

    @abstractmethod
    def read_int8(self): pass

    @abstractmethod
    def read_int16_le(self): pass

    @abstractmethod
    def read_int32_le(self): pass

    @abstractmethod
    def read_int64_le(self): pass

    @abstractmethod
    def read_float32_le(self): pass

    @abstractmethod
    def read_float64_le(self): pass

    @abstractmethod
    def read_bool(self): pass