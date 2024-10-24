import pytest
from trade_logger import TradeLogger

def test_log_transaction():
    logger = TradeLogger()
    logger.log_transaction("Samsung", "buy", 2, 50000)
    assert len(logger.transactions) == 1

def test_display_trade_history(capsys):
    logger = TradeLogger()
    logger.log_transaction("Samsung", "buy", 2, 50000)
    logger.display_trade_history()
    captured = capsys.readouterr()
    assert "buy 2" in captured.out