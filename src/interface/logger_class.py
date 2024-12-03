import logging
from abc import ABC, abstractmethod

from logging.handlers import RotatingFileHandler

class BaseLogger(ABC):
    def __init__(self, logger_name, log_file, level=logging.INFO):
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False
        self.logger.setLevel(level)
        if not self.logger.hasHandlers():
            self._setup_handlers(log_file)

    def _setup_handlers(self, log_file):
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(console_handler)

        # 파일 핸들러
        file_handler = RotatingFileHandler(
    log_file, maxBytes=5*1024*1024, backupCount=3  # 5MB, 3개의 백업 파일
)
        file_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(file_handler)

    def _get_formatter(self):
        return logging.Formatter('%(asctime)s - %(process)d - %(threadName)s - %(module)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s')

    def get_logger(self):
        return self.logger

    def log_debug(self, message, *args):
        if args:
            self.logger.debug(message, *args)
        else:
            self.logger.debug(message)

    def log_info(self, message, *args):
        if args:
            self.logger.info(message, *args)
        else:
            self.logger.info(message)
 

    def log_warning(self, message, *args):
        if args:
            self.logger.warning(message, *args)
        else:
            self.logger.warning(message)


    def log_error(self, message, *args):
        if args:
            self.logger.error(message, *args)
        else:
            self.logger.error(message)
