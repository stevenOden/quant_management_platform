from enum import Enum

class IPOState(str, Enum):
    DISCOVERED = "DISCOVERED"
    WATCHING = "WATCHING"
    READY = "READY"
    BUY_SIGNAL = "BUY_SIGNAL"
    HOLDING = "HOLDING"
    EXITED = "EXITED"
