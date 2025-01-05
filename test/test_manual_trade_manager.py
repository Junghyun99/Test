import pytest
from src.util.enums import CountryCode
from src.util.price_calculator import PriceCalculator
from src.service.algorithm.manual_trade_manager import ManualTradeManager


@pytest.fixture
def setup_trade_manager(mocker):
    # Mock dependencies using pytest-mock
    monitoring_manager = mocker.Mock()
    broker_manager = mocker.Mock()
    trade_db_manager = mocker.Mock()
    logger = mocker.Mock()

    # Initialize the ManualTradeManager
    trade_manager = ManualTradeManager(
        monitoring_manager=monitoring_manager,
        broker_manager=broker_manager,
        trade_db_manager=trade_db_manager,
        logger=logger
    )
    return trade_manager, monitoring_manager, broker_manager, trade_db_manager, logger


def test_handle_trade_successful_execution(setup_trade_manager):
    trade_manager, monitoring_manager, broker_manager, trade_db_manager, logger = setup_trade_manager

    # Mock behaviors
    monitoring_manager.check_already_existing_monitoring.return_value = False
    broker_manager.get_current_price.return_value = 50000
    broker_manager.place_market_order.return_value = (True, ("TX123", 50500, 10))

    # Execute the trade
    trade_manager.handle_trade("005930", "Samsung Electronics", 100000)

    # Assertions
    monitoring_manager.check_already_existing_monitoring.assert_called_once_with("005930")
    broker_manager.get_current_price.assert_called_once_with("005930")
    broker_manager.place_market_order.assert_called_once_with("005930", 2, "BUY")
    trade_db_manager.record_buy_transaction.assert_called_once_with(
        "Samsung Electronics", "005930", "TX123", CountryCode.KR, 1, 50500, 10
    )
    monitoring_manager.add_stock_in_monitoring.assert_called_once()
    logger.info.assert_called()


def test_handle_trade_already_monitored(setup_trade_manager):
    trade_manager, monitoring_manager, _, _, logger = setup_trade_manager

    # Mock behaviors
    monitoring_manager.check_already_existing_monitoring.return_value = True

    # Execute the trade
    trade_manager.handle_trade("005930", "Samsung Electronics", 100000)

    # Assertions
    monitoring_manager.check_already_existing_monitoring.assert_called_once_with("005930")
    logger.info.assert_any_call("Manual trade initiated for 005930")
    logger.info.assert_any_call("Stopping auto-trade for 005930.")
    monitoring_manager.delete_stock_in_monitoring.assert_called_once_with("005930")


def test_handle_trade_order_failure(setup_trade_manager):
    trade_manager, monitoring_manager, broker_manager, _, logger = setup_trade_manager

    # Mock behaviors
    monitoring_manager.check_already_existing_monitoring.return_value = False
    broker_manager.get_current_price.return_value = 50000
    broker_manager.place_market_order.return_value = (False, None)

    # Execute the trade
    trade_manager.handle_trade("005930", "Samsung Electronics", 100000)

    # Assertions
    logger.error.assert_called_with("Failed to place BUY order for 005930.")


def test_handle_trade_invalid_inputs(setup_trade_manager):
    trade_manager, _, _, _, _ = setup_trade_manager

    # Execute the trade with invalid inputs
    with pytest.raises(TypeError):
        trade_manager.handle_trade(None, "Samsung Electronics", 100000)

    with pytest.raises(TypeError):
        trade_manager.handle_trade("005930", None, 100000)

    with pytest.raises(TypeError):
        trade_manager.handle_trade("005930", "Samsung Electronics", None)


def test_handle_trade_logging_behavior(setup_trade_manager):
    trade_manager, _, _, _, logger = setup_trade_manager

    # Execute the trade
    trade_manager.handle_trade("005930", "Samsung Electronics", 100000)

    # Verify logging calls
    logger.info.assert_called()