from src.service.repository.stock_trade_db import StockTradeDB


class TradeDBManager:
    def __init__(self, db_name='StockTrade.db'):
        self.db = StockTradeDB(db_name)

    # Reading Methods
    def get_trade_round(self, code, round):
        '''

        '''
        query = '''
            SELECT trade_round, id, price, amount, total_value FROM history 
            WHERE code = ? AND status = 'processing' AND trade_round = ?
        '''
        return dict(self.db.read_data(query, (code, round)))
    
    def get_last_round_data(self, code):             
        query = '''
            SELECT * FROM history 
            WHERE code = ? AND status = 'processing' 
            ORDER BY trade_round ASC
        '''        
        result = self.db.read_data(query, (code,))
        return dict(result[-1])            

    def get_completed_pairs(self, stock_name=None, date=None):
        """Returns completed trade pairs, filtered by stock name or date.
        query = '''
            SELECT * FROM history 
            WHERE status = 'completed' AND pair_id != 0
        '''
        params = []
        if stock_name:
            query += " AND stock_name = ?"
            params.append(stock_name)
        if date:
            query += " AND DATE(timestamp) = ?"
            params.append(date)
        return self.db.read_data(query, tuple(params))
        """
        pass

    def get_active_stacks(self, stock_name=None, date=None):
        """Returns all active stacks, optionally filtered by stock name or date.
        query = '''
            SELECT * FROM history 
            WHERE status = 'processing'
        '''
        params = []
        if stock_name:
            query += " AND stock_name = ?"
            params.append(stock_name)
        if date:
            query += " AND DATE(timestamp) = ?"
            params.append(date)
        return self.db.read_data(query, tuple(params))
        """
        pass

    # Writing Methods
    def record_buy_transaction(self, stock_name, code, transaction_id, country_code, trade_round, price, amount):
        query = '''INSERT INTO history (stock_name, code, transaction_id, country_code, trade_round, trade_type, price, amount, status, pair_id) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    data = (stock_name, code, transaction_id, country_code, trade_round, 'buy', price, amount, 'processing', 0)
  
        self.db.insert_data(query, data)

    def record_sell_transaction(self, stock_name, code, transaction_id, country_code, trade_round, price, amount):
        instance = self.get_last_round_data(code)
        
        query = '''INSERT INTO history (stock_name, code, transaction_id, country_code, trade_round, trade_type, price, amount, status, pair_id) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    data = (stock_name, code, transaction_id, country_code, trade_round, 'sell', price, amount, 'completed', instance['id'])
  
        self.db.insert_data(query, data)

        query = '''
            SELECT id FROM history 
            WHERE code = ? AND transaction_id = ?
        '''  
        id = self.db.read_data(query, (code, transaction_id))

        # Update the paired buy transaction
        update_query = "UPDATE history SET status = 'COMPLETED' AND pair_id =? WHERE id = ?"
        self.db.update_data(update_query, (id,instance['pair_id']))

    def manual_adjustment(self, transaction_id, new_status, new_pair_id=None):
        """Manually adjusts a transaction's status and optionally updates the pair ID.
        query = "UPDATE history SET status = ?"
        data = [new_status]
        if new_pair_id is not None:
            query += ", pair_id = ?"
            data.append(new_pair_id)
        query += " WHERE transaction_id = ?"
        data.append(transaction_id)
        self.db.update_data(query, tuple(data))
        """
        pass