from src.interface.logger_class import BaseLogger

class TransactionLogger(BaseLogger):
    def __init__(self):
        super().__init__('TransactionLogger')
