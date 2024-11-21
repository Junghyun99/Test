from src.interface.algorithm import Algorithm
from src.util.price_calculator import PriceCalulator
from src.util.enums import QueryOp
from src.model.monitoring_db_model import AlgorithmData, MonitoringData

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

        yaml_data = self.yaml_manager.read(code)
        if yaml_data[0]["orders"][trade_round+1]["order"] != trade_round:
            return
        quantity = PriceCalulator.calculate_quantity(yaml_data[0]["orders"][trade_round+1]["buy_price"], current_price)

        # 매수 또는 매도 조건 확인
        if current_price <= target_buy_price:
            if self.broker_manager.place_market_order(code, quantity, "BUY"):
                price = 1 # 매수 성공한 가격을 찾아야함, 브로커에서 수정
                # self.trade_db_manager. 히스토리 추가, 브로커에서?해도될듯?
                # 다음차수 정보가 있을까? 없으면? 설정한 최대 차수에 걸렸다 치면 그만해야지
                if len(yaml_data[0]["orders"]) > trade_round:
                    next_buy_rate = yaml_data[0]["orders"][trade_round+2]["buy_rate"]
                    next_sell_rate = yaml_data[0]["orders"][trade_round+2]["sell_rate"]
                    next_round = yaml_data[0]["orders"][trade_round+2]["order"]
                    moni = MonitoringData(stock_name, code, self.yaml_manager.COUNTRY_CODE, next_round, price, next_buy_rate, next_sell_rate)
                
                else:
                    moni = MonitoringData(stock_name, code, self.yaml_manager.COUNTRY_CODE, trade_round+1, price, 0, next_sell_rate)
                return AlgorithmData(QueryOp.UPDATE, moni)
            # 매수와 매도 rate와 차수가 전부 일치 안하네
            # 미래 차수와 미래 매수 rate, 현재 차수와 현재 매도 rate


        elif current_price >= target_sell_price:
            result = self.broker_manager.place_market_order(code, quantity, "SELL")
        # 매도 성공시
        else:
            pass