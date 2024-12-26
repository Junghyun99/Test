from src.service.repository.stock_trade_db import StockTradeDB

from src.util.enums import CountryCode

from src.util.yaml_manager import YamlManager

class TradeDBManager(YamlManager):
    def __init__(self, logger, config_file):
        super().__init__(config_file)
        self._set_stock_trade_db_yaml_config()
        self.db = StockTradeDB(logger, self.stock_trade_db_file)
        self.logger = logger
        

        self.logger.log_info("TradeDBManager init")

    def convert_country_code(self, country_code):
        if country_code == CountryCode.KR:
            return "KR"
        if country_code == CountryCode.US:
            return "US"
  
    # Reading Methods
    def last_transaction_id(self):
        query = '''
            SELECT transaction_id FROM history 
        '''
        result = self.db.read_data(query)
        if result:
            return result[-1][0]
        return None

    def get_trade_round(self, code, round):
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
        data = (stock_name, code, transaction_id, self.convert_country_code(country_code), trade_round, 'buy', price, amount, 'processing', 0)
  
        self.db.insert_data(query, data)
        
    
        result = self.db.read_data("SELECT id FROM history WHERE transaction_id=?", (transaction_id,))
        return result[0][0]


    def record_sell_transaction(self, stock_name, code, transaction_id, country_code, trade_round, price, amount):
        instance = self.get_last_round_data(code)
        
        query = '''INSERT INTO history (stock_name, code, transaction_id, country_code, trade_round, trade_type, price, amount, status, pair_id) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        data = (stock_name, code, transaction_id, self.convert_country_code(country_code), trade_round, 'sell', price, amount, 'completed', instance['id'])
  
        self.db.insert_data(query, data)

        query = '''
            SELECT id FROM history 
            WHERE code = ? AND transaction_id = ?
        '''  
        id = self.db.read_data(query, (code, transaction_id))

        # Update the paired buy transaction
        update_query = "UPDATE history SET status = 'COMPLETED' AND pair_id =? WHERE id = ?"
        self.db.update_data(update_query, (id,instance['pair_id']))

        return instance['id']


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


    def close_db(self):
        self.logger.log_info("TradeDBManager db close")
        self.db.close()