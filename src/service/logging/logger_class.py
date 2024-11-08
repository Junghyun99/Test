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
        return logging.Formatter('%(asctime)s - %(process)d - %(threadName)s - %(module)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s')
    
    @abstractmethod
    def log(self, message: str):
        pass








logger = TradeLogger()

logger.log_transaction("Samsung", "BUY", 100, 70.5)
logger.log_warning("Price is volatile")
logger.log_error("Failed to execute transaction")
logger.log_debug("Debugging information")


    def log_transaction(self, stock_name: str, action: str, amount: int, price: float):
        message = f"{stock_name} - {action} {amount} shares at {price}"
        self.logger.info(message)

    def log_error(self, message: str):
        self.logger.error(message)

    def log_warning(self, message: str):
        self.logger.warning(message)

    def log_debug(self, message: str):
        self.logger.debug(message)