from nex.nex_types.rv_type import RVType, RVTypePtr
from nex.nex_types.writable import Writable
from nex.nex_types.readable import Readable
from nex.nex_types.string import String


class AnyDataHolder:
    AnyDataHolderObjects = {}

    @staticmethod
    def register_data_holder_type(name, rv_type):
        AnyDataHolder.AnyDataHolderObjects[name] = rv_type

    def __init__(self):
        self.type_name = String()
        self.length1 = 0
        self.length2 = 0
        self.object_data = RVType()

    def write_to(self, writable: Writable):
        content_writable = writable.copy_new()

        self.object_data.write_to(content_writable)

        object_data = content_writable.bytes()
        length1 = len(object_data) + 4
        length2 = len(object_data)

        self.type_name(writable)
        writable.write_uint32_le(length1)
        writable.write_uint32_le(length2)
        writable.write(object_data)

    def extract_from(self, readable: Readable):
        err = None

        try:
            self.type_name.extract_from(readable)
        except Exception as e:
            return f"Failed to read AnyDataHolder type name. {str(e)}"

        try:
            self.length1
        except Exception as e:
            return f"Failed to read AnyDataHolder length 1. {str(e)}"

        try:
            self.length2
        except Exception as e:
            return f"Failed to read AnyDataHolder length 2. {str(e)}"

        type_name = String(self.type_name)

        if type_name not in AnyDataHolder:
            return f"Unknown AnyDataHolder type: {type_name}"

        self.object_data = AnyDataHolder.AnyDataHolderObjects[type_name].copy()

        if not isinstance(self.object_data, RVTypePtr):
            return "AnyDataHolder object data is not a valid RVType. Missing ExtractFrom pointer receiver"

        try:
            self.object_data.extract_from(readable)
        except Exception as e:
            return f"Failed to read AnyDataHolder object data. {str(e)}"

        return None

    def copy(self) -> RVType:
        copied = AnyDataHolder()
        copied.type_name = self.type_name
        copied.length1 = self.length1
        copied.length2 = self.length2
        copied.object_data = self.object_data.copy()
        return copied

    def equals(self, other: RVType) -> bool:
        if not isinstance(other, AnyDataHolder):
            return False

        if self.type_name != other.type_name:
            return False

        if self.length1 != other.length1:
            return False

        if self.length2 != other.length2:
            return False

        return self.object_data.equals(other.object_data)

    def copy_ref(self) -> RVTypePtr:
        return self.copy()

    def deref(self) -> RVType:
        return self

    def __str__(self):
        return self.format_to_string(0)

    def format_to_string(self, indentation_level: int):
        indentation_values = "\t" * (indentation_level + 1)
        indentation_end = "\t" * indentation_level

        return (f"AnyDataHolder{{\n"
                f"{indentation_values}TypeName: {self.type_name},\n"
                f"{indentation_values}Length1: {self.length1},\n"
                f"{indentation_values}Length2: {self.length2},\n"
                f"{indentation_values}ObjectData: {self.object_data}\n"
                f"{indentation_end}}}")

    @staticmethod
    def new_any_data_holder():
        return AnyDataHolder()