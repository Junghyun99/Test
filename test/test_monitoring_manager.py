#not check
import pytest
from src.service.repository.monitoring_db import MonitoringDB
from src.service.algorithm.magicsplit_alogrithm import MagicSplit
from src.service.monitoring_manager import MonitoringManager

from src.util.enums import QueryOp, CountryCode

@pytest.fixture
def setup_manager(mocker):
    mock_algorithm = mocker.Mock(spec=MagicSplit)
    mock_db = mocker.Mock(spec=MonitoringDB)
    manager = MonitoringManager(mock_algorithm)
    manager.db = mock_db
    return manager

def test_read_all_stocks_empty_db(setup_manager):
    setup_manager.db.read_data.return_value = []  # 빈 DB를 모킹
    result = setup_manager.read_all_stocks(CountryCode.KR.value)
    assert result == []


def test_read_all_stocks_with_data(setup_manager):
    mock_data = [
        ("Samsung", "005930", "KR", 1, 70000, 20, 5, 10),
        ("Hyundai", "005380", "KR", 2, 180000, 6, 4, 8)
    ]
    setup_manager.db.read_data.return_value = mock_data
    result = setup_manager.read_all_stocks(CountryCode.KR.value)
    assert len(result) == 2
    assert result[0][0] == "Samsung"

def test_read_all_stocks_wrong_country_code(setup_manager):
    setup_manager.db.read_data.return_value = []  # Mock an empty DB for a different country code
    result = setup_manager.read_all_stocks(CountryCode.US.value)
    assert result == []

def test_read_all_stocks_invalid_query(setup_manager):
    setup_manager.db.read_data.side_effect = Exception("DB Error")
    with pytest.raises(Exception, match="DB Error"):
        setup_manager.read_all_stocks(CountryCode.KR.value)



def test_add_stock_successful(setup_manager):
    setup_manager.db.insert_data.return_value = None  # Mock a successful insert
    setup_manager.add_stock_in_monitoring("Samsung", "005930", "KR", 1, 10, 70000, 5, 10)
    setup_manager.db.insert_data.assert_called_once()

def test_add_stock_missing_data(setup_manager):
    setup_manager.db.insert_data.side_effect = Exception("Missing Data")
    with pytest.raises(Exception, match="Missing Data"):
        setup_manager.add_stock_in_monitoring("Samsung", "005930", "KR", None, 70000, 7, 5, 10)

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




import pytest
from src.service.monitoring_manager import MonitoringManager, MonitoringKRManager
from src.model.monitoring_db_model import MonitoringData
from src.util.enums import CountryCode, QueryOp


@pytest.fixture
def setup_manager(mocker):
    mock_algorithm = mocker.Mock()  # 알고리즘 의존성 모킹
    mock_db = mocker.Mock()  # MonitoringDB 모킹
    manager = MonitoringManager(mock_algorithm)
    manager.db = mock_db  # 모킹된 DB 주입
    return manager, mock_algorithm, mock_db


# 1. read_all_stocks 테스트
def test_read_all_stocks(setup_manager):
    manager, _, mock_db = setup_manager

    # 가짜 반환값 설정
    mock_db.read_data.return_value = [("StockA", "123", "KR", 1, 1000, 0.5, 1.5)]

    # 1. 정상적으로 데이터 읽기
    result = manager.read_all_stocks(CountryCode.KR.value)
    assert len(result) == 1
    assert result[0][0] == "StockA"

    # 2. 빈 데이터 반환
    mock_db.read_data.return_value = []
    result = manager.read_all_stocks(CountryCode.KR.value)
    assert result == []

    # 3. DB 호출 확인
    manager.read_all_stocks(CountryCode.KR.value)
    mock_db.read_data.assert_called_once_with("SELECT * FROM monitoring WHERE country_code=?", ("KR",))

    # 4. 예외 처리 테스트
    mock_db.read_data.side_effect = Exception("DB error")
    with pytest.raises(Exception):
        manager.read_all_stocks(CountryCode.KR.value)

    # 5. 잘못된 국가 코드 테스트
    with pytest.raises(Exception):
        manager.read_all_stocks(None)


