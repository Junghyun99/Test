# stock_stack_db.py

import sqlite3

class StockStackDB:
    def __init__(self, db_name="trading_stack.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS stock_stack (
            stock_symbol TEXT PRIMARY KEY,
            stack TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def save_stack(self, stock_symbol, stack):
        query = """
        INSERT OR REPLACE INTO stock_stack (stock_symbol, stack) VALUES (?, ?)
        """
        stack_str = ','.join([f"{action}:{amount}" for action, amount in stack])
        self.conn.execute(query, (stock_symbol, stack_str))
        self.conn.commit()

    def load_stack(self, stock_symbol):
        query = "SELECT stack FROM stock_stack WHERE stock_symbol = ?"
        cursor = self.conn.execute(query, (stock_symbol,))
        result = cursor.fetchone()
        if result:
            stack_str = result[0]
            stack = [(action.split(':')[0], int(action.split(':')[1])) for action in stack_str.split(',')]
            return stack
        return []

    def close(self):
        self.conn.close()