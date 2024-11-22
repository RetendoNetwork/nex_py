from enum import IntEnum, unique


@unique
class StreamType(IntEnum):
    DO = 0x1                # DO PRUDP virtual connection stream type
    RV = 0x2                # RV PRUDP virtual connection stream type
    OldRVSec = 0x3          # OldRVSec PRUDP virtual connection stream type
    SBMGMT = 0x4            # SBMGMT PRUDP virtual connection stream type
    NAT = 0x5               # NAT PRUDP virtual connection stream type
    SessionDiscovery = 0x6  # SessionDiscovery PRUDP virtual connection stream type
    NATEcho = 0x7           # NATEcho PRUDP virtual connection stream type
    Routing = 0x8           # Routing PRUDP virtual connection stream type
    Game = 0x9              # Game PRUDP virtual connection stream type
    RVSecure = 0x10         # RVSecure PRUDP virtual connection stream type
    Relay = 0x11            # Relay PRUDP virtual connection stream type

    def enum_index(self) -> int:
        return self.value