# 2. add_stock_in_monitoring 테스트
def test_add_stock_in_monitoring(setup_manager):
    manager, _, mock_db = setup_manager

    # 1. 정상적인 추가
    manager.add_stock_in_monitoring("StockA", "123", "KR", 1, 1000, 0.5, 1.5)
    mock_db.insert_data.assert_called_once_with(
        '''INSERT INTO monitoring (stock_name, code, country_code, trade_round, price, buy_rate, sell_rate)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
        ("StockA", "123", "KR", 1, 1000, 0.5, 1.5)
    )

    # 2. 값 누락
    with pytest.raises(TypeError):
        manager.add_stock_in_monitoring("StockA", "123", "KR", 1, 1000)

    # 3. 잘못된 데이터 유형
    with pytest.raises(Exception):
        manager.add_stock_in_monitoring("StockA", 123, "KR", "invalid", 1000, 0.5, "invalid")

    # 4. DB 오류 처리
    mock_db.insert_data.side_effect = Exception("DB Error")
    with pytest.raises(Exception):
        manager.add_stock_in_monitoring("StockA", "123", "KR", 1, 1000, 0.5, 1.5)

    # 5. 중복 데이터 테스트
    mock_db.insert_data.side_effect = Exception("Unique constraint failed")
    with pytest.raises(Exception):
        manager.add_stock_in_monitoring("StockA", "123", "KR", 1, 1000, 0.5, 1.5)


# 3. delete_stock_in_monitoring 테스트
def test_delete_stock_in_monitoring(setup_manager):
    manager, _, mock_db = setup_manager

    # 1. 정상 삭제
    manager.delete_stock_in_monitoring("123")
    mock_db.delete_data.assert_called_once_with("DELETE FROM monitoring WHERE code = ?", ("123",))

    # 2. 존재하지 않는 데이터 삭제
    mock_db.delete_data.side_effect = Exception("No such record")
    with pytest.raises(Exception):
        manager.delete_stock_in_monitoring("999")

    # 3. None 값으로 삭제 시도
    with pytest.raises(Exception):
        manager.delete_stock_in_monitoring(None)

    # 4. 잘못된 데이터 형식
    with pytest.raises(Exception):
        manager.delete_stock_in_monitoring(123)

    # 5. DB 오류 발생
    mock_db.delete_data.side_effect = Exception("DB Error")
    with pytest.raises(Exception):
        manager.delete_stock_in_monitoring("123")


# 4. update_stock_in_monitoring 테스트
def test_update_stock_in_monitoring(setup_manager):
    manager, _, mock_db = setup_manager

    # 1. 정상 업데이트
    manager.update_stock_in_monitoring("StockA", "123", "KR", 1, 1000, 0.5, 1.5)
    mock_db.insert_data.assert_called_once_with(
        '''UPDATE INTO monitoring SET trade_round =?, price=?, buy_rate=?, sell_rate=? WHERE code = ?''',
        (1, 1000, 0.5, 1.5, "123")
    )

    # 2. 값 누락
    with pytest.raises(TypeError):
        manager.update_stock_in_monitoring("StockA", "123", "KR", 1)

    # 3. 잘못된 데이터 유형
    with pytest.raises(Exception):
        manager.update_stock_in_monitoring("StockA", 123, "KR", "invalid", 1000, 0.5, "invalid")

    # 4. DB 오류 처리
    mock_db.insert_data.side_effect = Exception("DB Error")
    with pytest.raises(Exception):
        manager.update_stock_in_monitoring("StockA", "123", "KR", 1, 1000, 0.5, 1.5)

    # 5. 업데이트 대상이 없는 경우
    mock_db.insert_data.side_effect = Exception("No such record")
    with pytest.raises(Exception):
        manager.update_stock_in_monitoring("StockB", "999", "KR", 2, 2000, 0.6, 1.6)


# 5. start_monitoring 테스트
def test_start_monitoring(setup_manager, mocker):
    manager, mock_algorithm, mock_db = setup_manager

    # 가짜 데이터 생성
    mock_db.read_data.return_value = [
        ("StockA", "123", "KR", 1, 1000, 0.5, 1.5),
        ("StockB", "456", "KR", 2, 2000, 0.6, 1.6)
    ]

    mock_algorithm.run_algorithm.side_effect = [
        mocker.Mock(QueryOp=QueryOp.UPDATE, MonitoringData=MonitoringData("StockA", "123", "KR", 1, 1000, 0.5, 1.5)),
        mocker.Mock(QueryOp=QueryOp.DELETE, MonitoringData=MonitoringData("StockB", "456", "KR", 2, 2000, 0.6, 1.6)),
    ]

    # 1. 정상 작동 확인
    manager.start_monitoring()
    mock_algorithm.run_algorithm.assert_called()
    mock_db.insert_data.assert_called()
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