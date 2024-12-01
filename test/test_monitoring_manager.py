#not check
import pytest
from src.service.repository.monitoring_db import MonitoringDB
from src.service.algorithm.magicsplit_algorithm import MagicSplit
from src.service.repository.monitoring_manager import MonitoringManager
from src.model.monitoring_db_model import MonitoringData

from src.util.enums import QueryOp, CountryCode

@pytest.fixture
def setup_manager(mocker):
    mock_algorithm = mocker.Mock(spec=MagicSplit)
    mock_db = mocker.Mock(spec=MonitoringDB)
    manager = MonitoringManager(mock_algorithm)
    manager.db = mock_db
    return manager, mock_algorithm, mock_db


def test_read_all_stocks_empty_db(setup_manager):
    manager, _, mock_db = setup_manager
    mock_db.read_data.return_value = []  # 빈 DB를 모킹
    result = manager.read_all_stocks(CountryCode.KR.value)
    assert result == []

def test_read_all_stocks_with_data(setup_manager):
    mock_data = [
        ("Samsung", "005930", "KR", 1, 70000, 20, 5, 10),
        ("Hyundai", "005380", "KR", 2, 180000, 6, 4, 8)
    ]
    manager, _, mock_db = setup_manager
    mock_db.read_data.return_value = mock_data
    result = manager.read_all_stocks(CountryCode.KR.value)
    assert len(result) == 2
    assert result[0][0] == "Samsung"

def test_read_all_stocks_wrong_country_code(setup_manager): 
    manager, _, mock_db = setup_manager
    mock_db.read_data.side_effect = Exception("DB error")
    with pytest.raises(Exception):
        manager.read_all_stocks(None)

def test_read_all_stocks_db_call(setup_manager):
    manager, _, mock_db = setup_manager 
    manager.read_all_stocks(CountryCode.KR.value)
    mock_db.read_data.assert_called_once_with("SELECT * FROM monitoring WHERE country_code=?", ("KR",))

def test_read_all_stocks_exception(setup_manager):
    manager, _, mock_db = setup_manager
    mock_db.read_data.side_effect = Exception("DB error")
    with pytest.raises(Exception):
        manager.read_all_stocks(CountryCode.KR.value)

def test_add_stock_successful(setup_manager):
    manager, _, mock_db = setup_manager
    mock_db.insert_data.return_value = None
    manager.add_stock_in_monitoring("StockA", "123", "KR", 1, 1000, 10, 0.5, 1.5)
    mock_db.insert_data.assert_called_once()
    
def test_add_stock_missing_data(setup_manager):
    manager, _, mock_db = setup_manager
    with pytest.raises(TypeError):
        manager.add_stock_in_monitoring("StockA", "123", "KR", 1, 1000)

def test_add_stock_invalid_query(setup_manager):
    manager, _, mock_db = setup_manager
    mock_db.insert_data.side_effect = Exception("sqlite3.IntegrityError")
    with pytest.raises(Exception):
        manager.add_stock_in_monitoring("StockA", 123, "KR", "invalid", 1000, 10, 0.5, "invalid")

def test_add_stock_Exception(setup_manager):
    manager, _, mock_db = setup_manager
    mock_db.insert_data.side_effect = Exception("DB Error")
    with pytest.raises(Exception):
        manager.add_stock_in_monitoring("StockA", "123", "KR", 1, 1000, 10, 0.5, 1.5)

def test_add_stock_duplicate_entry(setup_manager):
    manager, _, mock_db = setup_manager
    manager.add_stock_in_monitoring("StockA", "123", "KR", 1, 1000, 10, 0.5, 1.5)
    mock_db.insert_data.side_effect = Exception("Unique constraint failed")
    with pytest.raises(Exception):
        manager.add_stock_in_monitoring("StockA", "123", "KR", 1, 1000, 10, 0.5, 1.5)

def test_add_stock_with_special_characters(setup_manager):
    manager, _, mock_db = setup_manager
    mock_db.insert_data.return_value = None
    manager.add_stock_in_monitoring("Special$Char", "005930$", "KR", 1, 70000, 10, 5, 10)
    mock_db.insert_data.assert_called_once()


def test_delete_stock_successful(setup_manager):
    manager, _, mock_db = setup_manager
    manager.delete_stock_in_monitoring("123")
    mock_db.delete_data.assert_called_once_with("DELETE FROM monitoring WHERE code = ?", ("123",))


