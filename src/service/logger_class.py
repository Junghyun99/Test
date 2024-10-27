import logging
from abc import ABC, abstractmethod

class BaseLogger(ABC):
    def __init__(self, logger_name: str, log_file: str, level=logging.INFO):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)
        self._setup_handlers(log_file)

    def _setup_handlers(self, log_file: str):
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(console_handler)
        
        # 파일 핸들러
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(file_handler)

    def _get_formatter(self):
        return logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    @abstractmethod
    def log(self, message: str):
        pass