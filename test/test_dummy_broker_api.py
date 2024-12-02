import pytest
from src.service.broker.dummy_broker_api import DummyBrokerAPI

@pytest.fixture
def dummy_broker():
    return DummyBrokerAPI()

# Tests for get_current_price
def test_get_current_price_returns_float(dummy_broker):
    price = dummy_broker.get_current_price("AAPL")
    assert isinstance(price, float)

def test_get_current_price_in_range(dummy_broker):
    price = dummy_broker.get_current_price("AAPL")
    assert 100 <= price <= 500

def test_get_current_price_symbol_changes(dummy_broker):
    price_1 = dummy_broker.get_current_price("AAPL")
    price_2 = dummy_broker.get_current_price("TSLA")
    assert price_1 != price_2

def test_get_current_price_precision(dummy_broker):
    price = dummy_broker.get_current_price("AAPL")
    assert round(price, 2) == price

def test_get_current_price_multiple_symbols(dummy_broker):
    symbols = ["AAPL", "TSLA", "GOOGL"]
    prices = [dummy_broker.get_current_price(symbol) for symbol in symbols]
    assert all(100 <= price <= 500 for price in prices)

# Tests for place_market_order
def test_place_market_order_creates_order(dummy_broker):
    order_id = dummy_broker.place_market_order("AAPL", 10, "buy")
    assert order_id in dummy_broker.order

def test_place_market_order_increments_number(dummy_broker):
    dummy_broker.place_market_order("AAPL", 10, "buy")
    assert dummy_broker.number == 1

def test_place_market_order_different_ids(dummy_broker):
    order_id1 = dummy_broker.place_market_order("AAPL", 10, "buy")
    order_id2 = dummy_broker.place_market_order("AAPL", 5, "sell")
    assert order_id1 != order_id2

def test_place_market_order_pending_or_complete(dummy_broker):
    order_id = dummy_broker.place_market_order("AAPL", 10, "buy")
    assert dummy_broker.order[order_id] in ["pending", "complete"]

# Tests for place_limit_order
def test_place_limit_order_creates_order(dummy_broker):
    order_id = dummy_broker.place_limit_order("AAPL", 10, 250, "buy")
    assert order_id in dummy_broker.order

def test_place_limit_order_different_prices(dummy_broker):
    order_id1 = dummy_broker.place_limit_order("AAPL", 10, 300, "buy")
    order_id2 = dummy_broker.place_limit_order("AAPL", 10, 250, "buy")
    assert order_id1 != order_id2

def test_place_limit_order_pending_or_complete(dummy_broker):
    order_id = dummy_broker.place_limit_order("AAPL", 10, 250, "buy")
    assert dummy_broker.order[order_id] in ["pending", "complete"]


def test_place_limit_order_increments_number(dummy_broker):
    dummy_broker.place_limit_order("AAPL", 10, 250, "buy")
    assert dummy_broker.number == 1

# Tests for get_order_status
def test_get_order_status_pending(dummy_broker):
    order_id = dummy_broker.place_market_order("AAPL", 10, "buy")
    dummy_broker.order[order_id] = "pending"
    assert dummy_broker.get_order_status(order_id) in ["cancel", "pending", "complete"]

def test_get_order_status_complete(dummy_broker):
    order_id = dummy_broker.place_market_order("AAPL", 10, "buy")
    dummy_broker.order[order_id] = "complete"
    assert dummy_broker.get_order_status(order_id) == "complete"

def test_get_order_status_invalid_order(dummy_broker):
    assert dummy_broker.get_order_status("nonexistent") == "invalid"

# Tests for amend_order
def test_amend_order_pending(dummy_broker):
    order_id = dummy_broker.place_limit_order("AAPL", 10, 300, "buy")
    dummy_broker.order[order_id] = "pending"
    assert dummy_broker.amend_order(order_id, 310) is True

def test_amend_order_not_pending(dummy_broker):
    order_id = dummy_broker.place_limit_order("AAPL", 10, 300, "buy")
    dummy_broker.order[order_id] = "complete"
    assert dummy_broker.amend_order(order_id, 310) is False

