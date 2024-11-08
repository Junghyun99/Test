from src.interface.logger_class import BaseLogger

class TransactionLogger(BaseLogger):
    def __init__(self):
        super().__init__('TransactionLogger')



    def log_transaction(self, stock_name: str, action: str, amount: int, price: float):
        message = f"{stock_name} - {action} {amount} shares at {price}"
        self.logger.info(message)
