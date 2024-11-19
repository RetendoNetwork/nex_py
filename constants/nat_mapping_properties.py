from enum import Enum, auto

class NATMappingProperties(Enum):
    # Indicates that the NAT type could not be identified
    UnknownNATMapping = 0
    
    # Indicates endpoint-independent mapping
    EIMNATMapping = 1
    
    # Indicates endpoint-dependent mapping
    EDMNATMapping = 2