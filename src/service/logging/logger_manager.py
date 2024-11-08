from system_logger import SystemLogger
from transaction_logger import TransactionLogger


class LoggerManager:
    def __init__(self):
        self.loggers = {}

    def get_logger(self, logger_type):
        if logger_type not in self.loggers:
            if logger_type == 'system':
                self.loggers[logger_type] = SystemLogger().get_logger()
            elif logger_type == 'transaction':
                self.loggers[logger_type] = TransactionLogger().get_logger()
            else:
                raise ValueError(f"Unknown logger type: {logger_type}")
        return self.loggers[logger_type]

    def set_log_level(self, logger_type, level):
        if logger_type in self.loggers:
            self.loggers[logger_type].setLevel(level)
        else:
            raise ValueError(f"Logger type {logger_type} not found")

# LoggerManager 인스턴스 생성
logger_manager = LoggerManager()

# SystemLogger와 TransactionLogger 가져오기
system_logger = logger_manager.get_logger('system')
transaction_logger = logger_manager.get_logger('transaction')

# 로그 메시지 기록
system_logger.info("This is an info message from the system logger.")
transaction_logger.error("This is an error message from the transaction logger.")

# 로그 레벨 변경
logger_manager.set_log_level('system', logging.DEBUG)
system_logger.debug("This debug message will now be shown since the log level is DEBUG.")