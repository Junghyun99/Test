from src.interface.algorithm import Algorithm
from src.util.price_calculator import PriceCalulator


class MagicSplit(Algorithm):
    def __init__(self, broker, trade_db_manager, yaml_manager):        
        self.broker = broker
        self.trade_db_manager = trade_db_manager
        self.yaml_manager = yaml_manager

    def _calculate_price(self):
        pass

    def run_algorithm(self, stock_name, code, buy_price, trade_round, buy_rate, sell_rate):    
        # 매수 희망가와 매도 희망가 계산
        target_buy_price = PriceCalulator.calculate_price(buy_price, buy_rate, True)
        target_sell_price = PriceCalulator.calculate_price(buy_price, sell_rate, False)

        # 현재 가격을 API로 받아오기
        current_price = self.broker.get_current_price(code)

        # 매수 또는 매도 조건 확인
        if current_price <= target_buy_price:
self.broker.place_market_order(code, quantity, "BUY")
        elif current_price >= target_sell_price:
            self.broker.place_market_order(code, quantity, "SELL")
        else:
            pass