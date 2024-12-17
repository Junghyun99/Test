import requests
from src.interface.broker_api import BrokerAPI

class RealBrokerAPI(BrokerAPI):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.realbroker.com"

    def get_current_price(self, symbol: str) -> float:
        pass

    def place_market_order(self, symbol: str, quantity: int, order_type: str) -> str:
        pass

    def place_limit_order(self, symbol: str, quantity: int, price: float, order_type: str) -> str:
        pass

    def get_order_status(self, order_id: str) -> str:
        pass

    def get_order_book(self, symbol: str):
        pass