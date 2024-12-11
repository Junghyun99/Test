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