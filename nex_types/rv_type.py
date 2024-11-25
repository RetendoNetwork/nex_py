from nex.nex_types.readable import Readable
from nex.nex_types.writable import Writable


class RVType:
    def write_to(self, writable: Writable):
        raise NotImplementedError

    def copy(self) -> 'RVType':
        raise NotImplementedError

    def copy_ref(self) -> 'RVTypePtr':
        raise NotImplementedError

    def equals(self, other: 'RVType') -> bool:
        raise NotImplementedError

class RVTypePtr(RVType):
    def extract_from(self, readable: Readable):
        raise NotImplementedError

    def deref(self) -> 'RVType':
        raise NotImplementedError