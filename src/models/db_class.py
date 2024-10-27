from abc import ABC, abstractmethod

class BaseDB(ABC):
    @abstractmethod
    def _create_table(self):
        pass

    @abstractmethod
    def add_data(self, query, data):
        pass

    @abstractmethod
    def get_data(self, query, data):
        pass

    @abstractmethod
    def delete_data(self, query, data):
        pass

    @abstractmethod
    def update_data(self, query, data):
        pass

    @abstractmethod
    def close(self):
        pass