import pytest
from dummy_broker_api import DummyBrokerAPI

def test_buy():
    api = DummyBrokerAPI()
    transaction_id = api.buy("Samsung", 2)
    assert transaction_id is not None

def test_sell():
    api = DummyBrokerAPI()
    transaction_id = api.sell("Samsung", 2)
    assert transaction_id is not None

def test_check_transaction_status():
    api = DummyBrokerAPI()
    status = api.check_transaction_status("TX12345")
    assert status in ["completed", "pending", "cancelled"]