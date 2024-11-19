from abc import ABC, abstractmethod
from typing import List

class Algorithm(ABC):
    """
    Algorithm defines all the methods an encryption algorithm should have.
    """

    @abstractmethod
    def key(self) -> List[int]:
        """Returns the key as a list of bytes."""
        pass

    @abstractmethod
    def set_key(self, key: List[int]) -> None:
        """
        Sets the encryption key.

        :param key: A list of bytes representing the key.
        :raises ValueError: If the key is invalid.
        """
        pass

    @abstractmethod
    def encrypt(self, payload: List[int]) -> List[int]:
        """
        Encrypts the given payload.

        :param payload: A list of bytes to encrypt.
        :return: The encrypted payload as a list of bytes.
        :raises Exception: If encryption fails.
        """
        pass

    @abstractmethod
    def decrypt(self, payload: List[int]) -> List[int]:
        """
        Decrypts the given payload.

        :param payload: A list of bytes to decrypt.
        :return: The decrypted payload as a list of bytes.
        :raises Exception: If decryption fails.
        """
        pass

    @abstractmethod
    def copy(self) -> 'Algorithm':
        """
        Returns a copy of the encryption algorithm instance.

        :return: A new instance of the algorithm with the same state.
        """
        pass