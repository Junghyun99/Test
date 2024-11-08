from src.interface.logger_class import BaseLogger

class SystemLogger(BaseLogger):
    def __init__(self):
        super().__init__('SystemLogger')