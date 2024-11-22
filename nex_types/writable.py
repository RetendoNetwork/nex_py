from abc import ABC, abstractmethod


class Writable(ABC):
    @abstractmethod
    def string_length_size(self) -> int: pass

    @abstractmethod
    def pid_size(self) -> int: pass

    @abstractmethod
    def use_structure_header(self) -> bool: pass

    @abstractmethod
    def copy_new(self) -> 'Writable': pass

    @abstractmethod
    def write(self, data): pass

    @abstractmethod
    def write_uint8(self, value): pass

    @abstractmethod
    def write_uint16_le(self, value): pass

    @abstractmethod
    def write_uint32_le(self, value): pass

    @abstractmethod
    def write_uint64_le(self, value): pass

    @abstractmethod
    def write_int8(self, value): pass

    @abstractmethod
    def write_int16_le(self, value): pass

    @abstractmethod
    def write_int32_le(self, value): pass

    @abstractmethod
    def write_int64_le(self, value): pass

    @abstractmethod
    def write_float32_le(self, value): pass

    @abstractmethod
    def write_float64_le(self, value): pass

    @abstractmethod
    def write_bool(self, value: bool): pass

    @abstractmethod
    def bytes(self): pass