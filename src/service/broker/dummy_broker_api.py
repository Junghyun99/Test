import threading
import random
import time
from src.interface.broker_api import BrokerAPI
import yfinance as yf

class DummyBrokerAPI(BrokerAPI):
    def __init__(self):
        self.number = 0
        self.order = {}
        self.lock = threading.Lock()  # Lock 객체 생성

    def set_number(self, number):
        self.number = number
        

    def generate_order_id(self,index):
        return f"TX_{index}"
    
    def get_current_price(self, symbol):
        """
        Yahoo Finance에서 현재 주가를 가져옵니다.
        :param symbol: 주식 티커 심볼 (e.g., "AAPL", "MSFT")
        :return: 현재 주가(float) 또는 에러 메시지(str)
        """
        try:
            stock = yf.Ticker(symbol)
            current_price = stock.history(period="1d")["Close"].iloc[-1]
            return round(current_price, 2)
        except Exception as e:
            print(f"Error fetching data for symbol '{symbol}': {e}")
        return round(random.uniform(100, 500), 2)

    def place_market_order(self, symbol, quantity, order_type):

        with self.lock:  # Lock을 사용하여 코드 블록 동기화
            order_id = self.generate_order_id(self.number)
            self.number += 1  # self.number를 안전하게 증가
       
        status= ["pending", "complete"]
        self.order[order_id] = random.choice(status)
        time.sleep(random.randint(0,9))
        
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
    
    def get_order_info(self, order_id):
        price = random.randint(100, 5000)
        quantity = random.randint(10, 50)
        return (price, quantity)
    
    def get_order_book(self, symbol):
        buy_orders = [(round(random.uniform(100, 500), 2), random.randint(1, 100)) for _ in range(5)]
        sell_orders = [(round(random.uniform(500, 1000), 2), random.randint(1, 100)) for _ in range(5)]
        return sorted(buy_orders, reverse=True), sorted(sell_orders)


    def amend_order(self, order_id, new_price):
        if order_id not in self.order:
            return False
        if self.order[order_id] != "pending":
            return False

        return True

    def cancel_order(self, order_id):
        if order_id not in self.order:
            return False
        if self.order[order_id] != "pending":
            return False

        self.order[order_id] = "cancel"
        return True