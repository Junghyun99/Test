import random
import time
from datetime import datetime
from src.interface.broker_api import BrokerAPI

class DummyBrokerAPI(BrokerAPI):
    def __init__(self):
        self.number = 0
        self.order = {}

    def generate_order_id(index):
        return f"TX_{index}"
    
    def get_current_price(self, symbol):
        return round(random.uniform(100, 500), 2)

    def place_market_order(self, symbol, quantity, order_type):
        order_id = self.generate_order_id(self.number)
        status= ["pending", "complete"]
        self.order[order_id] = random.choice(status)
        time.sleep(random.randint(0,9))
        self.number = self.number + 1
        return order_id

    def place_limit_order(self, symbol, quantity, price, order_type):
        order_id = self.generate_order_id(self.number)
        status= ["pending", "complete"]
        self.order[order_id] = random.choice(status)
        time.sleep(random.randint(0,9))
        self.number = self.number + 1
        return order_id

    def get_order_status(self, order_id):
        if order_id not in self.order:
            return "invalid"
        if self.order[order_id] == "complete":
            return "complete"

        status= ["cancel", "pending", "complete"]
        re_status = random.choice(status)
        self.order[order_id] = re_status
        return re_status

    def get_order_book(self, symbol):
        buy_orders = [(round(random.uniform(100, 500), 2), random.randint(1, 100)) for _ in range(5)]
        sell_orders = [(round(random.uniform(500, 1000), 2), random.randint(1, 100)) for _ in range(5)]
        return sorted(buy_orders, reverse=True), sorted(sell_orders)


    def amend_order(self, order_id, new_price):
        if order_id not in self.order:
            return False
        if self.order[order_id] is not "pending":
            return False

        return True

    def cancel_order(self, order_id):
        if order_id not in self.order:
            return False
        if self.order[order_id] is not "pending":
            return False

        self.order[order_id] = "cancel"
        return True