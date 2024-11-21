from enum import Enum

class TradeStatus(Enum):
    PENDING = 1
    COMPLETED = 2
    CANCEL = 3

class CountryCode(Enum):
    KR = "KR"
    US = "US"

class QueryOp(Enum):
    READ = 1
    INSERT = 2
    DELETE = 3
    UPDATE = 4
    DEFAULT = 5
