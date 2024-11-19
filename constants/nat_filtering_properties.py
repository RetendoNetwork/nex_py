from enum import Enum

class NATFilteringProperties(Enum):
    # Indicates that the NAT type could not be identified
    UnknownNATFiltering = 0
    
    # Indicates port-independent filtering
    PIFNATFiltering = 1
    
    # Indicates port-dependent filtering
    PDFNATFiltering = 2