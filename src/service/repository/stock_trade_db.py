import sqlite3
from db_class.py import BaseDB

class StockTradeDB(BaseDB):
    def __init__(self, db_name='StockTrade.db'):
        self.conn = sqlite3.connect(db_name)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS history 
                              (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              date TEXT DEFAULT (datetime('now')),
                              type TEXT NOT NULL CHECK (type IN ('BUY', 'SELL')),
                              symbol TEXT NOT NULL,
                              amount INTEGER NOT NULL CHECK (amount > 0),
                              price REAL NOT NULL,
                              fee REAL NOT NULL
                              )''')

    def add_data(self, query, data):
        pass

    def get_data(self, query, data):
        pass

    def delete_data(self, query, data):
        pass

    def update_data(self, query, data):
        pass                 

    def close(self):
        self.conn.close()