def test_amend_order_invalid_order(dummy_broker):
    assert dummy_broker.amend_order("nonexistent", 310) is False


# Tests for cancel_order
def test_cancel_order_pending(dummy_broker):
    order_id = dummy_broker.place_market_order("AAPL", 10, "buy")
    dummy_broker.order[order_id] = "pending"
    assert dummy_broker.cancel_order(order_id) is True

def test_cancel_order_not_pending(dummy_broker):
    order_id = dummy_broker.place_market_order("AAPL", 10, "buy")
    dummy_broker.order[order_id] = "complete"
    assert dummy_broker.cancel_order(order_id) is False

def test_cancel_order_invalid_order(dummy_broker):
    assert dummy_broker.cancel_order("nonexistent") is False

def test_cancel_order_changes_status(dummy_broker):
    order_id = dummy_broker.place_market_order("AAPL", 10, "buy")
    dummy_broker.order[order_id] = "pending"
    dummy_broker.cancel_order(order_id)
    assert dummy_broker.order[order_id] == "cancel"

# Composite scenarios
def test_composite_market_and_limit_orders(dummy_broker):
    order_id1 = dummy_broker.place_market_order("AAPL", 10, "buy")
    order_id2 = dummy_broker.place_limit_order("AAPL", 10, 300, "sell")
    assert order_id1 in dummy_broker.order and order_id2 in dummy_broker.order

def test_composite_order_status_amend(dummy_broker):
    order_id = dummy_broker.place_limit_order("AAPL", 10, 300, "buy")
    dummy_broker.order[order_id] = "pending"
    assert dummy_broker.get_order_status(order_id) in ["cancel", "pending", "complete"]
    if dummy_broker.order[order_id] == "pending":       
        assert dummy_broker.amend_order(order_id, 310) is True

def test_composite_cancel_then_amend(dummy_broker):
    order_id = dummy_broker.place_limit_order("AAPL", 10, 300, "buy")
    dummy_broker.order[order_id] = "pending"
    assert dummy_broker.cancel_order(order_id) is True
    assert dummy_broker.amend_order(order_id, 310) is False

def test_composite_multiple_orders(dummy_broker):
    order_ids = [dummy_broker.place_market_order("AAPL", i, "buy") for i in range(3)]
    assert all(order_id in dummy_broker.order for order_id in order_ids)

def test_composite_order_book(dummy_broker):
    buy_orders, sell_orders = dummy_broker.get_order_book("AAPL")
    assert buy_orders and sell_orders
    assert all(isinstance(price, float) and isinstance(quantity, int) for price, quantity in buy_orders)



# Tests for get_order_book
def test_get_order_book_returns_two_lists(dummy_broker):
    buy_orders, sell_orders = dummy_broker.get_order_book("AAPL")
    assert isinstance(buy_orders, list)
    assert isinstance(sell_orders, list)

def test_get_order_book_buy_orders_sorted(dummy_broker):
    buy_orders, _ = dummy_broker.get_order_book("AAPL")
    assert all(buy_orders[i][0] >= buy_orders[i + 1][0] for i in range(len(buy_orders) - 1))

def test_get_order_book_sell_orders_sorted(dummy_broker):
    _, sell_orders = dummy_broker.get_order_book("AAPL")
    assert all(sell_orders[i][0] <= sell_orders[i + 1][0] for i in range(len(sell_orders) - 1))

def test_get_order_book_price_format(dummy_broker):
    buy_orders, sell_orders = dummy_broker.get_order_book("AAPL")
    all_prices = [price for price, _ in buy_orders + sell_orders]
    assert all(isinstance(price, float) and 100 <= price <= 1000 for price in all_prices)

def test_get_order_book_quantity_format(dummy_broker):
    buy_orders, sell_orders = dummy_broker.get_order_book("AAPL")
    all_quantities = [quantity for _, quantity in buy_orders + sell_orders]
    assert all(isinstance(quantity, int) and 1 <= quantity <= 100 for quantity in all_quantities)