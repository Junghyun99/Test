import pytest
import logging
from src.main import MainApp
from src.util.enums import CountryCode
from src.service.repository.trade_db_manager import TradeDBManager
from src.service.repository.monitoring_manager import MonitoringKRManager, MonitoringUSManager 

from src.service.algorithm.magicsplit_algorithm import MagicSplit
from src.service.broker.broker_manager import BrokerManager
from src.service.algorithm.stock_round_yaml_manager import StockRoundYamlKrManager, StockRoundYamlUsManager 

# === Test for `parser_argument` ===
def test_parser_argument_default(mocker):
    mocker.patch("sys.argv", ["program","--config","test/test_config.yaml"])
    app = MainApp()
    assert app.args.country == "KR"


def test_parser_argument_kr(mocker):
    mocker.patch("sys.argv", ["program", "KR","--config","test/test_config.yaml"])
    app = MainApp()
    assert app.args.country == "KR"


def test_parser_argument_us(mocker):
    mocker.patch("sys.argv", ["program", "US","--config","test/test_config.yaml"])
    app = MainApp()
    assert app.args.country == "US"


def test_parser_argument_invalid_choice(mocker):
    mocker.patch("sys.argv", ["program", "INVALID","--config","test/test_config.yaml"])
    with pytest.raises(SystemExit):
        MainApp()


def test_parser_argument_help_option(mocker):
    mocker.patch("sys.argv", ["program", "--help"])
    with pytest.raises(SystemExit):
        MainApp()  # argparse automatically exits on help


# === Test for `parse_country_code` ===
def test_parse_country_code_kr(mocker):
    mocker.patch("sys.argv", ["program", "KR","--config","test/test_config.yaml"])
    app = MainApp()
    assert app.country_code == CountryCode.KR


def test_parse_country_code_us(mocker):
    mocker.patch("sys.argv", ["program", "US","--config","test/test_config.yaml"])
    app = MainApp()
    assert app.country_code == CountryCode.US


def test_parse_country_code_invalid(mocker):
    mocker.patch("sys.argv", ["program", "INVALID","--config","test/test_config.yaml"])
    with pytest.raises(SystemExit):
        MainApp()


def test_parse_country_code_lowercase_us(mocker):
    mocker.patch("sys.argv", ["program", "us","--config","test/test_config.yaml"])
    app = MainApp()
    assert app.country_code == CountryCode.US


def test_parse_country_code_no_args(mocker):
    mocker.patch("sys.argv", ["program","--config","test/test_config.yaml"])
    app = MainApp()
    assert app.country_code == CountryCode.KR


# === Test for `get_yaml_manager` ===
def test_get_yaml_manager_kr(mocker):
    # sys.argv를 KR로 설정
    mocker.patch("sys.argv", ["program", "KR","--config","test/test_config.yaml"])

    # MainApp 객체 생성 및 메서드 호출
    app = MainApp()
    yaml_manager = app.get_stock_round_yaml_manager(app.logger.get_logger("SYSTEM"))

    # YamlKrManager가 정확히 호출되었는지 확인
    assert isinstance(yaml_manager, StockRoundYamlKrManager)


def test_get_yaml_manager_us(mocker):
    mocker.patch("sys.argv", ["program", "US","--config","test/test_config.yaml"])
    
    app = MainApp()
    yaml_manager = app.get_stock_round_yaml_manager(app.logger.get_logger("SYSTEM"))
    assert isinstance(yaml_manager, StockRoundYamlUsManager)



def test_get_yaml_manager_invalid_country(mocker):
    mocker.patch("sys.argv", ["program", "INVALID","--config","test/test_config.yaml"])
    with pytest.raises(SystemExit):
        app = MainApp()
        app.get_stock_round_yaml_manager(app.logger.get_logger("SYSTEM"))


# === Test for `get_monitoring_manager` ===
def test_get_monitoring_manager_kr(mocker):
    mocker.patch("sys.argv", ["program", "KR","--config","test/test_config.yaml"])        
    app = MainApp()
    monitor_manager = app.get_monitoring_manager("mock_algorithm",app.logger.get_logger("SYSTEM"))
    assert isinstance(monitor_manager, MonitoringKRManager)


def test_get_monitoring_manager_us(mocker):
    mocker.patch("sys.argv", ["program", "US","--config","test/test_config.yaml"])    
    app = MainApp()
    monitor_manager = app.get_monitoring_manager("mock_algorithm",app.logger.get_logger("SYSTEM"))
    assert isinstance(monitor_manager, MonitoringUSManager)


def test_get_monitoring_manager_invalid_country(mocker):
    mocker.patch("sys.argv", ["program", "INVALID","--config","test/test_config.yaml"])
    with pytest.raises(SystemExit):
        app = MainApp()
        app.get_monitoring_manager(None,app.logger.get_logger("SYSTEM"))


# === Test for `run` ===          
def test_run_monitoring_started(mocker, caplog):
    mocker.patch("sys.argv", ["program", "KR","--config","test/test_config.yaml"])
    app = MainApp()  
    app.logger.get_logger('SYSTEM').get_logger().propagate = True 
     
    with caplog.at_level(logging.DEBUG):        
        app.run()
        app.logger.get_logger('SYSTEM').proc_log()
                
        assert "start_monitoring" in caplog.text



def test_run_broker_manager_called(mocker, caplog):
    mocker.patch("sys.argv", ["program", "KR","--config","test/test_config.yaml"])

    app = MainApp() 
    app.logger.get_logger('TRANSACTION').get_logger().propagate = True   
  
    with caplog.at_level(logging.DEBUG):        
        app.run()
        app.logger.get_logger('TRANSACTION').proc_log()
                
        assert "BrokerManager" in caplog.text


def test_run_algorithm_initialized(mocker, caplog):
    mocker.patch("sys.argv", ["program", "KR","--config","test/test_config.yaml"])
    app = MainApp()    
    app.logger.get_logger('SYSTEM').get_logger().propagate = True  
    with caplog.at_level(logging.DEBUG):
        app.run()
        app.logger.get_logger('SYSTEM').proc_log()
                
        assert "MGST" in caplog.text


def test_run_yaml_manager_initialized(mocker, caplog):
    mocker.patch("sys.argv", ["program", "KR","--config","test/test_config.yaml"])
    app = MainApp()    
    app.logger.get_logger('SYSTEM').get_logger().propagate = True  
    with caplog.at_level(logging.DEBUG):        
        app.run()
        app.logger.get_logger('SYSTEM').proc_log()
                
        assert "StockRoundYamlKrManager" in caplog.text