def test_delete_stock_not_found(setup_manager):
    manager, _, mock_db = setup_manager
    mock_db.delete_data.return_value = None
    manager.delete_stock_in_monitoring("999")
    mock_db.delete_data.assert_called_once()

def test_delete_stock_None(setup_manager):
    manager, _, mock_db = setup_manager
    mock_db.delete_data.side_effect = Exception("unsupported type")
    with pytest.raises(Exception):
        manager.delete_stock_in_monitoring(None)

def test_delete_stock_Invalid_Type(setup_manager):
    manager, _, mock_db = setup_manager
    mock_db.delete_data.return_value = None
    manager.delete_stock_in_monitoring(123)
    mock_db.delete_data.assert_called_once()

def test_delete_stock_empty_code(setup_manager):
    manager, _, mock_db = setup_manager
    with pytest.raises(AttributeError):
        setup_manager.delete_stock_in_monitoring()

def test_delete_stock_sql_injection(setup_manager):
    manager, _, mock_db = setup_manager
    mock_db.delete_data.return_value = None
    manager.delete_stock_in_monitoring("005930; DROP TABLE monitoring")


def test_update_stock_normal(setup_manager):
    manager, _, mock_db = setup_manager
    manager.update_stock_in_monitoring("StockA", "123", "KR", 1, 1000, 10, 0.5, 1.5)
    mock_db.update_data.assert_called_once_with(
        '''UPDATE INTO monitoring SET trade_round =?, price=?, quantity=?, buy_rate=?, sell_rate=? WHERE code = ?''',
        (1, 1000, 10, 0.5, 1.5, "123")
    )

def test_update_stock_invalid_entry(setup_manager):
    manager, _, mock_db = setup_manager
    with pytest.raises(TypeError):
        manager.update_stock_in_monitoring("StockA", "123", "KR", 1)

def test_update_stock_invalid_data(setup_manager):
    manager, _, mock_db = setup_manager
    mock_db.update_data.return_value = None
    manager.update_stock_in_monitoring("StockA", 123, "KR", "invalid", 1000, 10, 0.5, "invalid")

def test_update_stock_in_monitoring(setup_manager):
    manager, _, mock_db = setup_manager
    mock_db.update_data.return_value = None
    manager.update_stock_in_monitoring("StockB", "999", "KR", 2, 2000, 10, 0.6, 1.6)


def test_start_monitoring_successful(setup_manager, mocker):
    setup_manager.read_all_stocks = mocker.Mock(return_value=[(1, "Samsung", "005930", "KR", 1, 70000, 5, 10)])
    setup_manager.algorithm.fetch_func = mocker.Mock(return_value="Success")
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





# 5. start_monitoring 테스트
def test_start_monitoring(setup_manager, mocker):
    manager, mock_algorithm, mock_db = setup_manager

    # 가짜 데이터 생성
    mock_db.read_data.return_value = [
        ("StockA", "123", "KR", 1, 1000, 10, 0.5, 1.5),
        ("StockB", "456", "KR", 2, 2000, 10, 0.6, 1.6)
    ]

    mock_algorithm.run_algorithm.side_effect = [
        mocker.Mock(QueryOp=QueryOp.UPDATE, MonitoringData=MonitoringData("StockA", "123", "KR", 1, 1000, 10, 0.5, 1.5)),
        mocker.Mock(QueryOp=QueryOp.DELETE, MonitoringData=MonitoringData("StockB", "456", "KR", 2, 2000, 10, 0.6, 1.6)),
    ]

    # 1. 정상 작동 확인
    manager.start_monitoring()
    mock_algorithm.run_algorithm.assert_called()
    mock_db.update_data.assert_called()
    mock_db.delete_data.assert_called()

    # 2. 빈 데이터 처리
    mock_db.read_data.return_value = []
    manager.start_monitoring()
    mock_algorithm.run_algorithm.assert_not_called()

    # 3. 알고리즘 예외 발생
    mock_algorithm.run_algorithm.side_effect = Exception("Algorithm error")
    with pytest.raises(Exception):
        manager.start_monitoring()

    # 4. 쓰레드 풀 동작 확인
    mocker.patch("os.cpu_count", return_value=4)
    manager.start_monitoring()

    # 5. DB 연산 실패 시 처리
    mock_db.delete_data.side_effect = Exception("DB Error")
    with pytest.raises(Exception):
        manager.start_monitoring()