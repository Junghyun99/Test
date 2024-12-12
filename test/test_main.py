import pytest
from src.main import MainApp
from src.util.enums import CountryCode
from src.service.repository.trade_db_manager import TradeDBManager
from src.service.repository.monitoring_manager import MonitoringManager

from src.service.algorithm.magicsplit_algorithm import MagicSplit
from src.service.broker.broker_manager import BrokerManager
from src.service.yaml.yaml_manager import YamlKrManager 

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

    # YamlKrManager에 대한 Mock 객체 생성
    mock_kr_manager = mocker.Mock(spec=YamlKrManager)
    
    # MainApp.get_yaml_manager에서 Mock 객체를 반환하도록 설정
    mocker.patch("src.service.yaml.yaml_manager.YamlKrManager", return_value=mock_kr_manager)

    # MainApp 객체 생성 및 메서드 호출
    app = MainApp()
    yaml_manager = app.get_yaml_manager()

    # YamlKrManager가 정확히 호출되었는지 확인
    assert yaml_manager == mock_kr_manager

    mock_kr_manager.assert_called_once_with()


def test_get_yaml_manager_us(mocker):
    mocker.patch("sys.argv", ["program", "US"])
    mock_us_manager = mocker.patch("src.service.yaml.yaml_manager.YamlUsManager", return_value="Mocked US YAML")
    app = MainApp()
    app.run()
    yaml_manager = app.get_yaml_manager()
    mock_us_manager.assert_called_once_with()
    assert yaml_manager == "Mocked US YAML"


def test_get_yaml_manager_invalid_country(mocker):
    mocker.patch("sys.argv", ["program", "INVALID"])
    with pytest.raises(SystemExit):
        app = MainApp()
        app.run()
        app.get_yaml_manager()


# === Test for `get_monitoring_manager` ===
def test_get_monitoring_manager_kr(mocker):
    mocker.patch("sys.argv", ["program", "KR"])    
    mock_monitor_manager = mocker.patch(
        "src.service.repository.monitoring_manager.MonitoringKRManager", return_value="Mocked KR Monitor"
    )
    app = MainApp()
    app.run()
    monitor_manager = app.get_monitoring_manager("mock_algorithm")
    mock_monitor_manager.assert_called_once_with("mock_algorithm")
    assert monitor_manager == "Mocked KR Monitor"


def test_get_monitoring_manager_us(mocker):
    mocker.patch("sys.argv", ["program", "US"])    
    mock_monitor_manager = mocker.patch(
        "src.service.repository.monitoring_manager.MonitoringUSManager", return_value="Mocked US Monitor"
    )
    app = MainApp()
    app.run()
    monitor_manager = app.get_monitoring_manager("mock_algorithm")
    mock_monitor_manager.assert_called_once_with("mock_algorithm")
    assert monitor_manager == "Mocked US Monitor"


def test_get_monitoring_manager_invalid_country(mocker):
    mocker.patch("sys.argv", ["program", "INVALID"])
    with pytest.raises(SystemExit):
        app = MainApp()
        app.run()
        app.get_monitoring_manager(None)


# === Test for `run` ===
def test_run_close_methods_called(mocker):
    mocker.patch("sys.argv", ["program", "KR"])
    mock_trade = mocker.patch("src.service.repository.trade_db_manager.TradeDBManager")
    mock_monitor = mocker.patch("src.service.repository.monitoring_manager.MonitoringKRManager")
    app = MainApp()
    app.run()
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