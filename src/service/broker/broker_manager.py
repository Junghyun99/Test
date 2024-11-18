class BrokerManager:
    def __init__(self, broker):
        self.broker = broker

      status= ["cancel", "pending", "complete"]

    def get_current_price(self, symbol):
        return self.broker.get_current_price(symbol)

    def place_market_order(self, symbol, quantity, order_type):      
        order_id = self.broker.place_market_order(symbol, quantity, order_type)
        
        count = 0
        while count < 10:
            status = self.broker.get_order_status(order_id)
            if status is "complete":
                break
            elif status is "pending":
                time.sleep(1)
            elif status is "cancel":
                break
            count += 1

        if count is 10:
            self.broker.
        



        return get_current_price

    def place_limit_order(self, symbol, quantity, price, order_type):
        order_id = self.broker.place_limit_order(symbol, quantity, price, order_type)

        return order_id