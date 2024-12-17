import pytest
from src.service.algorithm.magicsplit_algorithm import MagicSplit
from src.service.broker.broker_manager import BrokerManager
from src.interface.stock_round_yaml import StockRoundYaml
from src.service.repository.trade_db_manager import TradeDBManager
from src.model.monitoring_db_model import AlgorithmData, MonitoringData
from src.util.enums import QueryOp, CountryCode

from src.service.logging.logger_manager import LoggerManager

@pytest.fixture
def setup_magic_split(mocker):
    """MagicSplit 객체를 초기화하고 의존성을 모킹."""
    mock_broker_manager = mocker.Mock(spec=BrokerManager)
    mock_trade_db_manager = mocker.Mock(spec=TradeDBManager)
    mock_yaml_manager = mocker.Mock(spec=StockRoundYaml)

    logger = LoggerManager("test/test_config.yaml")

    magic_split = MagicSplit(mock_broker_manager, mock_trade_db_manager, mock_yaml_manager, logger)
    return magic_split, mock_broker_manager, mock_trade_db_manager, mock_yaml_manager


# 1. _calculate_price 테스트
def test_calculate_price(setup_magic_split, mocker):
    magic_split, _, _, _ = setup_magic_split
    mocker.patch("src.util.price_calculator.PriceCalculator.calculate_price", side_effect=[90, 110])

    buy_price, sell_price = magic_split._calculate_price(100, 10, 10)
    assert buy_price == 90
    assert sell_price == 110


# 2. _get_prev_trade_round 테스트
def test_get_prev_trade_round(setup_magic_split):
    magic_split, _, mock_trade_db_manager, _ = setup_magic_split
    mock_trade_db_manager.get_trade_round.return_value = (900, 10)

    price, quantity = magic_split._get_prev_trade_round("ABC123", 3)
    assert price == 900
    assert quantity == 10
    mock_trade_db_manager.get_trade_round.assert_called_once_with("ABC123", 3)


# 3. _try_buy_stock 테스트
def test_try_buy_stock_normal(setup_magic_split, mocker):
    magic_split, mock_broker_manager, _, mock_yaml_manager = setup_magic_split

    moni_data = MonitoringData("StockA", "ABC123", CountryCode.KR, 1, 1000, 10, 0.5, 1.5)
    yaml_mock_data = [{"orders": [{"order": 1, "buy_price": 950, "buy_rate": 0.5, "sell_rate": 1.5}, {"order": 2, "buy_price": 960, "buy_rate": 0.5, "sell_rate": 1.5}]}]
    mock_yaml_manager.read_by_id.return_value = yaml_mock_data

    # 1. 정상적인 매수
    mock_broker_manager.place_market_order.return_value = (True, (960, 10))
    result = magic_split._try_buy_stock(960, moni_data)

    assert result.QueryOp == QueryOp.UPDATE
    assert result.MonitoringData.trade_round == 2
    assert result.MonitoringData.price == 960
    assert result.MonitoringData.quantity == 10

def test_try_buy_stock_fail(setup_magic_split, mocker):
    magic_split, mock_broker_manager, _, mock_yaml_manager = setup_magic_split

    moni_data = MonitoringData("StockA", "ABC123", CountryCode.KR, 1, 1000, 10, 0.5, 1.5)
    yaml_mock_data = [{"orders": [{"order": 1, "buy_price": 950, "buy_rate": 0.5, "sell_rate": 1.5}, {"order": 2, "buy_price": 960, "buy_rate": 0.5, "sell_rate": 1.5}]}]
    mock_yaml_manager.read_by_id.return_value = yaml_mock_data

    # 2. 매수 실패
    mock_broker_manager.place_market_order.return_value = (False, None)
    result = magic_split._try_buy_stock(960, moni_data)
    assert result.QueryOp == QueryOp.DEFAULT

def test_try_buy_stock_last_round(setup_magic_split, mocker):
    magic_split, mock_broker_manager, _, mock_yaml_manager = setup_magic_split

    moni_data = MonitoringData("StockA", "ABC123", CountryCode.KR, 2, 1000, 10, 0.5, 1.5)
    yaml_mock_data = [{"orders": [{"order": 1, "buy_price": 950, "buy_rate": 0.5, "sell_rate": 1.5}, {"order": 2, "buy_price": 960, "buy_rate": 0.5, "sell_rate": 1.5}]}]
    mock_yaml_manager.read_by_id.return_value = yaml_mock_data
    # 3. YAML 데이터 마지막 차수
    
    result = magic_split._try_buy_stock(960, moni_data)
    assert result.QueryOp == QueryOp.DEFAULT


