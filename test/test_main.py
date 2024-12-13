import pytest
from src.main import MainApp
from src.util.enums import CountryCode
from src.service.repository.trade_db_manager import TradeDBManager
from src.service.repository.monitoring_manager import MonitoringKRManager, MonitoringUSManager 

from src.service.algorithm.magicsplit_algorithm import MagicSplit
from src.service.broker.broker_manager import BrokerManager
from src.service.yaml.yaml_manager import YamlKrManager, YamlUsManager 

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
    yaml_manager = app.get_yaml_manager()

    # YamlKrManager가 정확히 호출되었는지 확인
    assert isinstance(yaml_manager, YamlKrManager)


def test_get_yaml_manager_us(mocker):
    mocker.patch("sys.argv", ["program", "US"])
    
    app = MainApp()
    yaml_manager = app.get_yaml_manager()
    assert isinstance(yaml_manager, YamlUsManager)



def test_get_yaml_manager_invalid_country(mocker):
    mocker.patch("sys.argv", ["program", "INVALID"])
    with pytest.raises(SystemExit):
        app = MainApp()
        app.get_yaml_manager()


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
def test_run_close_methods_called(mocker):
    mocker.patch("sys.argv", ["program", "KR"])
    mock_trade = mocker.patch("src.service.repository.trade_db_manager.TradeDbManager")
    mock_monitor = mocker.patch("src.service.repository.monitoring_manager.MonitoringKRManager")
    app = MainApp()
    app.run()
    print("Mock TradeDBManager instance:", mock_trade.return_value)
    print("Mock MonitoringKRManager instance:", mock_monitor.return_value)

    # 메서드 호출 확인
    assert mock_trade.call_count == 1
    assert mock_trade.return_value.close_db.call_count == 1
    assert mock_monitor.return_value.close_db.call_count == 1
 

    mock_trade.return_value.close_db.assert_called_once()
    mock_monitor.return_value.close_db.assert_called_once()


def test_run_monitoring_started(mocker):
    mocker.patch("sys.argv", ["program", "KR"])
    mock_monitor = mocker.patch("src.service.repository.monitoring_manager.MonitoringKRManager")
    app = MainApp()
    app.run()
    mock_monitor.return_value.start_monitoring.assert_called_once()


def test_run_broker_manager_called(mocker):
    mocker.patch("sys.argv", ["program", "KR"])
    mock_broker = mocker.patch("src.service.broker.broker_manager.BrokerManager")
    app = MainApp()
    app.run()
    mock_broker.assert_called_once()


def test_run_algorithm_initialized(mocker):
    mocker.patch("sys.argv", ["program", "KR"])
    mock_algo = mocker.patch("src.service.algorithm.magicsplit_algorithm.MagicSplit")
    app = MainApp()
    app.run()
    mock_algo.assert_called_once()


def test_run_yaml_manager_initialized(mocker):
    mocker.patch("sys.argv", ["program", "KR"])
    mock_yaml = mocker.patch("src.service.yaml.yaml_manager.YamlKrManager")
    app = MainApp()
    app.run()
    mock_yaml.assert_called_once()