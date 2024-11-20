from enum import Enum

class TradeStatus(Enum):
    PENDING = 1
    COMPLETED = 2
    CANCEL = 3

class CountryCode(Enum):
    KR = "KR"
    US = "US"