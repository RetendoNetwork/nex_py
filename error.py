from result_codes import error_mask, result_code_to_name


class Error(Exception):
    def __init__(self, result_code: int, message: str, packet=None):
        """
        Custom error type representing a NEX error.
        
        :param result_code: NEX result code. See result_codes.go for details.
        :param message: The error base message.
        :param packet: The packet which caused the error. This may not always be present.
        """
        self.result_code = result_code
        self.message = message
        self.packet = packet
    
    def __str__(self) -> str:
        """
        This method satisfies the error interface by returning the error message.
        
        :return: A string representation of the error.
        """
        result_code = self.result_code

        if result_code & error_mask != 0:
            # Result codes are stored without the MSB set, so we clear it
            result_code &= ~error_mask

        # Return a formatted string with result code name and message
        return f"[{result_code_to_name(result_code)}] {self.message}"

def new_error(result_code: int, message: str) -> Error:
    """
    Creates a new NEX error with a result code.
    
    :param result_code: The result code.
    :param message: The error message.
    
    :return: A new instance of the custom Error.
    """
    if result_code & error_mask == 0:
        # Set the MSB to mark the result as an error
        result_code |= error_mask

    return Error(result_code, message)