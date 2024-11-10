from src.service.repository.stock_trade_db import StockTradeDB


class TradeDBManager:
    def __init__(self, db_name='StockTrade.db'):
        self.db = StockTradeDB(db_name)

    # Reading Methods
    def get_latest_active_stack(self, stock_code):
    """
    종목을 넣어주면 최신 스택을 리턴,
    라운드 순으로 id, 매수 가격,양,총량을 리스트로 리턴,
    """
    # Query to get active transactions ordered by trade_round
    query = '''
        SELECT trade_round, id, price, amount, total_value FROM history 
        WHERE code = ? AND status = 'processing' 
        ORDER BY trade_round ASC
    '''
    # Fetch the data from the database
    result = self.db.read_data(query, (stock_name,))
    
    # Process the result to extract prices in trade_round order
    price_list = [record[1] for record in result]  # record[1] is the price
    
    return price_list



    def get_completed_pairs(self, stock_name=None, date=None):
        """Returns completed trade pairs, filtered by stock name or date."""
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

    def get_active_stacks(self, stock_name=None, date=None):
        """Returns all active stacks, optionally filtered by stock name or date."""
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

    # Writing Methods
    def record_buy_transaction(self, stock_name, code, transaction_id, country_code, trade_round, price, amount):
        """Inserts a new buy transaction record."""
        query = '''
            INSERT INTO history (stock_name, code, transaction_id, country_code, trade_round, 
                                 trade_type, price, amount, status, pair_id) 
            VALUES (?, ?, ?, ?, ?, 'buy', ?, ?, 'processing', 0)
        '''
        data = (stock_name, code, transaction_id, country_code, trade_round, price, amount)
        self.db.insert_data(query, data)

    def record_sell_transaction(self, stock_name, code, transaction_id, country_code, trade_round, price, amount, pair_id):
        """Inserts a new sell transaction record and updates the paired buy transaction."""
        # Insert the sell transaction
        query = '''
            INSERT INTO history (stock_name, code, transaction_id, country_code, trade_round, 
                                 trade_type, price, amount, status, pair_id) 
            VALUES (?, ?, ?, ?, ?, 'sell', ?, ?, 'completed', ?)
        '''
        data = (stock_name, code, transaction_id, country_code, trade_round, price, amount, pair_id)
        self.db.insert_data(query, data)

        # Update the paired buy transaction
        update_query = "UPDATE history SET status = 'completed' WHERE id = ?"
        self.db.update_data(update_query, (pair_id,))

    def manual_adjustment(self, transaction_id, new_status, new_pair_id=None):
        """Manually adjusts a transaction's status and optionally updates the pair ID."""
        query = "UPDATE history SET status = ?"
        data = [new_status]
        if new_pair_id is not None:
            query += ", pair_id = ?"
            data.append(new_pair_id)
        query += " WHERE transaction_id = ?"
        data.append(transaction_id)
        self.db.update_data(query, tuple(data))