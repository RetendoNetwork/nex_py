from enum import Enum


class ConnectionState(Enum):
    StateNotConnected = 0

    StateConnecting = 1

    StateConnected = 2

    StateDisconnecting = 3

    StateFaulty = 4