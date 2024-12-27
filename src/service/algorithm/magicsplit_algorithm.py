from threading import current_thread
from src.interface.algorithm import Algorithm
from src.util.price_calculator import PriceCalculator
from src.util.enums import QueryOp
from src.model.monitoring_db_model import AlgorithmData, MonitoringData

   
class MagicSplit(Algorithm):
    def __init__(self, broker_manager, trade_db_manager, stock_round_yaml_manager, logger):        
        self.broker_manager = broker_manager
        self.trade_db_manager = trade_db_manager
        self.stock_round_yaml_manager = stock_round_yaml_manager
        self.logger = logger
        self.logger.log_info("MGST 0. init")
        self.set_transaction_dummy()

    def set_transaction_dummy(self):
        last_tx = self.trade_db_manager.last_transaction_id()
        
        if last_tx:
            number = int(last_tx.split("_")[1])
            self.broker_manager.set_dummy_number(number+1)
  

    def _calculate_price(self, buy_price, buy_rate, sell_rate):
        target_buy_price = PriceCalculator.calculate_price(buy_price, buy_rate, True)
        target_sell_price = PriceCalculator.calculate_price(buy_price, sell_rate, False)
        
        return target_buy_price, target_sell_price
    
    def _get_prev_trade_round(self, code, trade_round):
        info = self.trade_db_manager.get_trade_round(code, trade_round)[0]
        self.logger.log_info("MGST 4-3. prev_trade_round") 
        self.logger.log_debug(" - input code %s, trade_round %s",code, trade_round)
        self.logger.log_debug(" - output price %s, quantity %s",info["price"], info["amount"])
        return info["price"], info["amount"] # price, quantity

    def _try_buy_stock_zero(self, current_price, moniData:MonitoringData):
        yaml_data = self.stock_round_yaml_manager.read_by_id(moniData.code)
        self.logger.log_info("MGST 2-1. BUY_STOCK_ZERO")
        self.logger.log_debug("  - price %s, moniData %s, yaml %s",current_price, moniData, yaml_data)

        quantity = PriceCalculator.calculate_quantity(yaml_data[0]["orders"][0]["buy_price"], current_price)
        status, info = self.broker_manager.place_market_order(moniData.code, quantity, "BUY")

        if status is False:
            self.logger.log_error("place_market_order status false")
            return AlgorithmData(QueryOp.DEFAULT, MonitoringData(*MonitoringData.DUMMY))


        
        self.trade_db_manager.record_buy_transaction(moniData.stock_name, moniData.code, info[2], moniData.country_code, 1, info[0], info[1])    
        moniData.price = info[0] # 실제 거래 매수 금액
        moniData.quantity = info[1] # 실제 거래 매수 수량
        moniData.buy_rate = yaml_data[0]["orders"][1]["buy_rate"]
        moniData.sell_rate = yaml_data[0]["orders"][1]["sell_rate"]
        moniData.trade_round = yaml_data[0]["orders"][1]["order"]
        self.logger.log_info("MGST 2-2. BUY_STOCK_ZERO success, moniData %s",moniData)
        return AlgorithmData(QueryOp.UPDATE, moniData)

    def _try_buy_stock(self, current_price, moniData:MonitoringData):
        yaml_data = self.stock_round_yaml_manager.read_by_id(moniData.code)
        self.logger.log_info("MGST 3-1. BUY_STOCK")
        self.logger.log_debug("  - price %s, moniData %s, yaml %s",current_price, moniData, yaml_data)

        if yaml_data[0]["orders"][moniData.trade_round-1]["order"] != moniData.trade_round:
            self.logger.log_warning(" - buy_stock, round %s != moni round %s",yaml_data[0]["orders"][moniData.trade_round-1]["order"], moniData.trade_round)
            return AlgorithmData(QueryOp.DEFAULT, MonitoringData(*MonitoringData.DUMMY))
        if len(yaml_data[0]["orders"]) <= moniData.trade_round: # 설정된 마지막 차수라는 뜻
            self.logger.log_warning(" - buy_stock, len %s != moni round %s",len(yaml_data[0]["orders"]), moniData.trade_round)
            return AlgorithmData(QueryOp.DEFAULT, MonitoringData(*MonitoringData.DUMMY))
        
        quantity = PriceCalculator.calculate_quantity(yaml_data[0]["orders"][moniData.trade_round-1]["buy_price"], current_price)
        status, info = self.broker_manager.place_market_order(moniData.code, quantity, "BUY")
            
        if status is False:
            self.logger.log_error("place_market_order status false")
            return AlgorithmData(QueryOp.DEFAULT, MonitoringData(*MonitoringData.DUMMY))


        self.trade_db_manager.record_buy_transaction(moniData.stock_name, moniData.code, info[2], moniData.country_code, moniData.trade_round, info[0], info[1])   
        moniData.price = info[0] # 실제 거래 매수 금액
        moniData.quantity = info[1] # 실제 거래 매수 수량
        moniData.buy_rate = yaml_data[0]["orders"][moniData.trade_round]["buy_rate"]
        moniData.sell_rate = yaml_data[0]["orders"][moniData.trade_round]["sell_rate"]
        moniData.trade_round = yaml_data[0]["orders"][moniData.trade_round]["order"]
        self.logger.log_info("MGST 3-2. buy_stock success, moniData %s",moniData)
        return AlgorithmData(QueryOp.UPDATE, moniData)
        
    def _try_sell_stock(self, current_price, moniData:MonitoringData):
        yaml_data = self.stock_round_yaml_manager.read_by_id(moniData.code)
        
        self.logger.log_info("MGST 4-1. SELL_STOCK")
        self.logger.log_debug("  - price %s, moniData %s, yaml %s",current_price, moniData, yaml_data)

        
        if yaml_data[0]["orders"][moniData.trade_round-1]["order"] != moniData.trade_round:
            self.logger.log_warning(" - sell_stock, round %s != moni round %s",yaml_data[0]["orders"][moniData.trade_round-1]["order"], moniData.trade_round)
            return AlgorithmData(QueryOp.DEFAULT, MonitoringData(*MonitoringData.DUMMY))
        
        status, info = self.broker_manager.place_market_order(moniData.code, moniData.quantity, "SELL")
            
        if status is False:
            self.logger.log_error("place_market_order status false")
            return AlgorithmData(QueryOp.DEFAULT, MonitoringData(*MonitoringData.DUMMY))
        



             


        if moniData.trade_round  == 1: # 1 차수 매도 성공, 모니터링 DB에서 0차수로 변경
            self.logger.log_info("MGST 4-2. sell_stock, lst round sell..")
            self.trade_db_manager.record_sell_transaction(moniData.stock_name, moniData.code, info[2], moniData.country_code, moniData.trade_round, info[0], info[1]) 

            return AlgorithmData(QueryOp.DELETE, moniData)
        
        # 이전 차수에 산 매수금액과 수량
        price, quantity  = self._get_prev_trade_round(moniData.code, moniData.trade_round - 1)
        self.trade_db_manager.record_sell_transaction(moniData.stock_name, moniData.code, info[2], moniData.country_code, moniData.trade_round, info[0], info[1])      
        moniData.trade_round = yaml_data[0]["orders"][moniData.trade_round-2]["order"]
        moniData.price = price
        moniData.quantity = quantity
        moniData.buy_rate = yaml_data[0]["orders"][moniData.trade_round-2]["buy_rate"]
        moniData.sell_rate = yaml_data[0]["orders"][moniData.trade_round-2]["sell_rate"]
        self.logger.log_info("MGST 4-4. sell_stock success, moniData %s",moniData)
        return AlgorithmData(QueryOp.UPDATE, moniData)
    
    def run_algorithm(self, moniData:MonitoringData):
        self.logger.log_info("*********  %s *********",current_thread().name)

        self.logger.log_info("MGST 1. RUN_ALGORITHM, %s",moniData.code)
        try:
            target_buy_price, target_sell_price = self._calculate_price(moniData.price, moniData.buy_rate, moniData.sell_rate)
            
            current_price = self.broker_manager.get_current_price(moniData.code)
            
            self.logger.log_debug("  - moni %s", moniData)
            self.logger.log_debug("  - current price %s, target_buy_price  %s, target_sell_price %s",current_price, target_buy_price, target_sell_price)
      
            result = None
            if current_price == 0:
                result =  AlgorithmData(QueryOp.DEFAULT, MonitoringData(*MonitoringData.DUMMY))
            elif moniData.trade_round == 0 and current_price <= target_buy_price:
                result =  self._try_buy_stock_zero(current_price, moniData)
            elif current_price <= target_buy_price:
                result =  self._try_buy_stock(current_price, moniData)
            elif current_price >= target_sell_price:
                result =  self._try_sell_stock(current_price, moniData)
            else:
                result =  AlgorithmData(QueryOp.DEFAULT, MonitoringData(*MonitoringData.DUMMY))
        except Exception as e:
            self.logger.log_error("MGST error %s", e, exc_info=True)
            result =  AlgorithmData(QueryOp.DEFAULT, MonitoringData(*MonitoringData.DUMMY))
        finally:                            
            self.logger.proc_log()
            self.broker_manager.logger.proc_log()    
            
        return result
'''
1차수 매수 가격, 매수 5% 매도 5%, 수량가액
2차수 매수 가격, 매수 5% 매도 5%, 수량가액
3차수 매수 가격, 매수 5% 매도 5%, 수량가액
4차수 매수 가격, 매수 5% 매도 5%, 수량가액

3차수까지 매수한 상태, 4차수를 매수하냐, 3차수를 매도하냐의 조건
3차수 매도 조건 : 3차수 매도률과 3차수 매수 가격, 수량은 3차수 수량 전부
4차수 매수 조건 : 3차수 매수률과 3차수 매수 가격, 수량은 3차수 수량가액만큼
'''