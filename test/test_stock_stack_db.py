#not check
import pytest
from src.service.repository.stock_stack_db import StockStackDB

def test_save_stack():
    db = StockStackDB("test.db")
    db.save_stack("Samsung", [{"price": 50000, "amount": 2}])
    result = db.load_stack("Samsung")
    assert len(result) == 1
    assert result[0]["price"] == 50000

def test_load_stack():
    db = StockStackDB("test.db")
    db.save_stack("Samsung", [{"price": 50000, "amount": 2}])
    stack = db.load_stack("Samsung")
    assert len(stack) == 1
    assert stack[0]["price"] == 50000