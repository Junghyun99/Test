from abc import ABC, abstractmethod


class Algorithm(ABC):   
    @abstractmethod
    def run_algorithm(self, stock_name, code, country_code, trade_round, price, buy_rate, sell_rate):
        """주가 검색"""
        pass