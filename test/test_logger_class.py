import pytest
import os
import logging
from src.interface.logger_class import BaseLogger

LOG_FILE = "test_log_file.log"

@pytest.fixture
def file_path(tmp_path):
    FILE_PATH = tmp_path / LOG_FILE
    return FILE_PATH

@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / LOG_FILE
    yield file_path
    if file_path.exists():
        os.remove(file_path)

@pytest.fixture
def logger(temp_file):
    return BaseLogger("TestLogger", temp_file)
  
def test_get_logger_name(logger):
    assert logger.get_logger().name == "TestLogger"

def test_get_logger_level_default(logger):
    assert logger.get_logger().level == logging.INFO

def test_get_logger_propagate(logger):
    assert not logger.get_logger().propagate


def test_get_logger_handlers(logger):
    assert len(logger.get_logger().handlers) == 2  
    # Console and File handlers

def test_get_logger_file_handler_type(logger):
    assert any(isinstance(handler, logging.FileHandler) for handler in logger.get_logger().handlers)

def test_log_debug_enabled(logger):
    logger.log_debug("Debug message")
    assert logger.get_logger().isEnabledFor(logging.DEBUG) == False

def test_log_debug_message_content(logger, caplog):
    with caplog.at_level(logging.DEBUG):
        logger.log_debug("Debug message")
    assert "Debug message" not in caplog.text

def test_log_info_level(logger, caplog):
    logger.get_logger().propagate = True
    with caplog.at_level(logging.INFO):
        logger.log_info("Check level")
    assert "INFO" in caplog.text

def test_log_info_enabled_when_above_level(logger, caplog):
    logger.get_logger().propagate = True
    with caplog.at_level(logging.WARNING):
        logger.log_warning("This appear")
    assert "This appear" in caplog.text

def test_log_info_file_output(logger,file_path):
    logger.log_info("File output test")
    with open(file_path, "r") as file:
        assert "File output test" in file.read()

def test_log_warning_message(logger, caplog):
    logger.get_logger().propagate = True
    with caplog.at_level(logging.WARNING):
        logger.log_warning("Warning message")
    assert "Warning message" in caplog.text
    assert "WARNING" in caplog.text

def test_log_error_message(logger, caplog):
    logger.get_logger().propagate = True
    with caplog.at_level(logging.ERROR):
        logger.log_error("Error message")
    assert "Error message" in caplog.text
    assert "ERROR" in caplog.text


def test_multiple_log_levels(logger, caplog):
    logger.get_logger().propagate = True
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
    assert logger.get_logger().isEnabledFor(logging.INFO)

def test_logger_warning(logger):
    logger.log_warning("This is a warning message")
    assert logger.get_logger().isEnabledFor(logging.WARNING)

def test_logger_error(logger):
    logger.log_error("This is an error message")
    assert logger.get_logger().isEnabledFor(logging.ERROR)

def test_log_file_created(logger, file_path):
    logger.log_info("Testing file creation")
    assert os.path.exists(file_path)

# Composite scenarios for BaseLogger
def test_logger_multiple_levels(logger):
    logger.log_debug("Debug level message")
    logger.log_info("Info level message")
    logger.log_warning("Warning level message")
    logger.log_error("Error level message")
    assert logger.get_logger().isEnabledFor(logging.DEBUG) == False
    assert logger.get_logger().isEnabledFor(logging.INFO)
    assert logger.get_logger().isEnabledFor(logging.WARNING)
    assert logger.get_logger().isEnabledFor(logging.ERROR)

