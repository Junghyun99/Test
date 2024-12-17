from src.service.logging.system_logger import SystemLogger
from src.service.logging.transaction_logger import TransactionLogger

from src.util.yaml_manager import YamlManager

class LoggerManager(YamlManager):
    def __init__(self, config_file):
        super().__init__(config_file)
        self.loggers = {}
        self._set_logger_class_yaml_config()
        
    def get_logger(self, logger_type):
        if logger_type not in self.loggers:
            if logger_type.upper() == 'SYSTEM':
                self.loggers[logger_type] = SystemLogger("SystemLogger", self.system_log_file)
            elif logger_type.upper() == 'TRANSACTION':
                self.loggers[logger_type] = TransactionLogger("TransactionLogger",self.transaction_log_file)
            else:
                raise ValueError(f"Unknown logger type: {logger_type}")
        return self.loggers[logger_type]

    def set_log_level(self, logger_type, level):
        if logger_type in self.loggers:
            self.loggers[logger_type].get_logger().setLevel(level)
        else:
            raise ValueError(f"Logger type {logger_type} not found")



