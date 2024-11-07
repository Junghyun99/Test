import requests
from src.interface.broker_api import BrokerAPI

class RealBrokerAPI(BrokerAPI):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.realbroker.com"

    def get_current_price(self, symbol: str) -> float:
        response = requests.get(f"{self.base_url}/price/{symbol}", headers={"Authorization": f"Bearer {self.api_key}"})
        return response.json().get("price")

    def place_market_order(self, symbol: str, quantity: int, order_type: str) -> str:
        response = requests.post(f"{self.base_url}/order/market", json={
            "symbol": symbol,
            "quantity": quantity,
            "type": order_type
        }, headers={"Authorization": f"Bearer {self.api_key}"})
        return response.json().get("order_id")

    def place_limit_order(self, symbol: str, quantity: int, price: float, order_type: str) -> str:
        response = requests.post(f"{self.base_url}/order/limit", json={
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "type": order_type
        }, headers={"Authorization": f"Bearer {self.api_key}"})
        return response.json().get("order_id")

    def get_order_status(self, order_id: str) -> str:
        response = requests.get(f"{self.base_url}/order/status/{order_id}", headers={"Authorization": f"Bearer {self.api_key}"})
        return response.json().get("status")

    def get_order_book(self, symbol: str) -> Tuple[List[Tuple[float, int]], List[Tuple[float, int]]]:
        response = requests.get(f"{self.base_url}/orderbook/{symbol}", headers={"Authorization": f"Bearer {self.api_key}"})
        order_book = response.json()
        return order_book.get("buy_orders"), order_book.get("sell_orders")