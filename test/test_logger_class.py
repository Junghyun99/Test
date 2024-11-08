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

#여기서부터 정리
def test_log_warning_message(caplog):
    logger = BaseLogger("TestLogger", "test_log.log")
    with caplog.at_level(logging.WARNING):
        logger.log_warning("Warning message")
    assert "Warning message" in caplog.text

def test_log_warning_level(caplog):
    logger = BaseLogger("TestLogger", "test_log.log")
    with caplog.at_level(logging.WARNING):
        logger.log_warning("Level check")
    assert "WARNING" in caplog.text

def test_log_warning_no_logging_when_disabled(caplog):
    logger = BaseLogger("TestLogger", "test_log.log", level=logging.ERROR)
    with caplog.at_level(logging.WARNING):
        logger.log_warning("Should not log")
    assert "Should not log" not in caplog.text

def test_log_warning_handler_types():
    logger = BaseLogger("TestLogger", "test_log.log")
    assert any(isinstance(handler, logging.StreamHandler) for handler in logger.logger.handlers)

def test_log_warning_format_output(caplog):
    logger = BaseLogger("TestLogger", "test_log.log")
    with caplog.at_level(logging.WARNING):
        logger.log_warning("Formatted warning")
    assert "WARNING" in caplog.text


def test_log_error_message(caplog):
    logger = BaseLogger("TestLogger", "test_log.log")
    with caplog.at_level(logging.ERROR):
        logger.log_error("Error message")
    assert "Error message" in caplog.text

def test_log_error_level(caplog):
    logger = BaseLogger("TestLogger", "test_log.log")
    with caplog.at_level(logging.ERROR):
        logger.log_error("Error level test")
    assert "ERROR" in caplog.text

def test_log_error_when_level_is_low(caplog):
    logger = BaseLogger("TestLogger", "test_log.log", level=logging.CRITICAL)
    with caplog.at_level(logging.ERROR):
        logger.log_error("Should not be logged")
    assert "Should not be logged" not in caplog.text

def test_log_error_multiple_handlers():
    logger = BaseLogger("TestLogger", "test_log.log")
    assert len(logger.logger.handlers) == 2

def test_log_error_to_file():
    logger = BaseLogger("TestLogger", "test_log.log")
    logger.log_error("Error to file")
    with open("test_log.log", "r") as file:
        assert "Error to file" in file.read()


def test_multiple_log_levels(caplog):
    logger = BaseLogger("TestLogger", "test_log.log", level=logging.DEBUG)
    with caplog.at_level(logging.DEBUG):
        logger.log_debug("Debug message")
        logger.log_info("Info message")
        logger.log_warning("Warning message")
        logger.log_error("Error message")
    assert "Debug message" in caplog.text
    assert "Info message" in caplog.text
    assert "Warning message" in caplog.text
    assert "Error message" in caplog.text


# gptnn체크

def test_logger_info(logger):
    logger.log_info("This is an info message")
    assert logger.isEnabledFor(logging.INFO)

def test_logger_warning(logger):
    logger.log_warning("This is a warning message")
    assert logger.isEnabledFor(logging.WARNING)

def test_logger_error(logger):
    logger.log_error("This is an error message")
    assert logger.isEnabledFor(logging.ERROR)

def test_log_file_created():
    BaseLogger("FileTestLogger", LOG_FILE).get_logger().info("Testing file creation")
    assert os.path.exists(LOG_FILE)

# Composite scenarios for BaseLogger
def test_logger_multiple_levels(logger):
    logger.debug("Debug level message")
    logger.info("Info level message")
    logger.warning("Warning level message")
    logger.error("Error level message")
    assert logger.isEnabledFor(logging.DEBUG)
    assert logger.isEnabledFor(logging.INFO)
    assert logger.isEnabledFor(logging.WARNING)
    assert logger.isEnabledFor(logging.ERROR)

def test_log_message_content():
    test_logger = BaseLogger("ContentLogger", LOG_FILE).get_logger()
    test_logger.info("Message content check")
    with open(LOG_FILE, 'r') as file:
        content = file.read()
    assert "Message content check" in content

def test_logger_propagation(logger):
    assert logger.propagate is False

def test_logger_formatting():
    logger = BaseLogger("FormatLogger", LOG_FILE).get_logger()
    logger.info("Testing formatting")
    with open(LOG_FILE, 'r') as file:
        content = file.read()
    assert "FormatLogger" in content  # Check for logger name in format

def test_logger_file_handler():
    test_logger = BaseLogger("HandlerLogger", LOG_FILE).get_logger()
    test_logger.info("Testing file handler")
    with open(LOG_FILE, 'r') as file:
        content = file.read()
    assert len(content) > 0