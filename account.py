from nex.nex_types.pid import PID


class Account:
    def __init__(self, pid: PID, username: str, password: str) -> None:
        self.pid = pid
        self.username = username
        self.password = password

    def new_account(cls, pid: PID, username: str, password: str) -> 'Account':
        return cls(pid, username, password)