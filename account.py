from nex.nex_types.pid import PID


class Account:
    def __init__(self, pid: PID, username, password) -> None:
        self.PID = pid
        self.Username = username
        self.Password = password

    def new_account(pid: PID, username, password) -> 'Account':
        return Account(pid, username, password)