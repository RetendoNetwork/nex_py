from typing import Callable, Optional


class PRUDPV0Settings:
    def __init__(self, 
                 is_quazal_mode: bool = False,
                 encrypted_connect: bool = False,
                 legacy_connection_signature: bool = False,
                 use_enhanced_checksum: bool = False,
                 connection_signature_calculator: Optional[Callable] = None,
                 signature_calculator: Optional[Callable] = None,
                 data_signature_calculator: Optional[Callable] = None,
                 checksum_calculator: Optional[Callable] = None):
        self.is_quazal_mode = is_quazal_mode
        self.encrypted_connect = encrypted_connect
        self.legacy_connection_signature = legacy_connection_signature
        self.use_enhanced_checksum = use_enhanced_checksum
        self.connection_signature_calculator = connection_signature_calculator
        self.signature_calculator = signature_calculator
        self.data_signature_calculator = data_signature_calculator
        self.checksum_calculator = checksum_calculator


def new_prudp_v0_settings() -> PRUDPV0Settings:
    return PRUDPV0Settings()