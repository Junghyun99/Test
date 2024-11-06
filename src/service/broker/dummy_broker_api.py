import random
import time
from datetime import datetime
from
class DummyBrokerAPI(BrokerAPI):
    def __init__(self):
        self.number = 0
        self.order = []

    def get_current_price(self, symbol):
        return round(random.uniform(100, 500), 2)

    def place_market_order(self, symbol, quantity, order_type):
        order_id = self.number
        status= ["pending", "complete"]
        self.order[order_id] = random.choice(status)
        time.sleep(random.randint(0,9))
        self.number++
        return order_id

    def place_limit_order(self, symbol, quantity, price, order_type):
        order_id = self.number
        status= ["pending", "complete"]
        self.order[order_id] = random.choice(status)
        time.sleep(random.randint(0,9))
        self.number++
        return order_id

    def get_order_status(self, order_id):
        if self.number < order_id:
            return "invalid"

        status= ["cancel", "pending", "complete"]
        return random.choice(status)

    def get_order_book(self, symbol: str) -> Tuple[List[Tuple[float, int]], List[Tuple[float, int]]]:
        buy_orders = [(round(random.uniform(100, 500), 2), random.randint(1, 100)) for _ in range(5)]
        sell_orders = [(round(random.uniform(500, 1000), 2), random.randint(1, 100)) for _ in range(5)]
        return sorted(buy_orders, reverse=True), sorted(sell_orders)


    def amend_order(self, order_id, new_quantity, new_price):
        order = self.orders.get(order_id)
        if order and order["status"] == "대기 중":
            order["quantity"] = new_quantity
            if new_price is not None:
                order["price"] = new_price
            return True
        return False

    def cancel_order(self, order_id):
        order = self.orders.get(order_id)
        if order and order["status"] == "대기 중":
            order["status"] = "취소됨"
            return True
        return False