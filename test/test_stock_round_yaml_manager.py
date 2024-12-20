import pytest
import os
import yaml

from src.service.algorithm.stock_round_yaml_manager import StockRoundYamlKrManager, StockRoundYamlUsManager

from src.service.logging.logger_manager import LoggerManager


@pytest.fixture
def temp_file():
    file_path = "test/csv/stock_round_config.yaml"

    # 초기값 설정
    initial_data = {
        "KR": [],
        "US": []
    }

    # 초기값을 test_stocks.yaml 파일에 작성
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(initial_data, file, allow_unicode=True)

    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)

@pytest.fixture
def sample_kr_data1():
    return {
        "name": "삼성전자",
            "code": "005930",
            "orders": [
                {"order": 1, "buy_price": 70000, "buy_rate": 6, "sell_rate": 3},
                {"order": 2, "buy_price": 71000, "buy_rate": 6, "sell_rate": 3},
                {"order": 3, "buy_price": 72000, "buy_rate": 6, "sell_rate": 3},
            ]
        }
@pytest.fixture
def sample_kr_data2():    
    return {
            "name": "현대차",
            "code": "005380",
            "orders": [
                {"order": 1, "buy_price": 180000, "buy_rate": 5, "sell_rate": 4},
            ]
        }
@pytest.fixture
def sample_us_data1():
    return {
        "name": "Apple",
        "code": "AAPL",
        "orders": [
            {"order": 1, "buy_price": 150,  "buy_rate": 5, "sell_rate":3},
            {"order": 2, "buy_price": 155,  "buy_rate": 5, "sell_rate":3}
        ]}
@pytest.fixture
def sample_us_data2():
    return {
        "name": "Amazon",
        "code": "AMZN",
        "orders": [
            {"order": 1, "buy_price": 3200,  "buy_rate": 4, "sell_rate":2},
            {"order": 2, "buy_price": 3300,  "buy_rate": 4, "sell_rate":2},
            {"order": 3, "buy_price": 3400, "buy_rate": 4, "sell_rate":2}
        ]}
                                                                                                                                                                                                                               
@pytest.fixture
def kr_stock_crud(temp_file):
    logger = LoggerManager("test/test_config.yaml").get_logger('SYSTEM')
    return StockRoundYamlKrManager("test/test_config.yaml", logger)

@pytest.fixture
def us_stock_crud(temp_file):
    logger = LoggerManager("test/test_config.yaml").get_logger('SYSTEM')
    return StockRoundYamlUsManager("test/test_config.yaml", logger)


# --- CREATE TEST CASES ---
def test_create_kr_stock(kr_stock_crud, sample_kr_data1,sample_kr_data2):
    kr_stock_crud.create(sample_kr_data1)
    kr_stock_crud.create(sample_kr_data2)
    data = kr_stock_crud.read_by_id("005930")
    assert len(data) == 1
    assert data[0]["name"] == "삼성전자"
    data = kr_stock_crud.read_all()
    assert len(data) == 2

def test_create_duplicate_kr_stock(kr_stock_crud, sample_kr_data1):
    with pytest.raises(Exception):
        kr_stock_crud.create(sample_kr_data1)
        kr_stock_crud.create(sample_kr_data1)
    data = kr_stock_crud.read_all()
    assert len(data) == 1  # 중복 허용 시에 대한 테스트

def test_create_empty_kr_stock(kr_stock_crud):
    kr_stock_crud.create({})
    data = kr_stock_crud.read_all()
    assert len(data) == 1
    assert data[0] == {}

def test_create_us_stock(us_stock_crud, sample_us_data1,sample_us_data2):
    us_stock_crud.create(sample_us_data1)
    us_stock_crud.create(sample_us_data2)
    data = us_stock_crud.read_by_id("AAPL")
    assert len(data) == 1
    assert data[0]["name"] == "Apple"

def test_create_multiple_stocks(kr_stock_crud, us_stock_crud, sample_kr_data1, sample_us_data1):
    kr_stock_crud.create(sample_kr_data1)
    us_stock_crud.create(sample_us_data1)
    data = kr_stock_crud.read_all()
    assert len(data) == 1
    assert data[0]["name"] == "삼성전자"


# --- READ TEST CASES ---
def test_read_empty_kr_stock(kr_stock_crud):
    data = kr_stock_crud.read_all()
    assert data == []

