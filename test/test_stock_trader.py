#not check
import pytest
from stock_trader import StockTrader
from dummy_broker_api import DummyBrokerAPI

def test_initialize_stack():
    api = DummyBrokerAPI()
    trader = StockTrader("Samsung", api)
    assert trader.stack == []

def test_execute_trade_buy():
    api = DummyBrokerAPI()
    trader = StockTrader("Samsung", api)
    trader.rounds = [{"buy_price": 50000, "sell_price": 55000, "amount": 100000}]
    trader.current_price = 50000
    trader.execute_trade("buy")
    assert len(trader.stack) == 1

def test_execute_trade_sell():
    api = DummyBrokerAPI()
    trader = StockTrader("Samsung", api)
    trader.rounds = [{"buy_price": 50000, "sell_price": 55000, "amount": 100000}]
    trader.stack.append({"price": 50000, "amount": 2})
    trader.current_price = 55000
    trader.execute_trade("sell")
    assert len(trader.stack) == 0