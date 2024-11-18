from src.interface.algorithm import Algorithm
from src.util.

class MagicSplit(Algorithm):
    def __init__(self, broker_api):
        
        self.broker_api = broker_api

    def fetch_data(self, stock_name, code, buy_price, trade_round, buy_rate, sell_rate):
        """
        주어진 종목에 대한 매수/매도 결정을 처리하는 메인 함수.
        :param stock_name: 종목 이름
        :param code: 종목 코드
        :param buy_price: 매수 기준 가격
        :param trade_round: 라운드 정보
        :param buy_rate: 매수 희망가를 결정하는 비율
        :param sell_rate: 매도 희망가를 결정하는 비율
        """
        # 매수 희망가와 매도 희망가 계산
        desired_buy_price = buy_price * (1 - buy_rate / 100)
        desired_sell_price = buy_price * (1 + sell_rate / 100)

        # 현재 가격을 API로 받아오기
        current_price = self.api_client.get_current_price(code)

        # 매수 또는 매도 조건 확인
        if current_price <= desired_buy_price:
            # 매수 API 호출
            success = self.api_client.buy_stock(code, trade_round, current_price)
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