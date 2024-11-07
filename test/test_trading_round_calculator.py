#not check
import pytest
from trading_round_calculator import TradingRoundCalculator

def test_setup_trading_rounds():
    calc = TradingRoundCalculator(initial_price=1000, buy_percentages=[5, 10], sell_percentages=[7, 12], buy_amounts=[100000, 200000])
    calc.setup_trading_rounds()
    assert len(calc.rounds) == 2
    assert calc.rounds[0]["buy_price"] == 1050
    assert calc.rounds[1]["sell_price"] == 1120

def test_get_round_info():
    calc = TradingRoundCalculator(initial_price=1000, buy_percentages=[5], sell_percentages=[7], buy_amounts=[100000])
    calc.setup_trading_rounds()
    round_info = calc.get_round_info(0)
    assert round_info["buy_price"] == 1050
    assert round_info["sell_price"] == 1070