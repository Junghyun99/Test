import sqlite3

class StockTradeHistoryDB:
    def __init__(self, db_name='StockTradeHistory.db'):
        self.conn = sqlite3.connect(db_name)
        self._createTable()

    def _createTable(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE trade_history (
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
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP  -- 거래 시간
)''')
            
    def loadHistoryDate(self,date1, date2):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM history WHERE date BETWEEN ? AND ?,(date1,date2)''')        
        return cursor.fetchall()
    
    def saveHistory():
        pass

    def close(self):
        self.conn.close()