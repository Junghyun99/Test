from system_logger import SystemLogger
from transaction_logger import TransactionLogger


class LoggerManager:
    def __init__(self):
        self.loggers = {}

    def get_logger(self, logger_type):
        if logger_type not in self.loggers:
            if logger_type.upper() == 'SYSTEM':
                self.loggers[logger_type] = SystemLogger().get_logger()
            elif logger_type.upper() == 'TRANSACTION':
                self.loggers[logger_type] = TransactionLogger().get_logger()
            else:
                raise ValueError(f"Unknown logger type: {logger_type}")
        return self.loggers[logger_type]

    def set_log_level(self, logger_type, level):
        if logger_type in self.loggers:
            self.loggers[logger_type].setLevel(level)
        else:
            raise ValueError(f"Logger type {logger_type} not found")