# 4. _try_sell_stock 테스트
def test_try_sell_stock_normal(setup_magic_split, mocker):
    magic_split, mock_broker_manager, mock_trade_db_manager, mock_yaml_manager = setup_magic_split

    moni_data = MonitoringData("StockA", "ABC123", CountryCode.KR, 2, 1000, 10, 0.5, 1.5)
    yaml_mock_data = [{"orders": [{"order": 1, "buy_price": 950, "buy_rate": 0.5, "sell_rate": 1.5}, {"order": 2, "buy_price": 960, "buy_rate": 0.5, "sell_rate": 1.5}]}]
    mock_yaml_manager.read_by_id.return_value = yaml_mock_data
    mock_broker_manager.place_market_order.return_value = (True, None)
    mock_trade_db_manager.get_trade_round.return_value = (950, 10)

    # 1. 정상적인 매도
    result = magic_split._try_sell_stock(1100, moni_data)
    assert result.QueryOp == QueryOp.UPDATE
    assert result.MonitoringData.trade_round == 1
    assert result.MonitoringData.price == 950
    assert result.MonitoringData.quantity == 10

def test_try_sell_stock_fail(setup_magic_split, mocker):
    magic_split, mock_broker_manager, mock_trade_db_manager, mock_yaml_manager = setup_magic_split

    moni_data = MonitoringData("StockA", "ABC123", CountryCode.KR, 2, 1000, 10, 0.5, 1.5)
    yaml_mock_data = [{"orders": [{"order": 1, "buy_price": 950, "buy_rate": 0.5, "sell_rate": 1.5}, {"order": 2, "buy_price": 960, "buy_rate": 0.5, "sell_rate": 1.5}]}]
    mock_yaml_manager.read_by_id.return_value = yaml_mock_data
    mock_broker_manager.place_market_order.return_value = (True, None)
    mock_trade_db_manager.get_trade_round.return_value = (950, 10)
    # 2. 매도 실패
    mock_broker_manager.place_market_order.return_value = (False, None)
    result = magic_split._try_sell_stock(1100, moni_data)
    assert result.QueryOp == QueryOp.DEFAULT

def test_try_sell_stock_first(setup_magic_split, mocker):
    magic_split, mock_broker_manager, mock_trade_db_manager, mock_yaml_manager = setup_magic_split

    moni_data = MonitoringData("StockA", "ABC123", CountryCode.KR, 1, 1000, 10, 0.5, 1.5)
    yaml_mock_data = [{"orders": [{"order": 1, "buy_price": 950, "buy_rate": 0.5, "sell_rate": 1.5}, {"order": 2, "buy_price": 960, "buy_rate": 0.5, "sell_rate": 1.5}]}]
    mock_yaml_manager.read_by_id.return_value = yaml_mock_data
    mock_broker_manager.place_market_order.return_value = (True, None)
    mock_trade_db_manager.get_trade_round.return_value = (950, 10)
    # 3. 첫 번째 차수에서 매도 성공
    
    result = magic_split._try_sell_stock(1100, moni_data)
    assert result.QueryOp == QueryOp.DELETE


# 5. run_algorithm 테스트
def test_run_algorithm(setup_magic_split, mocker):
    magic_split, mock_broker_manager, _, _ = setup_magic_split
    moni_data = MonitoringData("StockA", "ABC123", CountryCode.KR, 1, 1000, 10, 0.5, 1.5)

    mocker.patch.object(magic_split, "_calculate_price", return_value=(950, 1100))
    mocker.patch.object(magic_split, "_try_buy_stock", return_value=AlgorithmData(QueryOp.UPDATE, moni_data))
    mocker.patch.object(magic_split, "_try_sell_stock", return_value=AlgorithmData(QueryOp.DELETE, moni_data))

    # 1. 매수 조건 만족
    mock_broker_manager.get_current_price.return_value = 940
    result = magic_split.run_algorithm(moni_data)
    assert result.QueryOp == QueryOp.UPDATE

    # 2. 매도 조건 만족
    mock_broker_manager.get_current_price.return_value = 1150
    result = magic_split.run_algorithm(moni_data)
    assert result.QueryOp == QueryOp.DELETE

    # 3. 조건 미충족
    mock_broker_manager.get_current_price.return_value = 1000
    result = magic_split.run_algorithm(moni_data)
    assert result.QueryOp == QueryOp.DEFAULT