import pytest
import os
import yaml
from src.service.yaml import KRStockCRUD, USStockCRUD 

@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test_stocks.yaml"
    yield file_path
    if file_path.exists():
        os.remove(file_path)

@pytest.fixture
def sample_data() -> Dict:
    return {US_STOCK:
  - name: Apple
    code: AAPL
    orders:
      - order: 1
        buy_price: 150
        buy_rate: 5
        sell_rate: 3
      - order: 2
        buy_price: 155
        buy_rate: 5
        sell_rate: 3

  - name: Amazon
    code: AMZN
    orders:
      - order: 1
        buy_price: 3200
        buy_rate: 4
        sell_rate: 2
      - order: 2
        buy_price: 3300
        buy_rate: 4
        sell_rate: 2
      - order: 3
        buy_price: 3400
        buy_rate: 4
        sell_rate: 2

KR_STOCK:
  - name: 삼성전자
    code: 005930
    orders:
      - order: 1
        buy_price: 70000
        buy_rate: 6
        sell_rate: 3
      - order: 2
        buy_price: 71000
        buy_rate: 6
        sell_rate: 3
      - order: 3
        buy_price: 72000
        buy_rate: 6
        sell_rate: 3

  - name: 현대차
    code: 005380
    orders:
      - order: 1
        buy_price: 180000
        buy_rate: 5
        sell_rate: 4}

@pytest.fixture
def kr_stock_crud(temp_file):
    return KRStockCRUD(str(temp_file))

@pytest.fixture
def us_stock_crud(temp_file):
    return USStockCRUD(str(temp_file))


# --- CREATE TEST CASES ---
def test_create_kr_stock(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    data = kr_stock_crud.read()
    assert len(data) == 1
    assert data[0]["name"] == "Samsung Electronics"

def test_create_duplicate_kr_stock(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    kr_stock_crud.create(sample_data)
    data = kr_stock_crud.read()
    assert len(data) == 2  # 중복 허용 시에 대한 테스트

def test_create_empty_kr_stock(kr_stock_crud):
    kr_stock_crud.create({})
    data = kr_stock_crud.read()
    assert len(data) == 1
    assert data[0] == {}

def test_create_us_stock(us_stock_crud, sample_data):
    us_stock_crud.create(sample_data)
    data = us_stock_crud.read()
    assert len(data) == 1
    assert data[0]["name"] == "Samsung Electronics"

def test_create_multiple_stocks(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    sample_data["name"] = "LG Electronics"
    sample_data["code"] = "066570"
    kr_stock_crud.create(sample_data)
    data = kr_stock_crud.read()
    assert len(data) == 2
    assert data[1]["name"] == "LG Electronics"


# --- READ TEST CASES ---
def test_read_empty_kr_stock(kr_stock_crud):
    data = kr_stock_crud.read()
    assert data == []

def test_read_kr_stock_after_create(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    data = kr_stock_crud.read()
    assert len(data) == 1
    assert data[0]["code"] == "005930"

def test_read_specific_kr_stock(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    result = kr_stock_crud.get("KR_STOCK", "005930")
    assert result[0]["name"] == "Samsung Electronics"

def test_read_us_stock_empty(us_stock_crud):
    data = us_stock_crud.read()
    assert data == []

def test_read_multiple_us_stocks(us_stock_crud, sample_data):
    us_stock_crud.create(sample_data)
    sample_data["name"] = "Apple"
    sample_data["code"] = "AAPL"
    us_stock_crud.create(sample_data)
    data = us_stock_crud.read()
    assert len(data) == 2


# --- UPDATE TEST CASES ---
def test_update_existing_kr_stock(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    updated_data = {"name": "Samsung Electronics Modified"}
    kr_stock_crud.update("005930", updated_data)
    data = kr_stock_crud.read()
    assert data[0]["name"] == "Samsung Electronics Modified"

def test_update_non_existing_kr_stock(kr_stock_crud):
    result = kr_stock_crud.update("999999", {"name": "Non Existent"})
    assert result is False

def test_update_multiple_orders_kr_stock(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    updated_data = {
        "orders": [
            {"order": 1, "buy_price": 62000, "buy_rate": 5, "sell_rate": 3}
        ]
    }
    kr_stock_crud.update("005930", updated_data)
    data = kr_stock_crud.read()
    assert data[0]["orders"][0]["buy_price"] == 62000

def test_update_us_stock(us_stock_crud, sample_data):
    us_stock_crud.create(sample_data)
    us_stock_crud.update("005930", {"name": "Updated Stock"})
    data = us_stock_crud.read()
    assert data[0]["name"] == "Updated Stock"

def test_update_partial_data(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    kr_stock_crud.update("005930", {"name": "Partial Update"})
    data = kr_stock_crud.read()
    assert data[0]["name"] == "Partial Update"


# --- DELETE TEST CASES ---
def test_delete_existing_kr_stock(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    result = kr_stock_crud.delete("005930")
    assert result is True
    data = kr_stock_crud.read()
    assert len(data) == 0

def test_delete_non_existing_kr_stock(kr_stock_crud):
    result = kr_stock_crud.delete("999999")
    assert result is False

def test_delete_one_of_multiple_stocks(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    sample_data["code"] = "066570"
    kr_stock_crud.create(sample_data)
    kr_stock_crud.delete("066570")
    data = kr_stock_crud.read()
    assert len(data) == 1
    assert data[0]["code"] == "005930"

def test_delete_us_stock(us_stock_crud, sample_data):
    us_stock_crud.create(sample_data)
    us_stock_crud.delete("005930")
    data = us_stock_crud.read()
    assert len(data) == 0

def test_delete_all_kr_stocks(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    sample_data["code"] = "066570"
    kr_stock_crud.create(sample_data)
    kr_stock_crud.delete("005930")
    kr_stock_crud.delete("066570")
    data = kr_stock_crud.read()
    assert data == []


# --- COMPLEX TEST CASES ---
def test_complex_create_update_delete(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    sample_data["code"] = "066570"
    kr_stock_crud.create(sample_data)
    kr_stock_crud.update("005930", {"name": "Samsung Updated"})
    kr_stock_crud.delete("066570")
    data = kr_stock_crud.read()
    assert len(data) == 1
    assert data[0]["name"] == "Samsung Updated"

def test_complex_create_read_update(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    sample_data["code"] = "066570"
    kr_stock_crud.create(sample_data)
    kr_stock_crud.update("005930", {"name": "Updated Samsung"})
    data = kr_stock_crud.read()
    assert len(data) == 2
    assert data[0]["name"] == "Updated Samsung"

def test_complex_multiple_updates(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    for i in range(3):
        kr_stock_crud.update("005930", {"name": f"Samsung Updated {i}"})
    data = kr_stock_crud.read()
    assert data[0]["name"] == "Samsung Updated 2"

def test_complex_create_delete_read(kr_stock_crud, sample_data):
    kr_stock_crud.create(sample_data)
    kr_stock_crud.delete("005930")
    data = kr_stock_crud.read()
    assert len(data) == 0

def test_complex_us_stock_operations(us_stock_crud, sample_data):
    us_stock_crud.create(sample_data)
    us_stock_crud.update("005930", {"name": "Tesla Updated"})
    us_stock_crud.delete("005930")
    data = us_stock_crud.read()
    assert data == []