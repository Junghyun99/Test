from abc import ABC, abstractmethod


class BrokerAPI(ABC):   
    @abstractmethod
    def get_current_price(self, symbol):
        """주가 검색"""
        pass

    @abstractmethod
    def place_market_order(self, symbol, quantity, order_type):
        """시장가 매수/매도 (order_type은 'buy' 또는 'sell')"""
        pass

    @abstractmethod
    def place_limit_order(self, symbol, quantity, price, order_type):
        """지정가 매수/매도 (order_type은 'buy' 또는 'sell')"""
        pass

    @abstractmethod
    def get_order_status(self, order_id):
        """거래내역 검색"""
        pass

    @abstractmethod
    def get_order_book(self, symbol):
        """호가 검색 (매수호가와 매도호가 리스트 반환)"""
        pass