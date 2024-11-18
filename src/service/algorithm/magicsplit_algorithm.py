from src.interface.algorithm import Algorithm
from src.util.price_calculator import PriceCalulator


class MagicSplit(Algorithm):
    def __init__(self, broker_manager, trade_db_manager, yaml_manager):        
        self.broker_manager = broker_manager
        self.trade_db_manager = trade_db_manager
        self.yaml_manager = yaml_manager

    def _calculate_price(self):
        pass

    def run_algorithm(self, stock_name, code, buy_price, trade_round, buy_rate, sell_rate):    
        # 매수 희망가와 매도 희망가 계산
        target_buy_price = PriceCalulator.calculate_price(buy_price, buy_rate, True)
        target_sell_price = PriceCalulator.calculate_price(buy_price, sell_rate, False)

        # 현재 가격을 API로 받아오기
        current_price = self.broker_manager.get_current_price(code)

        # 매수 또는 매도 조건 확인
        if current_price <= target_buy_price:
result = self.broker_manager.place_market_order(code, quantity, "BUY")
        # 매수 성공시
        self.trade_db_manager. 히스토리 추가       
        yaml의 다음 차수정보 읽어와서
        모니터링 디비 다음차수로 수정 


        elif current_price >= target_sell_price:
            result = self.broker_manager.place_market_order(code, quantity, "SELL")
        # 매도 성공시
        else:
            pass