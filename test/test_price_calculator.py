# test_price_calculator.py
import pytest
from your_module import PriceCalculator  # 실제 파일명에 맞게 수정하세요

class TestPriceCalculator:
    @pytest.mark.parametrize("base_price, percentage, is_buy, expected", [
        (100, 10, True, 90),      # 매수 시 10% 감소
        (100, 10, False, 110),    # 매도 시 10% 증가
        (200, 20, True, 160),     # 매수 시 20% 감소
        (200, 20, False, 240),    # 매도 시 20% 증가
        (150, 5, True, 142.5),    # 매수 시 5% 감소
        (150, 5, False, 157.5),   # 매도 시 5% 증가
        (100, 0, True, 100),      # 0% 변화 시 매수가
        (100, 0, False, 100)      # 0% 변화 시 매도가
    ])
    def test_calculate_price(self, base_price, percentage, is_buy, expected):
        result = PriceCalculator.calculate_price(base_price, percentage, is_buy)
        assert result == pytest.approx(expected, rel=1e-2), f"Expected {expected}, but got {result}"