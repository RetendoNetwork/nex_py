from enum import Enum


class ConnectionState(Enum):
    STATE_NOT_CONNECTED = 0
    STATE_CONNECTING = 1
    STATE_CONNECTED = 2
    STATE_DISCONNECTING = 3
    STATE_FAULTY = 4