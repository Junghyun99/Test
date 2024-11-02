import pytest
import os
import yaml
from src.service.repository.stock_trade_db import StockTradeDB

@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test_stocks.yaml"
    yield file_path
    if file_path.exists():
        os.remove(file_path)