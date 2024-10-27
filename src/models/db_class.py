from abc import ABC, abstractmethod

class BaseDB(ABC):
    @abstractmethod
    def _create_table(self):
        pass

    @abstractmethod
    def add_data(self, transaction):
        pass

    @abstractmethod
    def get_data(self, stock_name):
        pass

    @abstractmethod
    def delete_data(self, transaction_id):
        pass

    @abstractmethod
    def update_data(self, transaction_id, quantity, price):
        pass

    @abstractmethod
    def close(self):
        pass