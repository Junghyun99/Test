import time

class BrokerManager:
    def __init__(self, broker, logger):
        self.broker = broker
        self.logger = logger
        self.logger.log_info("create BrokerManager instance, init")

    def get_current_price(self, symbol):
        price = self.broker.get_current_price(symbol)
        self.logger.log_info("get_current_price code %s, price %s", symbol, price)        
        return price

    def place_market_order(self, symbol, quantity, order_type):      
        self.logger.log_info("place_market_order %s,  %s, %s", symbol, quantity, order_type)     
        order_id = self.broker.place_market_order(symbol, quantity, order_type)

        self.logger.log_transaction(symbol, order_type, quantity, 0) #todo      

        self.logger.log_info("place_market_order code %s, quantity %s type %s id %s", symbol, quantity, order_type, order_id)

        result = False
        count = 0
        while count < 10:
            status = self.broker.get_order_status(order_id)
            self.logger.log_info("place_market_order status %s, count %s", status, count) 
            if status == "complete":
                result = True
                break
            else : # status is "pending":
                time.sleep(1)
            count += 1

        if count == 10:
            self.logger.log_info("place_market_order cancel") 
            self.broker.cancel_order(order_id)
            result = False

        info = [self.get_current_price(symbol), quantity, order_id]
    
        return result, info
    # self.trade_db_manager. 히스토리 추가, 브로커에서?해도될듯?
    # 시장가 체결 금액 리턴해줘야함

    def place_limit_order(self, symbol, quantity, price, order_type):
        order_id = self.broker.place_limit_order(symbol, quantity, price, order_type)


        self.logger.log_transaction(code, order_type, quantity, price)

        self.logger.log_info("place_limit_order code %s, quantity %s price %s type %s id %s", symbol, quantity, price, order_type, order_id)

        result = False
        count = 0
        while count < 10:
            status = self.broker.get_order_status(order_id)
            self.logger.log_info("place_limit_order status %s, count %s", status, count) 
            if status == "complete":
                info = self.broker.get_order_info(order_id)
                result = True
                break
            else : # status is "pending":
                time.sleep(1)
            count += 1

        if count == 10:
            self.logger.log_info("place_limit_order cancel")     
            self.broker.cancel_order(order_id)
            result = False 
        info = [price, quantity, order_id]
        return result, info