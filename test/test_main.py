import pytest
from src.main import main, parse_country_code, run
from src.util.enums import CountryCode


def test_parse_country_code_valid():
    """Valid country code 테스트"""
    assert parse_country_code("KR") == CountryCode.KR
    assert parse_country_code("US") == CountryCode.US


def test_parse_country_code_invalid():
    """Invalid country code 테스트"""
    assert parse_country_code("INVALID") is None
    assert parse_country_code("") is None


def test_main_default_country(mocker):
    """Default country 테스트 (KR)"""
    mocker.patch("argparse.ArgumentParser.parse_args", return_value=mocker.Mock(country="KR"))
    mock_run = mocker.patch("src.main.run")

    main()

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

    with pytest.raises(Exception):  # Invalid code로 인한 종료
        main()

    captured = capsys.readouterr()
    assert "Error: Invalid country code: INVALID" in captured.out


def test_run_flow(mocker):
    """run 함수 내부 흐름 테스트"""
    mock_trade = mocker.patch("src.main.TradeDbManager")
    mock_yaml_manager = mocker.patch("src.main.get_yaml_manager")
    mock_broker = mocker.patch("src.main.BrokerManager")
    mock_algorithm = mocker.patch("src.main.MagicSplit")
    mock_monitoring = mocker.patch("src.main.get_monitoring_manager")

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
    mock_trade = mocker.patch("src.main.TradeDbManager")
    mock_monitoring = mocker.patch("src.main.get_monitoring_manager")

    # start_monitoring에서 예외 발생
    mock_monitoring.return_value.start_monitoring.side_effect = Exception("Test Exception")

    with pytest.raises(Exception, match="Test Exception"):
        run(CountryCode.KR)

    # 자원 해제 호출 확인
    mock_trade.return_value.close.assert_called_once()
    mock_monitoring.return_value.close.assert_called_once()