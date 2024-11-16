from src.interface.logger_class import BaseLogger

class TransactionLogger(BaseLogger):
    def __init__(self, logger_name, log_file):
        super().__init__(logger_name, log_file)



    def log_transaction(self, stock_name: str, action: str, amount: int, price: float):
        message = f"{stock_name} - {action} {amount} shares at {price}"
        self.logger.info(message)
