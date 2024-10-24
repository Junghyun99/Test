# dummy_broker_api.py

import random

class DummyBrokerAPI:
    def __init__(self, stock_prices):
        self.stock_prices = stock_prices
        self.transaction_status = {}

    def get_current_price(self, stock_symbol):
        # 더미로 주식 가격을 조회
        return self.stock_prices[stock_symbol]

    def buy(self, stock_symbol, amount):
        transaction_number = random.randint(1000, 9999)
        self.transaction_status[transaction_number] = "펜딩"
        print(f"매수 요청: {stock_symbol} {amount}주, 거래번호: {transaction_number}")
        return transaction_number

    def sell(self, stock_symbol, amount):
        transaction_number = random.randint(1000, 9999)
        self.transaction_status[transaction_number] = "펜딩"
        print(f"매도 요청: {stock_symbol} {amount}주, 거래번호: {transaction_number}")
        return transaction_number

    def check_transaction_status(self, transaction_number):
        # 랜덤으로 거래 상태를 결정
        status = random.choice(["완료", "펜딩", "취소"])
        self.transaction_status[transaction_number] = status
        return status