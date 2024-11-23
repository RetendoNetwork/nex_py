from nex_types.pid import PID


class Account:
    def __init__(self, pid: PID, username: str, password: str) -> None:
        self.PID = pid
        self.Username = username
        self.Password = password

    def new_account(pid: PID, username: str, password: str) -> 'Account':
        return Account(pid, username, password)