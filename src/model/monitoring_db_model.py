from dataclasses import dataclass
from src.util.enums import CountryCode, QueryOp


# 기본 필드 순서
FIELD_ORDER = ["stock_name", "code", "country_code", "trade_round", "price", "buy_rate", "sell_rate"]

@dataclass
class MonitoringData:
    stock_name: str
    code: str
    country_code: CountryCode
    trade_round: int
    price : float
    buy_rate: int
    sell_rate: int

    def to_tuple(self, field_order=FIELD_ORDER):
        # 필드 이름 순서에 따라 튜플 생성
        return tuple(getattr(self, field) for field in field_order)

@dataclass
class AlgorithmData:
    QueryOp: QueryOp
    MonitoringData: MonitoringData