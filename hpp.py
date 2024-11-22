from nex_types.pid import PID


class HPPClient:
    def __init__(self, address, endpoint: 'HPPServer', pid: PID):
        self.address = address
        self.endpoint = endpoint
        self.pid = pid

class HPPPacket:
    def __init__(self, sender: 'HPPClient', access_key_signature, password_signature, payload, message, processed):
        self.sender = sender
        self.access_key_signature = access_key_signature
        self.password_signature = password_signature
        self.payload = payload
        self.message = message
        self.processed = processed

class HPPServer:
    def __init__(self, server, access_key, datahandlers, error_event_handlers, account_details_by_pid, account_details_by_username, use_verbose_rmc):
        self.server = server
        self.access_key = access_key
        self.datahandlers = datahandlers
        self.error_env_handlers = error_event_handlers
        self.account_details_by_pid = account_details_by_pid
        self.account_details_by_username = account_details_by_username
        self.use_verbose_rmc = use_verbose_rmc