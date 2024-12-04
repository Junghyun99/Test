import time
from src.service.logging.logger_manager import logger_manager

transaction_logger = logger_manager.get_logger('TRANSACTION')

class BrokerManager:
    def __init__(self, broker):
        self.broker = broker
        transaction_logger.log_info("create BrokerManager instance, init")

    def get_current_price(self, symbol):
        price = self.broker.get_current_price(symbol)
 transaction_logger.log_info("get_current_price code %s, price %s", symbol, price)        
        return price

    def place_market_order(self, symbol, quantity, order_type):      
        order_id = self.broker.place_market_order(symbol, quantity, order_type)
        transaction_logger.log_info("place_market_order code %s, quantity %s type %s id %s", symbol, quantity, order_type, order_id)

        result = False
        count = 0
        while count < 10:
            status = self.broker.get_order_status(order_id)
            transaction_logger.log_info("place_market_order status %s, count %s", status, count) 
            if status == "complete":
                result = True
                break
            else : # status is "pending":
                time.sleep(1)
            count += 1

        if count == 10:
            transaction_logger.log_info("place_market_order cancel") 
            self.broker.cancel_order(order_id)
        return result
    # self.trade_db_manager. 히스토리 추가, 브로커에서?해도될듯?

    def place_limit_order(self, symbol, quantity, price, order_type):
        order_id = self.broker.place_limit_order(symbol, quantity, price, order_type)
        transaction_logger.log_info("place_limit_order code %s, quantity %s price %s type %s id %s", symbol, quantity, price, order_type, order_id)

        result = False
        info = ()
        count = 0
        while count < 10:
            status = self.broker.get_order_status(order_id)
            transaction_logger.log_info("place_limit_order status %s, count %s", status, count) 
            if status == "complete":
                info = self.broker.get_order_info(order_id)
                result = True
                break
            else : # status is "pending":
                time.sleep(1)
            count += 1

        if count == 10:
            transaction_logger.log_info("place_limit_order cancel")     
            self.broker.cancel_order(order_id)
        return (result, info)