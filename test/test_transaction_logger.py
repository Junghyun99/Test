import pytest
import os
import logging
from src.service.logging.transaction_logger import TransactionLogger

LOG_FILE = "test_log_file.log"

@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / LOG_FILE
    yield file_path
    if file_path.exists():
        os.remove(file_path)

@pytest.fixture
def transaction_logger(temp_file):
    return TransactionLogger("TestLogger", temp_file)


def test_log_transaction_message_format(caplog, transaction_logger):
    transaction_logger.get_logger().propagate = True
    with caplog.at_level(logging.INFO):
        transaction_logger.log_transaction("AAPL", "buy", 10, 150.5)
        assert "AAPL - buy 10 shares at 150.5" in caplog.text

def test_log_transaction_log_level(caplog, transaction_logger):
    transaction_logger.get_logger().propagate = True
    with caplog.at_level(logging.INFO):
        transaction_logger.log_transaction("GOOG", "sell", 5, 2500.75)
        for record in caplog.records:
            assert record.levelname == "INFO"

def test_log_transaction_different_stocks(caplog, transaction_logger):
    transaction_logger.get_logger().propagate = True
    with caplog.at_level(logging.INFO):
        transaction_logger.log_transaction("MSFT", "buy", 20, 300.0)
        assert "MSFT - buy 20 shares at 300.0" in caplog.text

def test_log_transaction_multiple_actions(caplog, transaction_logger):
    transaction_logger.get_logger().propagate = True
    with caplog.at_level(logging.INFO):
        transaction_logger.log_transaction("TSLA", "buy", 15, 800.25)
        transaction_logger.log_transaction("TSLA", "sell", 15, 820.75)
        assert "TSLA - buy 15 shares at 800.25" in caplog.text
        assert "TSLA - sell 15 shares at 820.75" in caplog.text

def test_log_transaction_large_quantity(caplog, transaction_logger):
    transaction_logger.get_logger().propagate = True
    with caplog.at_level(logging.INFO):
        transaction_logger.log_transaction("AMZN", "buy", 10000, 3500.5)
        assert "AMZN - buy 10000 shares at 3500.5" in caplog.text