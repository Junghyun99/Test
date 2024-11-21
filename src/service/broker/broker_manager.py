import time

class BrokerManager:
    def __init__(self, broker):
        self.broker = broker
    def get_current_price(self, symbol):
        return self.broker.get_current_price(symbol)

    def place_market_order(self, symbol, quantity, order_type):      
        order_id = self.broker.place_market_order(symbol, quantity, order_type)
        result = False
        count = 0
        while count < 10:
            status = self.broker.get_order_status(order_id)
            if status is "complete":
                result = True
                break
            else : # status is "pending":
                time.sleep(1)
            count += 1

        if count is 10:
            self.broker.cancel_order(order_id)
        return result

    def place_limit_order(self, symbol, quantity, price, order_type):
        order_id = self.broker.place_limit_order(symbol, quantity, price, order_type)

        result = False
        count = 0
        while count < 10:
            status = self.broker.get_order_status(order_id)
            if status is "complete":
                result = True
                break
            else : # status is "pending":
                time.sleep(1)
            count += 1

        if count is 10:     
            self.broker.cancel_order(order_id)
        return result