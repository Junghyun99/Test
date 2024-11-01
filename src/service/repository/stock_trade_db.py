import sqlite3
from db_class import BaseDB

class StockTradeDB(BaseDB):
    def __init__(self, db_name='StockTrade.db'):
        self.conn = sqlite3.connect(db_name)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS history 
                              (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,         -- 고유 식별자
    stock_name TEXT NOT NULL,                     -- 종목 이름
   나라 TEXT NOT NULL, 
    transaction_id TEXT NOT NULL,                 -- 거래번호
    country_code TEXT NOT NULL,
    trade_round INTEGER,
    trade_type TEXT CHECK(trade_type IN ('buy', 'sell')),  -- 거래 유형 (매수, 매도)
    price REAL NOT NULL,                          -- 거래 단가
    amount REAL NOT NULL,                         -- 거래 수량
    total_value REAL GENERATED ALWAYS AS (price * amount), -- 총 거래 금액
    status TEXT CHECK(status IN ('completed', 'processing' )), -- 거래 상태 (완료, 진행중)
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP  -- 거래 시간 )''')