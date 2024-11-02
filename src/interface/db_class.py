from abc import ABC, abstractmethod

class BaseDB(ABC):
    @abstractmethod
    def _create_table(self):
        pass

    @abstractmethod
    def add_data(self, query, data):
        cursor = self.conn.cursor()
        cursor.execute(query, data)
        self.conn.commit()  # 명시적 commit

    @abstractmethod 
    def get_data(self, query, data):
        cursor = self.conn.cursor()
        cursor.execute(query, data)
        return cursor.fetchall()

    @abstractmethod
    def delete_data(self, query, data):
        cursor = self.conn.cursor()
        cursor.execute(query, data)
        self.conn.commit()  # 명시적 commit

    @abstractmethod
    def update_data(self, query, data):
        cursor = self.conn.cursor()
        cursor.execute(query, data)
        self.conn.commit()  # 명시적 commit

    @abstractmethod
    def close(self):
        self.conn.close()