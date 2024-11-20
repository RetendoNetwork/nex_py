from typing import Optional

from nex.nex_types.pid import PID


class Account:
    def __init__(self, pid: PID, username: str, password: str):
        """
        Represents a game server account.
        
        :param pid: The PID of the account. PIDs are unique IDs per account.
                    NEX PIDs start at 1800000000 and decrement with each new account.
        :param username: The username for the account. For NEX user accounts, this is the same as the account's PID.
        :param password: The password for the account. For NEX accounts, this is always 16 characters long using seemingly any ASCII character.
        """
        self.pid = pid
        self.username = username
        self.password = password