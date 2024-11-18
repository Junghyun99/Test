from src.interface.algorithm import Algorithm
from src.util.price_calculator import PriceCalulator


class MagicSplit(Algorithm):
    def __init__(self, broker_api):        
        self.broker_api = broker_api

    def run_algorithm(self, stock_name, code, buy_price, trade_round, buy_rate, sell_rate):    
        # 매수 희망가와 매도 희망가 계산
        target_buy_price = PriceCalulator.calculate_price(buy_price, buy_rate, True)
        target_sell_price = PriceCalulator.calculate_price(buy_price, sell_rate, False)

        # 현재 가격을 API로 받아오기
        current_price = self.broker_api.get_current_price(code)

        # 매수 또는 매도 조건 확인
        if current_price <= desired_buy_price:
            # 매수 API 호출
            success =in self.api_client.buy_stock(code, trade_round, current_price)
            if success:
                print(f"{stock_name} ({code}) - 매수 완료: 가격 {current_price}, 라운드 {trade_round}")
            else:
                print(f"{stock_name} ({code}) - 매수 실패")

        elif current_price >= desired_sell_price:
            # 매도 API 호출
            success = self.api_client.sell_stock(code, trade_round, current_price)
            if success:
                print(f"{stock_name} ({code}) - 매도 완료: 가격 {current_price}, 라운드 {trade_round}")
            else:
                print(f"{stock_name} ({code}) - 매도 실패")

        else:
            print(f"{stock_name} ({code}) - 현재 가격 {current_price}로 매수/매도 조건에 부합하지 않음") 