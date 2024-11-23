from enum import IntEnum, unique


@unique
class StreamType(IntEnum):
    DO = 1
    RV = 2
    OldRVSec = 3
    SBMGMT = 4
    NAT = 5
    SessionDiscovery = 6
    NATEcho = 7
    Routing = 8
    Game = 9
    RVSecure = 10
    Relay = 11

    def enum_index(self) -> int:
        return self.value