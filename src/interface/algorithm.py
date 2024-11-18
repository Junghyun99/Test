from abc import ABC, abstractmethod


class Algorithm(ABC):   
    @abstractmethod
    def run_algorithm(self, stock_name, code, country_code, trade_round, price, buy_rate, sell_rate):
        """쓰레드가 돌릴 함수"""
        pass