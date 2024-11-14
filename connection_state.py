from enum import Enum


class ConnectionState(Enum):
    # StateNotConnected indicates the client has not established a full PRUDP connection
    StateNotConnected = 0

    # StateConnecting indicates the client is attempting to establish a PRUDP connection
    StateConnecting = 1

    # StateConnected indicates the client has established a full PRUDP connection
    StateConnected = 2

    # StateDisconnecting indicates the client is disconnecting from a PRUDP connection. Currently unused
    StateDisconnecting = 3

    # StateFaulty indicates the client connection is faulty. Currently unused
    StateFaulty = 4