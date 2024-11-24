from typing import Optional

from nex.packet_interface import PacketInterface
from nex.result_codes import error_mask


class Error(Exception): 
    def __init__(self, result_code: int, message: str, packet: Optional[PacketInterface]):
        self.result_code = result_code
        self.message = message
        self.packet = packet
        
        if (self.result_code & error_mask) == 0:
            self.result_code |= error_mask

    def __str__(self) -> str:
        result_code = self.result_code

        if (result_code & error_mask) != 0:
            result_code &= ~error_mask
        
        result_code_name = self.result_code_to_name(result_code)
        
        return f"[{result_code_name}] {self.message}"
    
    def result_code_to_name(self, result_code: int) -> str:
        return f"Code {result_code}"

    def new_error(result_code: int, message: str) -> 'Error':
        return Error(result_code, message)