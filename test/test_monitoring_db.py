import pytest
import os
import sqlite3
from src.service.repository.monitoring_db import MonitoringDB

@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test_monitoring_db.db"
    yield file_path
    if file_path.exists():
        os.remove(file_path)

@pytest.fixture
def moni_db(temp_file):
    db = MonitoringDB(str(temp_file))
    yield db
    db.close()

# CREATE 테스트 케이스
def test_insert_data_success(moni_db):
    query = '''INSERT INTO monitoring(stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    data = ('aaple', 'AAPL', 'US', 1, 150.0, 10, 5, 3)
    moni_db.insert_data(query, data)
    result = moni_db.read_data("SELECT * FROM monitoring WHERE code=?", ('AAPL',))
    assert result[0][2] == 'AAPL'

def test_insert_data_multiple_entries(moni_db):
    data_entries = [
        ('aaple', 'AAPL', 'US', 1, 150.0, 10, 5, 3),
        ('aaple', 'MSFT', 'US', 1, 150.0, 10, 5, 3)
    ]
    for data in data_entries:
        moni_db.insert_data(
            '''INSERT INTO monitoring(stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
            data
        )
    result = moni_db.read_data("SELECT * FROM monitoring")
    assert len(result) == 2 

def test_insert_data_duplicate_insert(moni_db):
    with pytest.raises(sqlite3.IntegrityError):
        moni_db.insert_data(
            '''INSERT INTO monitoring(stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
            ('apple', 'AAPL', 'US', 1, 150.0, 10, 5, 3)
        )
        moni_db.insert_data(
            '''INSERT INTO monitoring(stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
            ('apple', 'AAPL', 'US', 1, 150.0, 10, 5, 3)
        )


def test_insert_data_missing_field(moni_db):
    with pytest.raises(sqlite3.IntegrityError):
        moni_db.insert_data(
            '''INSERT INTO monitoring(stock_name, country_code, trade_round, price, quantity, buy_rate, sell_rate) 
               VALUES (?, ?, ?, ?, ?, ?, ?)''', 
            ('apple', 'US', 1, 150.0, 10, 5, 3)
        )

def test_insert_data_negative_round(moni_db):
    with pytest.raises(sqlite3.IntegrityError):
        moni_db.insert_data(
            '''INSERT INTO monitoring(stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', ('aaple', 'AAPL', 'US', -1, 150.0, 10, 5, 3)
            
        )

# READ 테스트 케이스
def test_read_data_no_results(moni_db):
    result = moni_db.read_data("SELECT * FROM monitoring WHERE code=?", ('INVALID',))
    assert result == []

def test_read_data_no_results(moni_db):
    with pytest.raises(Exception):
        moni_db.read_data("SELECT * FROM monitoring WHERE code=?", None)

def test_delete_normal(moni_db):
    moni_db.insert_data(
        '''INSERT INTO monitoring (stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        ('aaple', 'AAPL', 'US', 1, 150.0, 10, 10, 5)
    )
    moni_db.delete_data("DELETE FROM monitoring WHERE code=?",("AAPL",))   

def test_delete_not_found(moni_db):
    moni_db.delete_data("DELETE FROM monitoring WHERE code=?",("AAPL",))  

def test_delete_injection(moni_db):
    moni_db.insert_data(
        '''INSERT INTO monitoring (stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        ('aaple', 'AAPL', 'US', 1, 150.0, 10, 10, 5)
    )
    moni_db.insert_data(
        '''INSERT INTO monitoring (stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        ('aaple', 'MSFT', 'US', 1, 150.0, 10, 10, 5)
    )
    moni_db.delete_data("DELETE FROM monitoring WHERE code=?",("AAPL; DROP TABLE monitoring",))  
    result = moni_db.read_data("SELECT * FROM monitoring")
    assert len(result) == 2

def test_delete_empty(moni_db):
    with pytest.raises(Exception):
        moni_db.delete_data("DELETE FROM monitoring WHERE code=?",( ))  

def test_delete_None(moni_db):
    with pytest.raises(Exception):
        moni_db.delete_data("DELETE FROM monitoring WHERE code=?",None)  

# 복합 시나리오 테스트 케이스
def test_full_scenario(moni_db):
    # Create
    moni_db.insert_data(
        '''INSERT INTO monitoring (stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        ('aaple', 'AAPL', 'US', 1, 150.0, 10, 10, 5)
    )
    # Update
    moni_db.update_data(
        "UPDATE monitoring SET buy_rate=? WHERE code=?", 
        (15, 'AAPL')
    )
    updated_data = moni_db.read_data("SELECT buy_rate FROM monitoring WHERE code=?", ('AAPL',))
    assert updated_data[0][0] == 15

    # Read
    result = moni_db.read_data("SELECT * FROM monitoring WHERE code=?", ('AAPL',))
    assert len(result) == 1
    assert result[0][2] == 'AAPL'
    assert result[0][7] == 15  # Updated amount

    # Delete
    moni_db.delete_data("DELETE FROM monitoring WHERE code=?", ('AAPL',))
    result = moni_db.read_data("SELECT * FROM monitoring WHERE code=?", ('AAPL',))
    assert result == []


@pytest.fixture
def sample_data(moni_db):
    # 각 국가별 모니터링내역 5개씩 생성
    kr_moni = [
        ('삼성전자', '005390', 'KR', 1, 60000, 10, 5, 6),
        ('현대차', '005830', 'KR', 3, 240000, 10, 1, 10),
        ('네이버', '002380', 'KR', 1, 6000, 10, 10, 23),
        ('카카오', '005530', 'KR', 5, 120000, 10, 3, 4),
        ('하이브', '012880', 'KR', 3, 6200, 10, 14, 5)
    ]
    us_moni = [
        ('apple', 'AAPL', 'US', 1, 180.4, 10, 5, 10),
        ('amazon', 'AMZN', 'US', 2, 432.1, 10, 8, 9),
        ('tesla', 'TSLA', 'US', 5, 300.8, 10, 2, 11),
        ('micro soft', 'MSFT', 'US', 2, 150.7, 10, 10, 32),
        ('reality income', 'O', 'US', 3, 90, 10, 5, 1)
    ]                 

    for data in kr_moni + us_moni:
        moni_db.insert_data(
            '''INSERT INTO monitoring (stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
            data
        )

# 국가 코드별 데이터 검색 테스트
def test_read_data_by_country_code_kr(moni_db,sample_data):
    result = moni_db.read_data("SELECT * FROM monitoring WHERE country_code=?", ('KR',))
    assert len(result) == 5
    for entry in result:
        assert entry[3] == 'KR'

def test_read_data_by_country_code_us(moni_db,sample_data):
    result = moni_db.read_data("SELECT * FROM monitoring WHERE country_code=?", ('US',))
    assert len(result) == 5
    for entry in result:
        assert entry[3] == 'US'

# 복합 조건 검색 테스트
def test_read_data_by_country_and_trade_round(moni_db,sample_data):
    result = moni_db.read_data("SELECT * FROM monitoring WHERE country_code=? AND trade_round=?", ('KR', 3))
    assert len(result) == 2
    for entry in result:
        assert entry[3] == 'KR'
        assert entry[4] == 3

def test_read_data_by_code(moni_db,sample_data):
    result = moni_db.read_data("SELECT * FROM monitoring WHERE code=?", ('AAPL',))
    assert len(result) == 1