def test_read_kr_stock_after_create(kr_stock_crud, sample_kr_data1):
    kr_stock_crud.create(sample_kr_data1)
    data = kr_stock_crud.read_all()
    assert len(data) == 1
    assert data[0]["code"] == "005930"

def test_read_specific_kr_stock(kr_stock_crud, sample_kr_data1, sample_kr_data2):
    kr_stock_crud.create(sample_kr_data1)
    kr_stock_crud.create(sample_kr_data2)
    data = kr_stock_crud.read_by_id("005380")
    assert data[0]["name"] == "현대차"

def test_read_us_stock_empty(us_stock_crud):
    data = us_stock_crud.read_all()
    assert data == []

def test_read_multiple_us_stocks(us_stock_crud, kr_stock_crud, sample_kr_data1, sample_us_data1):
    kr_stock_crud.create(sample_kr_data1)
    us_stock_crud.create(sample_us_data1)
    data = us_stock_crud.read_all()
    assert len(data) == 1
    data = kr_stock_crud.read_all()
    assert len(data) == 1


# --- UPDATE TEST CASES ---
def test_update_existing_kr_stock(kr_stock_crud, sample_kr_data1):
    kr_stock_crud.create(sample_kr_data1)
    updated_data = {"name": "Samsung"}
    kr_stock_crud.update("005930", updated_data)
    data = kr_stock_crud.read_all()
    assert data[0]["name"] == "Samsung"

def test_update_non_existing_kr_stock(kr_stock_crud):
    with pytest.raises(Exception):
        kr_stock_crud.update("999999", {"name": "Non Existent"})
   

def test_update_multiple_orders_kr_stock(kr_stock_crud, sample_kr_data1):
    kr_stock_crud.create(sample_kr_data1)
    updated_data = {
        "orders": [
            {"order": 1, "buy_price": 62000,  "buy_rate": 5, "sell_rate": 3}
        ]
    }
    kr_stock_crud.update("005930", updated_data)
    data = kr_stock_crud.read_all()
    assert data[0]["orders"][0]["buy_price"] == 62000

def test_update_code_us_stock(us_stock_crud, sample_us_data1):
    with pytest.raises(Exception):
        us_stock_crud.create(sample_us_data1)
        us_stock_crud.update("AAPL", {"code": "AAPP"})
    data = us_stock_crud.read_all()
    assert data[0]["code"] == "AAPL"

# --- DELETE TEST CASES ---
def test_delete_existing_kr_stock(kr_stock_crud, sample_kr_data1, sample_kr_data2):
    kr_stock_crud.create(sample_kr_data1)
    kr_stock_crud.create(sample_kr_data2)
    data = kr_stock_crud.read_all()
    print("%s",data)
    assert len(data) == 2
    kr_stock_crud.delete("005380")
    data = kr_stock_crud.read_all()
    assert len(data) == 1

def test_delete_non_existing_kr_stock(kr_stock_crud):
    with pytest.raises(Exception):
        kr_stock_crud.delete("999999")
    

def test_delete_all_us_stocks(us_stock_crud, sample_us_data1, sample_us_data2):
    us_stock_crud.create(sample_us_data1)
    us_stock_crud.create(sample_us_data2)
    us_stock_crud.delete("AAPL")
    us_stock_crud.delete("AMZN")
    data = us_stock_crud.read_all()
    assert data == []


# --- COMPLEX TEST CASES ---
def test_complex_create_update_delete(kr_stock_crud, sample_kr_data1, sample_kr_data2):
    kr_stock_crud.create(sample_kr_data1)
    with pytest.raises(Exception):
        kr_stock_crud.create(sample_kr_data1)
    kr_stock_crud.create(sample_kr_data2)
    kr_stock_crud.update("005930", {"name": "Samsung"})
    kr_stock_crud.delete("005380")
    data = kr_stock_crud.read_all()
    assert len(data) == 1
    assert data[0]["name"] == "Samsung"

def test_complex_multiple_updates(kr_stock_crud, sample_kr_data1):
    kr_stock_crud.create(sample_kr_data1)
    for i in range(3):
        kr_stock_crud.update("005930", {"name": f"Samsung Updated {i}"})
    data = kr_stock_crud.read_all()
    assert data[0]["name"] == "Samsung Updated 2"

def test_complex_create_delete_read(kr_stock_crud, sample_kr_data1):
    kr_stock_crud.create(sample_kr_data1)
    kr_stock_crud.delete("005930")
    data = kr_stock_crud.read_all()
    assert len(data) == 0