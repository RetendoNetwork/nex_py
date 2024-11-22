from nex_types.pid import PID


class Account:
    def __init__(self, pid: PID, username, password):
        self.pid = pid
        self.username = username
        self.password = password