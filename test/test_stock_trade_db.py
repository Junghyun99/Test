import pytest
import os
import sqlite3
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

# CREATE 테스트 케이스
def test_insert_data_success(stock_db):
    query = '''INSERT INTO history (stock_name, code, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    data = ('aaple', 'AAPL', 'TX123', 'US', 1, 'buy', 150.0, 10, 'processing')
    stock_db.insert_data(query, data)
    result = stock_db.read_data("SELECT * FROM history WHERE transaction_id=?", ('TX123',))
    assert result[0][3] == 'TX123'

def test_insert_data_multiple_entries(stock_db):
    data_entries = [
        ('apple', 'APPL', 'TX124', 'US', 1, 'buy', 150.0, 10, 'completed'),
        ('microsoft', 'MSFT', 'TX125', 'US', 2, 'sell', 280.0, 5, 'processing'),
        ('google', 'GOOGL', 'TX126', 'US', 3, 'buy', 2200.0, 2, 'completed')
    ]
    for data in data_entries:
        stock_db.insert_data(
            '''INSERT INTO history (stock_name, code, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            data
        )
    result = stock_db.read_data("SELECT * FROM history")
    assert len(result) == 3

def test_insert_data_missing_field(stock_db):
    with pytest.raises(sqlite3.IntegrityError):
        stock_db.insert_data(
            '''INSERT INTO history (stock_name, transaction_id, country_code, trade_round, trade_type, price, amount) 
                VALUES (?, ?, ?, ?, ?, ?, ?)''', 
            ('apple', 'TX127', 'US', 1, 'buy', 150.0, 10)
        )

