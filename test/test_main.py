import pytest
from src.main import MainApp
from src.util.enums import CountryCode
from src.service.repository.trade_db_manager import TradeDBManager
from src.service.repository.monitoring_manager import MonitoringManager

from src.service.algorithm.magicsplit_algorithm import MagicSplit
from src.service.broker.broker_manager import BrokerManager
from src.service.yaml.yaml_manager import YamlKrManager 


@pytest.fixture
def setup_MainApp(mocker):
    app = MainApp()
    mock_algorithm = mocker.Mock(spec=MagicSplit)
    mock_broker = mocker.Mock(spec=BrokerManager)
    mock_yaml_manager = mocker.Mock(spec=YamlKrManager)  
    mock_trade = mocker.Mock(spec=TradeDBManager)
    mock_monitoring = mocker.Mock(spec=MonitoringManager)
    return app, mock_algorithm, mock_broker, mock_yaml_manager, mock_trade, mock_monitoring


def test_parse_country_code_valid(setup_MainApp):
    """Valid country code 테스트"""
    app, _, _, _, _, _ = setup_MainApp
    assert app.parse_country_code("KR") == CountryCode.KR
    assert app.parse_country_code("US") == CountryCode.US


def test_parse_country_code_invalid(setup_MainApp):
    """Invalid country code 테스트"""
    app, _, _, _, _, _ = setup_MainApp
    assert app.parse_country_code("INVALID") is None
    assert app.parse_country_code("") is None


def test_main_default_country(setup_MainApp,mocker):
    """Default country 테스트 (KR)"""
    app, _, _, _, _, _ = setup_MainApp mocker.patch("argparse.ArgumentParser.parse_args", return_value=mocker.Mock(country="KR"))
    mock_run = mocker.patch("src.main.run")

    app.parser_argument()

    mock_run.assert_called_once_with(CountryCode.KR)


def test_main_valid_country(mocker):
    """Valid country 코드 입력 테스트"""
    mocker.patch("argparse.ArgumentParser.parse_args", return_value=mocker.Mock(country="US"))
    mock_run = mocker.patch("src.main.run")

    main()

    mock_run.assert_called_once_with(CountryCode.US)


def test_main_invalid_country(mocker, capsys):
    """Invalid country 코드 입력 테스트"""
    mocker.patch("argparse.ArgumentParser.parse_args", return_value=mocker.Mock(country="INVALID"))

    with pytest.raises(SystemExit):  # Invalid code로 인한 종료
        main()

    captured = capsys.readouterr()
    assert "Error: Invalid country code: INVALID" in captured.out


def test_run_flow(mocker):
    """run 함수 내부 흐름 테스트"""
    
    mock_algorithm = mocker.Mock(spec=MagicSplit)
    mock_broker = mocker.Mock(spec=BrokerManager)
    mock_yaml_manager = mocker.Mock(spec=YamlKrManager)  
    mock_trade = mocker.Mock(spec=TradeDBManager)
    mock_monitoring = mocker.Mock(spec=MonitoringManager)

    run(CountryCode.KR)

    # 각 메서드 호출 확인
    mock_trade.assert_called_once()
    mock_yaml_manager.assert_called_once_with(CountryCode.KR, "src/config/stock_round_config.yaml")
    mock_broker.assert_called_once()
    mock_algorithm.assert_called_once()
    mock_monitoring.assert_called_once()

    # 모니터링 매니저의 start_monitoring 호출 확인
    mock_monitoring.return_value.start_monitoring.assert_called_once()
    # 자원 해제 확인
    mock_trade.return_value.close.assert_called_once()
    mock_monitoring.return_value.close.assert_called_once()


def test_run_with_exception_handling(mocker):
    """run 함수에서 예외 발생 시 자원 해제 테스트"""
    mock_trade = mocker.Mock(spec=TradeDBManager)
    mock_monitoring = mocker.Mock(spec=MonitoringManager)

    # start_monitoring에서 예외 발생
    mock_monitoring.start_monitoring.side_effect = Exception("Test Exception")

    with pytest.raises(Exception):
        run(CountryCode.KR)

    # 자원 해제 호출 확인
    mock_trade.return_value.close.assert_called_once()
    mock_monitoring.return_value.close.assert_called_once()


import pytest
from src.main_app import MainApp
from src.util.enums import CountryCode


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
    mocker.patch("sys.argv", ["program", "KR"])
    app = MainApp()
    mock_kr_manager = mocker.patch("src.service.yaml.yaml_manager.YamlKrManager", return_value="Mocked KR YAML")
    yaml_manager = app.get_yaml_manager()
    mock_kr_manager.assert_called_once_with()
    assert yaml_manager == "Mocked KR YAML"


def test_get_yaml_manager_us(mocker):
    mocker.patch("sys.argv", ["program", "US"])
    app = MainApp()
    mock_us_manager = mocker.patch("src.service.yaml.yaml_manager.YamlUsManager", return_value="Mocked US YAML")
    yaml_manager = app.get_yaml_manager()
    mock_us_manager.assert_called_once_with()
    assert yaml_manager == "Mocked US YAML"


def test_get_yaml_manager_invalid_country(mocker):
    mocker.patch("sys.argv", ["program", "INVALID"])
    with pytest.raises(SystemExit):
        app = MainApp()
        app.get_yaml_manager()


def test_get_yaml_manager_mock_kr(mocker):
    mocker.patch("sys.argv", ["program", "KR"])
    mock_kr_manager = mocker.patch("src.service.yaml.yaml_manager.YamlKrManager", return_value="Mocked KR YAML")
    app = MainApp()
    assert app.get_yaml_manager() == "Mocked KR YAML"


def test_get_yaml_manager_mock_us(mocker):
    mocker.patch("sys.argv", ["program", "US"])
    mock_us_manager = mocker.patch("src.service.yaml.yaml_manager.YamlUsManager", return_value="Mocked US YAML")
    app = MainApp()
    assert app.get_yaml_manager() == "Mocked US YAML"


# === Test for `get_monitoring_manager` ===
def test_get_monitoring_manager_kr(mocker):
    mocker.patch("sys.argv", ["program", "KR"])
    app = MainApp()
    mock_monitor_manager = mocker.patch(
        "src.service.repository.monitoring_manager.MonitoringKRManager", return_value="Mocked KR Monitor"
    )
    monitor_manager = app.get_monitoring_manager("mock_algorithm")
    mock_monitor_manager.assert_called_once_with("mock_algorithm")
    assert monitor_manager == "Mocked KR Monitor"


def test_get_monitoring_manager_us(mocker):
    mocker.patch("sys.argv", ["program", "US"])
    app = MainApp()
    mock_monitor_manager = mocker.patch(
        "src.service.repository.monitoring_manager.MonitoringUSManager", return_value="Mocked US Monitor"
    )
    monitor_manager = app.get_monitoring_manager("mock_algorithm")
    mock_monitor_manager.assert_called_once_with("mock_algorithm")
    assert monitor_manager == "Mocked US Monitor"


def test_get_monitoring_manager_invalid_country(mocker):
    mocker.patch("sys.argv", ["program", "INVALID"])
    with pytest.raises(SystemExit):
        app = MainApp()
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