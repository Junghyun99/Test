#not check
import pytest
from main import initialize_traders

def test_initialize_traders():
    traders = initialize_traders(["Samsung", "LG"])
    assert len(traders) == 2
    assert traders[0].stock_name == "Samsung"
    assert traders[1].stock_name == "LG" 