import sqlite3
from src.interface.db_class import BaseDB

class MonitoringDB(BaseDB):
    def __init__(self, logger,  db_name='Monitoring.db'):
        super().__init__(logger, db_name)        
        self._create_table(db_name)

    def _create_table(self, db_name):
        with sqlite3.connect(db_name) as conn:
            self.conn = conn
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS 
                       monitoring (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,         -- 고유 식별자
                       stock_name TEXT NOT NULL,                     -- 종목 이름
                       code TEXT NOT NULL UNIQUE,                            -- 심볼 혹은 번호
                       country_code TEXT NOT NULL, 
                       trade_round INTEGER CHECK(typeof(trade_round) == 'integer' AND trade_round > -1), --라운드
                       price REAL NOT NULL CHECK(typeof(price) == 'real' AND price > 0),     -- 거래 단가
                       quantity INTEGER NOT NULL CHECK(typeof(quantity) == 'integer' AND quantity > 0), -- 수량
                       buy_rate INTEGER NOT NULL CHECK(typeof(buy_rate) == 'integer' AND buy_rate > 0 AND buy_rate < 100),
                       sell_rate INTEGER NOT NULL CHECK(typeof(sell_rate) == 'integer' AND sell_rate > 0 AND sell_rate < 100)
                       )''')
            self.conn.commit()