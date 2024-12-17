import pytest
import logging
from src.service.logging.logger_manager import LoggerManager

@pytest.fixture
def logger_manager():
    # Fixture to create an instance of LoggerManager
    return LoggerManager("test/test_config.yaml")

def test_get_logger_system_type(logger_manager):
    # Test to get a SystemLogger instance
    logger = logger_manager.get_logger('SYSTEM')
    assert isinstance(logger.get_logger(), logging.Logger)
    assert logger.get_logger().name == "SystemLogger"

def test_get_logger_transaction_type(logger_manager):
    # Test to get a TransactionLogger instance
    logger = logger_manager.get_logger('TRANSACTION')
    assert isinstance(logger.get_logger(), logging.Logger)
    assert logger.get_logger().name == "TransactionLogger"

def test_get_logger_invalid_type(logger_manager):
    # Test to handle an invalid logger type
    with pytest.raises(ValueError, match="Unknown logger type: INVALID"):
        logger_manager.get_logger('INVALID')

def test_set_log_level_existing_logger(logger_manager):
    # Test setting log level for an existing logger
    logger = logger_manager.get_logger('SYSTEM')
    logger_manager.set_log_level('SYSTEM', logging.DEBUG)
    assert logger.get_logger().level == logging.DEBUG

def test_set_log_level_non_existing_logger(logger_manager):
    # Test setting log level for a non-existing logger
    with pytest.raises(ValueError, match="Logger type NON_EXISTENT not found"):
        logger_manager.set_log_level('NON_EXISTENT', logging.ERROR)
