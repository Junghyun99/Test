from dataclasses import dataclass
from src.util.enums import CountryCode, QueryOp

@dataclass
class MonitoringData:
    stock_name: str
    code: str
    country_code: CountryCode
    trade_round: int
    price : float
    quantity : int
    buy_rate: int
    sell_rate: int

    DUMMY = ("stock", "code", CountryCode.KR, 0, 0.0, 0, 0, 0)

    def __post_init__(self):
        if self.country_code == "KR": 
            self.country_code = CountryCode.KR
        if self.country_code == "US": 
            self.country_code = CountryCode.US
        if not isinstance(self.country_code, CountryCode):
            raise ValueError(f"Invalid country_code: {self.country_code}")

    def to_tuple(self):
        return tuple(getattr(self, field) for field in self.__dataclass_fields__)


    def to_tuple_field(self, field_order):
        # 필드 이름 순서에 따라 튜플 생성
        return tuple(getattr(self, field) for field in field_order)

@dataclass
class AlgorithmData:
    QueryOp: QueryOp
    MonitoringData: MonitoringData

    def __post_init__(self):
        if not isinstance(self.QueryOp, QueryOp):
            raise ValueError(f"Invalid QueryOp: {self.QueryOp}")

        if not isinstance(self.MonitoringData, MonitoringData):
            raise ValueError(f"Invalid MonitoringData: {self.MonitoringData}")

