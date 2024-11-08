import pytest
import os
import logging
from src.interface.logger_class import BaseLogger

LOG_FILE = "test_log_file.log"

@pytest.fixture
def logger():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    yield BaseLogger("TestLogger", LOG_FILE).get_logger()
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

def test_get_logger_name(logger):
    assert logger.name == "TestLogger"

def test_get_logger_level_default(logger):
    assert logger.level == logging.INFO

def test_get_logger_propagate(logger):
    assert not logger.propagate

def test_get_logger_handlers(logger):
    assert len(logger.handlers) == 2  
    # Console and File handlers

def test_get_logger_file_handler_type(logger):
    assert any(isinstance(handler, logging.FileHandler) for handler in logger.handlers)

def test_log_debug_enabled(logger):
    logger.log_debug("Debug message")
    assert !logger.isEnabledFor(logging.DEBUG)

def test_log_debug_message_content(logger, caplog):
    with caplog.at_level(logging.DEBUG):
        logger.log_debug("Debug message")
    assert "Debug message" not in caplog.text

def test_log_info_message(logger, caplog):
    with caplog.at_level(logging.INFO):
        logger.log_info("Info message")
    assert "Info message" in caplog.text

def test_log_info_level(logger, caplog):
    with caplog.at_level(logging.INFO):
        logger.log_info("Check level")
    assert "INFO" in caplog.text

def test_log_info_enabled_when_above_level(logger, caplog):
    with caplog.at_level(logging.WARING):
        logger.log_waring("This appear")
    assert "This appear" in caplog.text


def test_log_info_file_output(logger):
    logger.log_info("File output test")
    with open(LOG_FILE, "r") as file:
        assert "File output test" in file.read()

def test_log_warning_message(logger, caplog):
    with caplog.at_level(logging.WARNING):
        logger.log_warning("Warning message")
    assert "Warning message" in caplog.text
    assert "WARNING" in caplog.text

def test_log_error_message(logger, caplog):
    with caplog.at_level(logging.ERROR):
        logger.log_error("Error message")
    assert "Error message" in caplog.text
    assert "ERROR" in caplog.text


def test_multiple_log_levels(logger, caplog):
    with caplog.at_level(logging.INFO):
        logger.log_debug("Debug message")
        logger.log_info("Info message")
        logger.log_warning("Warning message")
        logger.log_error("Error message")
    assert "Debug message" not in caplog.text
    assert "Info message" in caplog.text
    assert "Warning message" in caplog.text
    assert "Error message" in caplog.text


def test_logger_info(logger):
    logger.log_info("This is an info message")
    assert logger.isEnabledFor(logging.INFO)

def test_logger_warning(logger):
    logger.log_warning("This is a warning message")
    assert logger.isEnabledFor(logging.WARNING)

def test_logger_error(logger):
    logger.log_error("This is an error message")
    assert logger.isEnabledFor(logging.ERROR)

def test_log_file_created(logger):
    logger.log_info("Testing file creation")
    assert os.path.exists(LOG_FILE)

# Composite scenarios for BaseLogger
def test_logger_multiple_levels(logger):
    logger.log_debug("Debug level message")
    logger.log_info("Info level message")
    logger.log_warning("Warning level message")
    logger.log_error("Error level message")
    assert !logger.isEnabledFor(logging.DEBUG)
    assert logger.isEnabledFor(logging.INFO)
    assert logger.isEnabledFor(logging.WARNING)
    assert logger.isEnabledFor(logging.ERROR)

