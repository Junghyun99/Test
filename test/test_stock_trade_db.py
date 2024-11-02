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



@pytest.fixture
def stock_db(tmp_path):
    db_path = tmp_path / "test_StockTrade.db"
    db = StockTradeDB(str(db_path))
    yield db
    db.close()

# CREATE 테스트 케이스
def test_create_data_success(stock_db):
    query = '''INSERT INTO history (stock_name, 나라, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    data = ('AAPL', 'KR', 'TX123', 'US', 1, 'buy', 150.0, 10, 'completed')
    stock_db.create_data(query, data)
    result = stock_db.read_data("SELECT * FROM history WHERE transaction_id=?", ('TX123',))
    assert result[0][3] == 'TX123'

def test_create_data_multiple_entries(stock_db):
    data_entries = [
        ('AAPL', 'KR', 'TX124', 'US', 1, 'buy', 150.0, 10, 'completed'),
        ('MSFT', 'KR', 'TX125', 'US', 2, 'sell', 280.0, 5, 'processing'),
        ('GOOGL', 'KR', 'TX126', 'US', 3, 'buy', 2200.0, 2, 'completed')
    ]
    for data in data_entries:
        stock_db.create_data(
            '''INSERT INTO history (stock_name, 나라, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            data
        )
    result = stock_db.read_data("SELECT * FROM history")
    assert len(result) == 3

def test_create_data_missing_field(stock_db):
    with pytest.raises(sqlite3.IntegrityError):
        stock_db.create_data(
            '''INSERT INTO history (stock_name, 나라, transaction_id, country_code, trade_round, trade_type, price, amount) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
            ('AAPL', 'KR', 'TX127', 'US', 1, 'buy', 150.0, 10)
        )

def test_create_data_invalid_trade_type(stock_db):
    with pytest.raises(sqlite3.IntegrityError):
        stock_db.create_data(
            '''INSERT INTO history (stock_name, 나라, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            ('AAPL', 'KR', 'TX128', 'US', 1, 'hold', 150.0, 10, 'completed')
        )

def test_create_data_negative_amount(stock_db):
    with pytest.raises(sqlite3.IntegrityError):
        stock_db.create_data(
            '''INSERT INTO history (stock_name, 나라, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            ('AAPL', 'KR', 'TX129', 'US', 1, 'buy', 150.0, -10, 'completed')
        )

# READ 테스트 케이스
def test_read_data_single_entry(stock_db):
    stock_db.create_data(
        '''INSERT INTO history (stock_name, 나라, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        ('AAPL', 'KR', 'TX130', 'US', 1, 'buy', 150.0, 10, 'completed')
    )
    result = stock_db.read_data("SELECT * FROM history WHERE transaction_id=?", ('TX130',))
    assert result[0][3] == 'TX130'

def test_read_data_no_results(stock_db):
    result = stock_db.read_data("SELECT * FROM history WHERE transaction_id=?", ('INVALID',))
    assert result == []

def test_read_data_multiple_results(stock_db):
    data_entries = [
        ('AAPL', 'KR', 'TX131', 'US', 1, 'buy', 150.0, 10, 'completed'),
        ('AAPL', 'KR', 'TX132', 'US', 2, 'sell', 160.0, 5, 'completed')
    ]
    for data in data_entries:
        stock_db.create_data(
            '''INSERT INTO history (stock_name, 나라, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            data
        )
    result = stock_db.read_data("SELECT * FROM history WHERE stock_name=?", ('AAPL',))
    assert len(result) == 2

# 복합 시나리오 테스트 케이스
def test_full_scenario(stock_db):
    # Create
    stock_db.create_data(
        '''INSERT INTO history (stock_name, 나라, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        ('AAPL', 'KR', 'TX140', 'US', 1, 'buy', 150.0, 10, 'completed')
    )
    # Update
    stock_db.update_data(
        "UPDATE history SET amount=? WHERE transaction_id=?", 
        (20, 'TX140')
    )
    updated_data = stock_db.read_data("SELECT amount FROM history WHERE transaction_id=?", ('TX140',))
    assert updated_data[0][0] == 20

    # Read
    result = stock_db.read_data("SELECT * FROM history WHERE transaction_id=?", ('TX140',))
    assert len(result) == 1
    assert result[0][3] == 'TX140'
    assert result[0][8] == 20  # Updated amount

    # Delete
    stock_db.delete_data("DELETE FROM history WHERE transaction_id=?", ('TX140',))
    result = stock_db.read_data("SELECT * FROM history WHERE transaction_id=?", ('TX140',))
    assert result == []