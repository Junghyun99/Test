from src.service.logging.system_logger import SystemLogger
from src.service.logging.transaction_logger import TransactionLogger

from src.util.yaml_manager import YamlManager

import yaml
from pathlib import Path


class LoggerManager(YamlManager):
    def __init__(self):
        self.loggers = {}
        self._set_yaml_config()

    def _set_yaml_config(self):
        # YAML 설정 로드
        with open("src/config/config.yaml", "r") as file:
            config = yaml.safe_load(file)

        logger = config['logger_class']
        log_dir = Path(logger['log_dir'])
        self.system_log_file = log_dir / logger['system_log_file']
        self.transaction_log_file = log_dir / logger['transaction_log_file']

        # 디렉토리 생성 (없으면 생성)
        log_dir.mkdir(parents=True, exist_ok=True)

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



logger_manager = LoggerManager()