import random
from datetime import datetime
from
class DummyBrokerAPI(BrokerAPI):
    def __init__(self):
        self.orders = {}  # 거래번호와 상태 저장

    def get_current_price(self, symbol):
        return round(random.uniform(100, 500), 2)

    def place_market_order(self, symbol, quantity, order_type):
        order_id = f"{symbol}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.orders[order_id] = "completed"
        return order_id

    def place_limit_order(self, symbol: str, quantity: int, price: float, order_type: str) -> str:
        order_id = f"{symbol}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.orders[order_id] = "pending"
        return order_id

    def get_order_status(self, order_id: str) -> str:
        return self.orders.get(order_id, "not found")

    def get_order_book(self, symbol: str) -> Tuple[List[Tuple[float, int]], List[Tuple[float, int]]]:
        buy_orders = [(round(random.uniform(100, 500), 2), random.randint(1, 100)) for _ in range(5)]
        sell_orders = [(round(random.uniform(500, 1000), 2), random.randint(1, 100)) for _ in range(5)]
        return sorted(buy_orders, reverse=True), sorted(sell_orders)