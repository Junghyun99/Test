from src.interface.logger_class import BaseLogger

class SystemLogger(BaseLogger):
    def __init__(self, logger_name, log_file):
        super().__init__(logger_name, log_file)