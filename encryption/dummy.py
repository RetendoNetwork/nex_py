class Dummy:
    """
    Dummy does no encryption. Payloads are returned as-is.
    """

    def __init__(self):
        """Initialize a new instance of the Dummy encryption with an empty key."""
        self.key = []

    def get_key(self) -> list:
        """
        Returns the encryption key.
        
        :return: The key as a list of bytes.
        """
        return self.key

    def set_key(self, key: list) -> None:
        """
        Sets the encryption key.
        
        :param key: A list of bytes representing the key.
        """
        self.key = key

    def encrypt(self, payload: list) -> list:
        """
        Does nothing to the payload.
        
        :param payload: A list of bytes to "encrypt."
        :return: The payload as-is.
        """
        return payload

    def decrypt(self, payload: list) -> list:
        """
        Does nothing to the payload.
        
        :param payload: A list of bytes to "decrypt."
        :return: The payload as-is.
        """
        return payload

    def copy(self) -> 'Dummy':
        """
        Returns a copy of the Dummy algorithm, retaining its state.
        
        :return: A new instance of Dummy with the same key.
        """
        copied = Dummy()
        copied.set_key(self.key)
        return copied