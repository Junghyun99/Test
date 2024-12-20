import pytest
from src.model.monitoring_db_model import MonitoringData
from src.util.enums import CountryCode


def test_create_object_positional():
    """순서대로 필드를 넣어 MonitoringData 객체 생성"""
    data = MonitoringData(1, "Samsung", "005930", CountryCode.KR, 1, 70000.0, 10, 0.95, 1.05)
    assert data.stock_name == "Samsung"
    assert data.code == "005930"
    assert data.country_code == CountryCode.KR
    assert data.price == 70000.0
    assert data.trade_round == 1
    assert data.buy_rate == 0.95
    assert data.sell_rate == 1.05

def test_create_object_keyword():
    """키워드로 필드를 섞어서 MonitoringData 객체 생성"""
    data = MonitoringData(code="005930", stock_name="Samsung", price=70000.0, 
                          country_code=CountryCode.KR, trade_round=1, quantity=10, buy_rate=0.95, sell_rate=1.05, id=1)
    assert data.stock_name == "Samsung"
    assert data.code == "005930"
    assert data.country_code == CountryCode.KR
    assert data.price == 70000.0
    assert data.trade_round == 1
    assert data.buy_rate == 0.95
    assert data.sell_rate == 1.05

def test_to_tuple_default_order():
    """to_tuple 메서드 테스트: 기본 필드 순서"""
    data = MonitoringData(1, "Samsung", "005930", CountryCode.KR, 1, 70000.0, 10, 0.95, 1.05)
    result = data.to_tuple()
    expected = (1, "Samsung", "005930", CountryCode.KR, 1, 70000.0, 10, 0.95, 1.05)
    assert result == expected

def test_to_tuple_custom_order():
    """to_tuple 메서드 테스트: 사용자 정의 필드 순서"""
    data = MonitoringData(1, "Samsung", "005930", CountryCode.KR, 1, 70000.0, 10, 0.95, 1.05)
    custom_order = ["code", "stock_name", "price"]
    result = data.to_tuple_field(custom_order)
    expected = ("005930", "Samsung", 70000.0)
    assert result == expected

def test_to_tuple_empty_order():
    """to_tuple 메서드 테스트: 빈 필드 순서"""
    data = MonitoringData(1, "Samsung", "005930", CountryCode.KR, 1 , 70000.0, 10, 0.95, 1.05)
    result = data.to_tuple_field([])
    expected = ()
    assert result == expected