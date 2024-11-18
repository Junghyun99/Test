from abc import ABC, abstractmethod


class Algorithm(ABC):   
    @abstractmethod
    def run_algorithm(self, symbol):
        """주가 검색"""
        pass

    @abstractmethod
    def place_market_order(self, symbol, quantity, order_type):
        """시장가 매수/매도 (order_type은 'buy' 또는 'sell')"""
        pass 