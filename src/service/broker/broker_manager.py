class BrokerManager:
    def __init__(self, broker):
        self.broker = broker

      status= ["cancel", "pending", "complete"]

    def get_current_price(self, symbol):
        return self.broker.get_current_price(symbol)

    def place_market_order(self, symbol, quantity, order_type):      
        order_id = self.broker.place_market_order(symbol, quantity, order_type)
        if 


        return get_current_price

    def place_limit_order(self, symbol, quantity, price, order_type):
        order_id = self.broker.place_limit_order(symbol, quantity, price, order_type)

        return order_id