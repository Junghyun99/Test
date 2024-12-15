import pytest
import logging
from src.main import MainApp
from src.util.enums import CountryCode
from src.service.repository.trade_db_manager import TradeDBManager
from src.service.repository.monitoring_manager import MonitoringKRManager, MonitoringUSManager 

from src.service.algorithm.magicsplit_algorithm import MagicSplit
from src.service.broker.broker_manager import BrokerManager
from src.service.algorithm.stock_round_yaml_manager import StockRoundYamlKrManager, StockRoundYamlUsManager 

from src.service.logging.logger_manager import logger_manager
system_logger = logger_manager.get_logger('SYSTEM')
transaction_logger = logger_manager.get_logger('TRANSACTION')

# === Test for `parser_argument` ===
def test_parser_argument_default(mocker):
    mocker.patch("sys.argv", ["program"])
    app = MainApp()
    assert app.args.country == "KR"


def test_parser_argument_kr(mocker):
    mocker.patch("sys.argv", ["program", "KR"])
    app = MainApp()
    assert app.args.country == "KR"


def test_parser_argument_us(mocker):
    mocker.patch("sys.argv", ["program", "US"])
    app = MainApp()
    assert app.args.country == "US"


def test_parser_argument_invalid_choice(mocker):
    mocker.patch("sys.argv", ["program", "INVALID"])
    with pytest.raises(SystemExit):
        MainApp()


def test_parser_argument_help_option(mocker):
    mocker.patch("sys.argv", ["program", "--help"])
    with pytest.raises(SystemExit):
        MainApp()  # argparse automatically exits on help


# === Test for `parse_country_code` ===
def test_parse_country_code_kr(mocker):
    mocker.patch("sys.argv", ["program", "KR"])
    app = MainApp()
    assert app.country_code == CountryCode.KR


def test_parse_country_code_us(mocker):
    mocker.patch("sys.argv", ["program", "US"])
    app = MainApp()
    assert app.country_code == CountryCode.US


def test_parse_country_code_invalid(mocker):
    mocker.patch("sys.argv", ["program", "INVALID"])
    with pytest.raises(SystemExit):
        MainApp()


def test_parse_country_code_lowercase_us(mocker):
    mocker.patch("sys.argv", ["program", "us"])
    app = MainApp()
    assert app.country_code == CountryCode.US


def test_parse_country_code_no_args(mocker):
    mocker.patch("sys.argv", ["program"])
    app = MainApp()
    assert app.country_code == CountryCode.KR


# === Test for `get_yaml_manager` ===
def test_get_yaml_manager_kr(mocker):
    # sys.argv를 KR로 설정
    mocker.patch("sys.argv", ["program", "KR"])

    # MainApp 객체 생성 및 메서드 호출
    app = MainApp()
    yaml_manager = app.get_stock_round_yaml_manager()

    # YamlKrManager가 정확히 호출되었는지 확인
    assert isinstance(yaml_manager, StockRoundYamlKrManager)


def test_get_yaml_manager_us(mocker):
    mocker.patch("sys.argv", ["program", "US"])
    
    app = MainApp()
    yaml_manager = app.get_stock_round_yaml_manager()
    assert isinstance(yaml_manager, StockRoundYamlUsManager)



def test_get_yaml_manager_invalid_country(mocker):
    mocker.patch("sys.argv", ["program", "INVALID"])
    with pytest.raises(SystemExit):
        app = MainApp()
        app.get_stock_round_yaml_manager()


# === Test for `get_monitoring_manager` ===
def test_get_monitoring_manager_kr(mocker):
    mocker.patch("sys.argv", ["program", "KR"])        
    app = MainApp()
    monitor_manager = app.get_monitoring_manager("mock_algorithm")
    assert isinstance(monitor_manager, MonitoringKRManager)


def test_get_monitoring_manager_us(mocker):
    mocker.patch("sys.argv", ["program", "US"])    
    app = MainApp()
    monitor_manager = app.get_monitoring_manager("mock_algorithm")
    assert isinstance(monitor_manager, MonitoringUSManager)


def test_get_monitoring_manager_invalid_country(mocker):
    mocker.patch("sys.argv", ["program", "INVALID"])
    with pytest.raises(SystemExit):
        app = MainApp()
        app.get_monitoring_manager(None)


# === Test for `run` ===
def test_run_close_methods_called(mocker, caplog):
    mocker.patch("sys.argv", ["program", "KR"])
       
    system_logger.get_logger().propagate = True   
    # 메서드 호출 확인
    with caplog.at_level(logging.DEBUG):
        app = MainApp()
        app.run()
                
        assert "db close" in caplog.text
            


def test_run_monitoring_started(mocker, caplog):
    mocker.patch("sys.argv", ["program", "KR"])
    system_logger.get_logger().propagate = True   
    with caplog.at_level(logging.DEBUG):
        app = MainApp()
        app.run()
                
        assert "start_monitoring" in caplog.text



def test_run_broker_manager_called(mocker, caplog):
    mocker.patch("sys.argv", ["program", "KR"])
    transaction_logger.get_logger().propagate = True   
    with caplog.at_level(logging.DEBUG):
        app = MainApp()
        app.run()
                
        assert "BrokerManager" in caplog.text


def test_run_algorithm_initialized(mocker, caplog):
    mocker.patch("sys.argv", ["program", "KR"])
    system_logger.get_logger().propagate = True   
    with caplog.at_level(logging.DEBUG):
        app = MainApp()
        app.run()
                
        assert "MagicSplit" in caplog.text


def test_run_yaml_manager_initialized(mocker, caplog):
    mocker.patch("sys.argv", ["program", "KR"])
    system_logger.get_logger().propagate = True   
    with caplog.at_level(logging.DEBUG):
        app = MainApp()
        app.run()
                
        assert "StockRoundYamlKrManager" in caplog.text