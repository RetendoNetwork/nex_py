from enum import IntEnum, unique


@unique
class PRUDPPacketTypes(IntEnum):
    SYN_PACKET = 0x0
    CONNECT_PACKET= 0x1
    DATA_PACKET = 0x2
    DISCONNECT_PACKET = 0x3
    PING_PACKET = 0x4