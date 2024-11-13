import socket
from typing import Callable, Optional


class PRUDPV1Settings:
    def __init__(self, 
                 legacy_connection_signature: bool = False,
                 connection_signature_calculator: Optional[Callable] = None,
                 signature_calculator: Optional[Callable] = None):
        self.legacy_connection_signature = legacy_connection_signature
        self.connection_signature_calculator = connection_signature_calculator
        self.signature_calculator = signature_calculator


def new_prudp_v1_settings() -> PRUDPV1Settings:
    return PRUDPV1Settings()