import sqlite3

class StockTradeHistoryDB:
    def __init__(self, db_name='StockTradeHistory.db'):
        self.conn = sqlite3.connect(db_name)
        self._createTable()

    def _createTable(self):
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
            
    def loadHistoryDate(self,date1, date2):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM history WHERE date BETWEEN ? AND ?,(date1,date2)''')        
        return cursor.fetchall()
    
    def saveHistory():
        pass

    def close(self):
        self.conn.close()