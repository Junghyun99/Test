import sqlite3
from src.interface.db_class import BaseDB

class StockTradeDB(BaseDB):
    def __init__(self, db_name='StockTrade.db'):
        self.conn = sqlite3.connect(db_name)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS 
                       history (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,         -- 고유 식별자
                       stock_name TEXT NOT NULL,                     -- 종목 이름
                       code TEXT NOT NULL,                            -- 심볼 혹은 번호
                       transaction_id TEXT NOT NULL UNIQUE,          -- 거래번호
                       country_code TEXT NOT NULL, 
                       trade_round INTEGER,
                       trade_type TEXT CHECK(trade_type IN ('buy', 'sell')),  -- 거래 유형 (매수, 매도) 
                       price REAL NOT NULL,                          -- 거래 단가 
                       amount REAL NOT NULL CHECK(amount >= 0),       -- 거래 수량 
                       total_value REAL GENERATED ALWAYS AS (price * amount), -- 총 거래 금액 
                       status TEXT NOT NULL CHECK(status IN ('completed', 'processing' )), -- 거래 상태 (완료, 진행중) 
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP  -- 거래 시간 
                       )''')
        self.conn.commit()