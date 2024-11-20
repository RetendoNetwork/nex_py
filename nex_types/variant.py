from typing import Dict, Any

from nex.nex_types.writable import Writable
from nex.nex_types.readable import Readable
from nex.nex_types.uint8 import UInt8
from nex.nex_types.rv_type import RVType


VariantTypes: Dict[UInt8, RVType] = {}

def register_variant_type(type_id: UInt8, rv_type: RVType):
    VariantTypes[type_id] = rv_type

class Variant:
    def __init__(self):
        self.type_id = UInt8(0)
        self.type = RVType

    def write_to(self, writable: Writable):
        self.type_id.write_to(writable)
        if self.type is not None:
            self.type.write_to(writable)

    def extract_from(self, readable: Readable):
        self.type_id.extract_from(readable)

        if self.type_id.value == 0:
            return

        if self.type_id not in VariantTypes:
            raise ValueError(f"Invalid Variant type ID {self.type_id}")

        self.type = VariantTypes[self.type_id].copy_ref()
        self.type.extract_from(readable)

    def copy(self) -> 'Variant':
        copied = Variant()
        copied.type_id = self.type_id.copy()

        if self.type is not None:
            copied.type = self.type.copy()

        return copied

    def equals(self, other: 'Variant') -> bool:
        if not isinstance(other, Variant):
            return False

        if not self.type_id.equals(other.type_id):
            return False

        if self.type is not None:
            return self.type.equals(other.type)

        return True

    def copy_ref(self) -> 'Variant':
        return self.copy()

    def deref(self) -> 'Variant':
        return self

    def __str__(self) -> str:
        return self.format_to_string(0)

    def format_to_string(self, indentation_level: int) -> str:
        indentation_values = "\t" * (indentation_level + 1)
        indentation_end = "\t" * indentation_level

        result = []
        result.append("Variant{")
        result.append(f"{indentation_values}TypeID: {self.type_id},")

        if self.type is not None:
            result.append(f"{indentation_values}Type: {self.type}")
        else:
            result.append(f"{indentation_values}Type: None")

        result.append(f"{indentation_end}}}")

        return "\n".join(result)