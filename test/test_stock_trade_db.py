import pytest
import os
import yaml
from src.service.repository.stock_trade_db import StockTradeDB

@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test_stock_db.db"
    yield file_path
    if file_path.exists():
        os.remove(file_path)


@pytest.fixture
def stock_db(temp_file):
    db = StockTradeDB(str(temp_file))
    yield db
    db.close()