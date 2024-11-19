#not check
import pytest
from src.service.repository.monitoring_db import MonitoringDB
from src.service.monitoring_manager import MonitoringManager

@pytest.fixture
def setup_manager(mocker):
    mock_algorithm = mocker.Mock()  # pytest-mock의 mocker를 사용하여 Mock 객체 생성
    mock_db = mocker.Mock(spec=MonitoringDB)
    manager = MonitoringManager(mock_algorithm)
    manager.db = mock_db
    return manager

def test_read_all_stocks_empty_db(setup_manager):
    setup_manager.db.read_data.return_value = []  # 빈 DB를 모킹
    result = setup_manager.read_all_stocks("KR")
    assert result == []


def test_read_all_stocks_empty_db(setup_manager):
    setup_manager.db.read_data.return_value = []  # Mock an empty DB
    result = setup_manager.read_all_stocks("KR")
    assert result == []

def test_read_all_stocks_with_data(setup_manager):
    mock_data = [
        (1, "Samsung", "005930", "KR", 1, 70000, 5, 10),
        (2, "Hyundai", "005380", "KR", 2, 180000, 4, 8)
    ]
    setup_manager.db.read_data.return_value = mock_data
    result = setup_manager.read_all_stocks("KR")
    assert len(result) == 2
    assert result[0][1] == "Samsung"

def test_read_all_stocks_wrong_country_code(setup_manager):
    setup_manager.db.read_data.return_value = []  # Mock an empty DB for a different country code
    result = setup_manager.read_all_stocks("US")
    assert result == []

def test_read_all_stocks_partial_data(setup_manager):
    mock_data = [(1, "Samsung", "005930", "KR", 1, 70000, 5, 10)]
    setup_manager.db.read_data.return_value = mock_data
    result = setup_manager.read_all_stocks("KR")
    assert len(result) == 1
    assert result[0][1] == "Samsung"

def test_read_all_stocks_invalid_query(setup_manager):
    setup_manager.db.read_data.side_effect = Exception("DB Error")
    with pytest.raises(Exception, match="DB Error"):
        setup_manager.read_all_stocks("KR")



def test_add_stock_successful(setup_manager):
    setup_manager.db.insert_data.return_value = None  # Mock a successful insert
    setup_manager.add_stock_in_monitoring("Samsung", "005930", "KR", 1, 70000, 5, 10)
    setup_manager.db.insert_data.assert_called_once()

def test_add_stock_missing_data(setup_manager):
    setup_manager.db.insert_data.side_effect = Exception("Missing Data")
    with pytest.raises(Exception, match="Missing Data"):
        setup_manager.add_stock_in_monitoring("Samsung", "005930", "KR", None, 70000, 5, 10)

def test_add_stock_duplicate_entry(setup_manager):
    setup_manager.db.insert_data.side_effect = Exception("Duplicate Entry")
    with pytest.raises(Exception, match="Duplicate Entry"):
        setup_manager.add_stock_in_monitoring("Samsung", "005930", "KR", 1, 70000, 5, 10)

def test_add_stock_invalid_query(setup_manager):
    setup_manager.db.insert_data.side_effect = Exception("Invalid Query")
    with pytest.raises(Exception, match="Invalid Query"):
        setup_manager.add_stock_in_monitoring("Samsung", "INVALID_CODE", "KR", 1, 70000, 5, 10)

def test_add_stock_with_special_characters(setup_manager):
    setup_manager.db.insert_data.return_value = None
    setup_manager.add_stock_in_monitoring("Special$Char", "005930$", "KR", 1, 70000, 5, 10)
    setup_manager.db.insert_data.assert_called_once()


def test_delete_stock_successful(setup_manager):
    setup_manager.db.delete_data.return_value = None
    setup_manager.delete_stock_in_monitoring("005930")
    setup_manager.db.delete_data.assert_called_once()

def test_delete_stock_not_found(setup_manager):
    setup_manager.db.delete_data.return_value = None
    setup_manager.delete_stock_in_monitoring("INVALID_CODE")
    setup_manager.db.delete_data.assert_called_once()

def test_delete_stock_invalid_query(setup_manager):
    setup_manager.db.delete_data.side_effect = Exception("Invalid Query")
    with pytest.raises(Exception, match="Invalid Query"):
        setup_manager.delete_stock_in_monitoring("INVALID_CODE")

def test_delete_stock_empty_code(setup_manager):
    with pytest.raises(ValueError):
        setup_manager.delete_stock_in_monitoring("")

def test_delete_stock_sql_injection(setup_manager):
    setup_manager.db.delete_data.side_effect = Exception("SQL Injection Detected")
    with pytest.raises(Exception, match="SQL Injection Detected"):
        setup_manager.delete_stock_in_monitoring("005930; DROP TABLE monitoring")


def test_start_monitoring_successful(setup_manager):
    setup_manager.read_all_stocks = Mock(return_value=[(1, "Samsung", "005930", "KR", 1, 70000, 5, 10)])
    setup_manager.algorithm.fetch_func = Mock(return_value="Success")
    setup_manager.start_monitoring()
    setup_manager.algorithm.fetch_func.assert_called_once()

def test_start_monitoring_no_stocks(setup_manager):
    setup_manager.read_all_stocks.return_value = []
    setup_manager.start_monitoring()
    assert setup_manager.algorithm.fetch_func.call_count == 0

def test_start_monitoring_exception_in_thread(setup_manager):
    setup_manager.read_all_stocks.return_value = [(1, "Samsung", "005930", "KR", 1, 70000, 5, 10)]
    setup_manager.algorithm.fetch_func.side_effect = Exception("Fetch Error")
    with pytest.raises(Exception, match="Fetch Error"):
        setup_manager.start_monitoring()

def test_start_monitoring_partial_success(setup_manager):
    setup_manager.read_all_stocks.return_value = [
        (1, "Samsung", "005930", "KR", 1, 70000, 5, 10),
        (2, "Hyundai", "005380", "KR", 2, 180000, 4, 8)
    ]
    setup_manager.algorithm.fetch_func.side_effect = [Exception("Fetch Error"), "Success"]
    setup_manager.start_monitoring()
    assert setup_manager.algorithm.fetch_func.call_count == 2

def test_start_monitoring_with_os_cpu_count(setup_manager):
    import os
    max_core = os.cpu_count() - 1
    setup_manager.read_all_stocks.return_value = [
        (1, "Samsung", "005930", "KR", 1, 70000, 5, 10)
    ]
    setup_manager.start_monitoring()
    setup_manager.algorithm.fetch_func.assert_called_once()