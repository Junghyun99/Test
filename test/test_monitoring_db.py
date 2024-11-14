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
    query = '''INSERT INTO monitoring(stock_name, code, country_code, trade_round, price, buy_rate, sell_rate) 
               VALUES (?, ?, ?, ?, ?, ?, ?)'''
    data = ('aaple', 'AAPL', 'US', 1, 150.0, 5, 3)
    moni_db.insert_data(query, data)
    result = moni_db.read_data("SELECT * FROM history WHERE code=?", ('AAPL',))
    assert result[0][2] == 'AAPL'

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


@pytest.fixture
def sample_data(stock_db):
    # 각 국가별 거래 내역 10개씩 생성
    kr_transactions = [
        ('삼성전자', '005390', 'TX_KR_1', 'KR', 1, 'buy', 60000, 5, 'processing', 0,  '2024-09-01'),
        ('삼성전자', '005390', 'TX_KR_2', 'KR', 2, 'buy', 55000, 5, 'completed', 3,  '2024-09-02'),
        ('삼성전자', '005390', 'TX_KR_3', 'KR', 2, 'sell', 58000, 5, 'completed', 2, '2024-09-03'),
        ('현대차', '005830', 'TX_KR_4', 'KR', 1, 'buy', 240000, 5, 'processing', 0, '2024-09-04'),
        ('네이버', '002380', 'TX_KR_5', 'KR', 1, 'buy', 6000, 10, 'completed', 8,  '2024-09-05'),
        ('카카오', '005530', 'TX_KR_6', 'KR', 1, 'buy', 120000, 3, 'processing', 0, '2024-09-06'),
        ('삼성전자', '005390', 'TX_KR_7', 'KR', 2, 'buy', 55000, 5, 'processing', 0, '2024-09-07'),
        ('네이버', '002380', 'TX_KR_8', 'KR', 1, 'sell', 8000, 10, 'completed', 5, '2024-09-08'),
        ('삼성전자', '005390', 'TX_KR_9', 'KR', 3, 'buy', 40000, 5, 'processing', 0, '2024-09-09'),
        ('네이버', '002380', 'TX_KR_10', 'KR', 1, 'buy', 6200, 5, 'processing', 0,  '2024-09-10')
    ]
    us_transactions = [
        ('apple', 'AAPL', 'TX_US_1', 'US', 1, 'buy', 180.4, 5, 'processing', 0,  '2024-10-01'),
        ('amazon', 'AMZN', 'TX_US_2', 'US', 1, 'buy', 432.1, 8, 'completed', 17,  '2024-10-02'),
        ('tesla', 'TSLA', 'TX_US_3', 'US', 1, 'buy', 300.8, 2, 'processing', 0,  '2024-10-03'),
        ('apple', 'AAPL', 'TX_US_4', 'US', 2, 'buy', 110.5, 5, 'completed', 15,  '2024-10-04'),
        ('apple', 'AAPL', 'TX_US_5', 'US', 2, 'sell', 150, 5, 'completed', 14, '2024-10-05'),
        ('apple', 'AAPL', 'TX_US_6', 'US', 2, 'buy', 110.7, 5, 'completed', 18,  '2024-10-06'),
        ('amazon', 'AMZN', 'TX_US_7', 'US', 1, 'sell', 501.3, 8, 'completed', 12, '2024-10-07'),
        ('apple', 'AAPL', 'TX_US_8', 'US', 2, 'sell', 150.7, 5, 'completed', 16,  '2024-10-08'),
        ('apple', 'AAPL', 'TX_US_9', 'US', 2, 'buy', 120.6, 5, 'processing', 0,  '2024-10-09'),
        ('apple', 'AAPL', 'TX_US_10', 'US', 3, 'buy', 90, 5, 'processing', 0,  '2024-10-10')
    ]                 

    for data in kr_transactions + us_transactions:
        stock_db.insert_data(
            '''INSERT INTO history (stock_name, code, transaction_id, country_code, trade_round, trade_type, price, amount, status, timestamp) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            data
        )

# 국가 코드별 데이터 검색 테스트
def test_read_data_by_country_code_kr(stock_db,sample_data):
    result = stock_db.read_data("SELECT * FROM history WHERE country_code=?", ('KR',))
    assert len(result) == 10
    for entry in result:
        assert entry[4] == 'KR'

def test_read_data_by_country_code_us(stock_db,sample_data):
    result = stock_db.read_data("SELECT * FROM history WHERE country_code=?", ('US',))
    assert len(result) == 10
    for entry in result:
        assert entry[4] == 'US'

# 거래 상태에 따른 데이터 검색 테스트
def test_read_data_by_status_completed(stock_db,sample_data):
    result = stock_db.read_data("SELECT * FROM history WHERE status=?", ('completed',))
    assert len(result) == 10  # 일부 데이터는 'completed' 상태
    for entry in result:
        assert entry[10] == 'completed'

def test_read_data_by_status_processing(stock_db,sample_data):
    result = stock_db.read_data("SELECT * FROM history WHERE status=?", ('processing',))
    assert len(result) == 10  # 일부 데이터는 'processing' 상태
    for entry in result:
        assert entry[10] == 'processing'

# 거래 유형별 데이터 검색 테스트
def test_read_data_by_trade_type_buy(stock_db,sample_data):
    result = stock_db.read_data("SELECT * FROM history WHERE trade_type=?", ('buy',))
    assert len(result) == 15  # 일부 데이터는 'buy' 유형
    for entry in result:
        assert entry[6] == 'buy'

def test_read_data_by_trade_type_sell(stock_db,sample_data):
    result = stock_db.read_data("SELECT * FROM history WHERE trade_type=?", ('sell',))
    assert len(result) == 5  # 일부 데이터는 'sell' 유형
    for entry in result:
        assert entry[6] == 'sell'

# 복합 조건 검색 테스트
def test_read_data_by_country_and_status(stock_db,sample_data):
    result = stock_db.read_data("SELECT * FROM history WHERE country_code=? AND status=?", ('KR', 'completed'))
    assert len(result) == 4
    assert len(result) % 2 == 0
    for entry in result:
        assert entry[4] == 'KR'
        assert entry[10] == 'completed'

def test_read_data_by_code(stock_db,sample_data):
    result = stock_db.read_data("SELECT * FROM history WHERE code=?", ('AAPL',))
    assert len(result) == 7
    for entry in result:
        assert entry[2] == 'AAPL' #all stack

def test_read_data_by_code_processing(stock_db,sample_data):
    result = stock_db.read_data("SELECT * FROM history WHERE code=? AND status=?", ('TSLA', 'processing'))
    assert len(result) == 0
    result = stock_db.read_data("SELECT * FROM history WHERE code=? AND status=?", ('005390', 'processing'))
    assert len(result) == 3 # processing stack



# 예시 데이터에 날짜도 넣어서 시간 조건검색도 테스트
def test_read_data_by_time_status(stock_db,sample_data):
    result = stock_db.read_data("SELECT * FROM history WHERE strftime('%Y', timestamp) =? AND status=?", ('2024','completed'))
    assert len(result) == 10

    result = stock_db.read_data("SELECT * FROM history WHERE strftime('%Y-%m', timestamp) =? AND status=?", ('2024-10','completed'))
    assert len(result) == 6

    result = stock_db.read_data("SELECT * FROM history WHERE date(timestamp) BETWEEN ? And ? AND status=?", ('2024-09-06','2024-10-05', 'completed'))
    assert len(result) == 4


# complete 검색은 매도 기준, pair id 활용
def test_read_data_by_time_completed(stock_db,sample_data):
    result = stock_db.read_data("SELECT * FROM history WHERE date(timestamp) BETWEEN ? And ? AND status=? And trade_type=?", ('2024-09-05''2024-10-5','completed','sell'))
    assert len(result) == 2
    assert result[0][0] == 8
    assert result[0][6] == 'sell'
    assert result[0][10] == 5 #pair
    assert result[1][0] == 15
    assert result[1][6] == 'sell'
    assert result[1][10] == 14 #pair

    pair_result = stock_db.read_data("SELECT * FROM history WHERE id= IN (?, ?)", (5, 14))
    assert len(result) == 2
    assert result[0][0] == 5
    assert result[0][6] == 'buy'
    assert result[0][10] == 8 #pair
    assert result[1][0] == 14
    assert result[1][6] == 'buy'
    assert result[1][10] == 15 #pair