from enum import IntEnum, unique


@unique
class StreamType(IntEnum):
    """
    StreamType represents the different types of PRUDP virtual connection streams.
    Each stream type has its own state and is used to create VirtualPorts.
    """
    DO = 1                # DO PRUDP virtual connection stream type
    RV = 2                # RV PRUDP virtual connection stream type
    OldRVSec = 3          # OldRVSec PRUDP virtual connection stream type
    SBMGMT = 4            # SBMGMT PRUDP virtual connection stream type
    NAT = 5               # NAT PRUDP virtual connection stream type
    SessionDiscovery = 6  # SessionDiscovery PRUDP virtual connection stream type
    NATEcho = 7           # NATEcho PRUDP virtual connection stream type
    Routing = 8           # Routing PRUDP virtual connection stream type
    Game = 9              # Game PRUDP virtual connection stream type
    RVSecure = 10         # RVSecure PRUDP virtual connection stream type
    Relay = 11            # Relay PRUDP virtual connection stream type

    def enum_index(self) -> int:
        """Returns the StreamType enum index as an integer."""
        return self.value