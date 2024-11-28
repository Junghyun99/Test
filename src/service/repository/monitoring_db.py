import sqlite3
from src.interface.db_class import BaseDB

class MonitoringDB(BaseDB):
    def __init__(self, db_name='Monitoring.db'):
        self.conn = sqlite3.connect(db_name)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS 
                       monitoring (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,         -- 고유 식별자
                       stock_name TEXT NOT NULL,                     -- 종목 이름
                       code TEXT NOT NULL UNIQUE,                            -- 심볼 혹은 번호
                       country_code TEXT NOT NULL, 
                       trade_round INTEGER CHECK(trade_round > 0),
                       price REAL NOT NULL CHECK(price > 0),                          -- 거래 단가 
                       quantity INTEGER NOT NULL,
                       buy_rate INTEGER NOT NULL CHECK(buy_rate > 0),
sell_rate INTEGER NOT NULL CHECK(sell_rate > 0)
                       )''')
        self.conn.commit()