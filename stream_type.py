from enum import IntEnum, unique


@unique
class StreamType(IntEnum):
    DO = 1
    RV = 2
    OlD_RV_SEC = 3
    SBMGMT = 4
    NAT = 5
    SESSION_DISCOVERY = 6
    NAT_ECHO = 7
    ROUTING = 8
    GAME = 9
    RV_SECURE = 10
    RELAY = 11

    def enum_index(self) -> int:
        return self.value