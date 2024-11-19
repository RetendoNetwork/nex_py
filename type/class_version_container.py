from readable import Readable
from writable import Writable
from map import Map

class ClassVersionContainer:
    def __init__(self):
        self.structure_version = 0
        self.class_versions = Map()

    def write_to(self, writable: Writable):
        self.class_versions.write_to(writable)

    def extract_from(self, readable: Readable):
        return self.class_versions.extract_from(readable)

    def copy(self):
        copied = ClassVersionContainer()
        copied.class_versions = self.class_versions.copy()
        return copied

    def equals(self, other):
        if not isinstance(other, ClassVersionContainer):
            return False
        return self.class_versions == other.class_versions

    def copy_ref(self):
        copied = self.copy()
        return copied

    def deref(self):
        return self

    def __str__(self):
        return self.format_to_string(0)

    def format_to_string(self, indentation_level):
        indentation_values = "\t" * (indentation_level + 1)
        indentation_end = "\t" * indentation_level

        return (
            "ClassVersionContainer{\n"
            f"{indentation_values}StructureVersion: {self.structure_version},\n"
            f"{indentation_values}ClassVersions: {self.class_versions}\n"
            f"{indentation_end}}}"
        )

def new_class_version_container():
    cvc = ClassVersionContainer()
    cvc.class_versions = {}
    return cvc