from enum import Enum

class IPOState(str, Enum):
    DISCOVERED = "DISCOVERED"
    WATCHING = "WATCHING"
    IPO_DAY = "IPO_DAY"
    READY = "READY"
    BUY_SIGNAL = "BUY_SIGNAL"
    HOLDING = "HOLDING"
    EXITED = "EXITED"
    MISSED = "MISSED"