def test_insert_data_invalid_trade_type(stock_db):
    with pytest.raises(sqlite3.IntegrityError):
        stock_db.insert_data(
            '''INSERT INTO history (stock_name, code, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            ('aaple', 'AAPL', 'TX128', 'US', 1, 'hold', 150.0, 10, 'completed')
        )

def test_insert_data_negative_amount(stock_db):
    with pytest.raises(sqlite3.IntegrityError):
        stock_db.insert_data(
            '''INSERT INTO history (stock_name, code, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            ('apple', 'AAPL', 'TX129', 'US', 1, 'buy', 150.0, -10, 'completed')
        )

# READ 테스트 케이스
def test_read_data_single_entry(stock_db):
    stock_db.insert_data(
        '''INSERT INTO history (stock_name, code, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        ('aaple', 'AAPL', 'TX130', 'US', 1, 'buy', 150.0, 10, 'completed')
    )
    result = stock_db.read_data("SELECT * FROM history WHERE transaction_id=?", ('TX130',))
    assert result[0][3] == 'TX130'

def test_read_data_no_results(stock_db):
    result = stock_db.read_data("SELECT * FROM history WHERE transaction_id=?", ('INVALID',))
    assert result == []

def test_read_data_multiple_results(stock_db):
    data_entries = [
        ('aaple', 'AAPL', 'TX131', 'US', 1, 'buy', 150.0, 10, 'completed'),
        ('삼성전자', '005390', 'TX132', 'KR', 2, 'sell', 160.0, 5, 'completed'),
        ('amazon', 'AMAZ', 'TX133', 'US', 1, 'sell', 170.0, 2, 'processing')
    ]
    for data in data_entries:
        stock_db.insert_data(
            '''INSERT INTO history (stock_name, code, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            data
        )
    result = stock_db.read_data("SELECT * FROM history WHERE country_code=?", ('US',))
    assert len(result) == 2

# 복합 시나리오 테스트 케이스
def test_full_scenario(stock_db):
    # Create
    stock_db.insert_data(
        '''INSERT INTO history (stock_name, code, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        ('aaple', 'AAPL', 'TX140', 'US', 1, 'buy', 150.0, 10, 'completed')
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



import pytest
import sqlite3
from src.service.repository.stock_trade_db import StockTradeDB

@pytest.fixture
def stock_db(tmp_path):
    db_path = tmp_path / "test_StockTrade.db"
    db = StockTradeDB(str(db_path))
    
    # 각 국가별 거래 내역 10개씩 생성
    kr_transactions = [
        ('KR_STOCK_{}'.format(i), 'KR', 'TX_KR_{}'.format(i), 'KR', i, 'buy' if i % 2 == 0 else 'sell', 100 + i, 5 + i, 'completed' if i % 3 == 0 else 'processing')
        for i in range(10)
    ]
    us_transactions = [
        ('US_STOCK_{}'.format(i), 'US', 'TX_US_{}'.format(i), 'US', i, 'buy' if i % 2 == 0 else 'sell', 200 + i, 10 + i, 'completed' if i % 3 == 0 else 'processing')
        for i in range(10)
    ]
    
    for data in kr_transactions + us_transactions:
        db.create_data(
            '''INSERT INTO history (stock_name, 나라, transaction_id, country_code, trade_round, trade_type, price, amount, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            data
        )

    yield db
    db.close()

# 국가 코드별 데이터 검색 테스트
def test_read_data_by_country_code_kr(stock_db):
    result = stock_db.read_data("SELECT * FROM history WHERE country_code=?", ('KR',))
    assert len(result) == 10
    for entry in result:
        assert entry[3] == 'KR'

def test_read_data_by_country_code_us(stock_db):
    result = stock_db.read_data("SELECT * FROM history WHERE country_code=?", ('US',))
    assert len(result) == 10
    for entry in result:
        assert entry[3] == 'US'

# 거래 상태에 따른 데이터 검색 테스트
def test_read_data_by_status_completed(stock_db):
    result = stock_db.read_data("SELECT * FROM history WHERE status=?", ('completed',))
    assert len(result) > 0  # 일부 데이터는 'completed' 상태
    for entry in result:
        assert entry[9] == 'completed'

def test_read_data_by_status_processing(stock_db):
    result = stock_db.read_data("SELECT * FROM history WHERE status=?", ('processing',))
    assert len(result) > 0  # 일부 데이터는 'processing' 상태
    for entry in result:
        assert entry[9] == 'processing'

# 거래 유형별 데이터 검색 테스트
def test_read_data_by_trade_type_buy(stock_db):
    result = stock_db.read_data("SELECT * FROM history WHERE trade_type=?", ('buy',))
    assert len(result) > 0  # 일부 데이터는 'buy' 유형
    for entry in result:
        assert entry[6] == 'buy'

def test_read_data_by_trade_type_sell(stock_db):
    result = stock_db.read_data("SELECT * FROM history WHERE trade_type=?", ('sell',))
    assert len(result) > 0  # 일부 데이터는 'sell' 유형
    for entry in result:
        assert entry[6] == 'sell'

# 복합 조건 검색 테스트
def test_read_data_by_country_and_status(stock_db):
    result = stock_db.read_data("SELECT * FROM history WHERE country_code=? AND status=?", ('KR', 'completed'))
    for entry in result:
        assert entry[3] == 'KR'
        assert entry[9] == 'completed'

def test_read_data_by_trade_type_and_price_range(stock_db):
    result = stock_db.read_data("SELECT * FROM history WHERE trade_type=? AND price BETWEEN ? AND ?", ('buy', 105, 115))
    for entry in result:
        assert entry[6] == 'buy'
        assert 105 <= entry[7] <= 115

def test_read_data_by_amount_and_trade_round(stock_db):
    result = stock_db.read_data("SELECT * FROM history WHERE amount>? AND trade_round<?", (6, 5))
    for entry in result:
        assert entry[8] > 6
        assert entry[5] < 5

def test_read_data_by_country_trade_type_and_status(stock_db):
    result = stock_db.read_data("SELECT * FROM history WHERE country_code=? AND trade_type=? AND status=?", ('US', 'sell', 'processing'))
    for entry in result:
        assert entry[3] == 'US'
        assert entry[6] == 'sell'
        assert entry[9] == 'processing'

# 특정 종목 이름으로 검색 테스트
def test_read_data_by_stock_name(stock_db):
    result = stock_db.read_data("SELECT * FROM history WHERE stock_name=?", ('KR_STOCK_5',))
    assert len(result) == 1
    assert result[0][1] == 'KR_STOCK_5'