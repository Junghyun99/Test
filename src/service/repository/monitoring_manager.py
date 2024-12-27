from concurrent.futures import ThreadPoolExecutor, as_completed 
import os
from src.service.repository.monitoring_db import MonitoringDB
from src.model.monitoring_db_model import MonitoringData
from src.util.enums import CountryCode, QueryOp

from src.util.yaml_manager import YamlManager

class MonitoringManager(YamlManager):
    COUNTRY_CODE = CountryCode.KR
    
    def __init__(self, algorithm, logger, config_file):
        super().__init__(config_file)
        self._set_monitoring_db_yaml_config()
        self.db = MonitoringDB(logger, self.monitoring_db_file)
        self.algorithm = algorithm
        self.logger = logger
        self.logger.log_info("Moni 0. init")

    def read_all_stocks(self, country_code):
        """모니터링 DB에서 모든 종목 읽기"""
        query = "SELECT * FROM monitoring WHERE country_code=?"
        data = (country_code,)       
        return self.db.read_data(query, data)

    def add_stock_in_monitoring(self, id, stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate):
        """새로운 종목 추가"""
        query = '''INSERT INTO monitoring (stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        data = (stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate)
        
        self.db.insert_data(query, data)

    def delete_stock_in_monitoring(self, code):
        """종목 삭제"""
        query = '''DELETE FROM monitoring WHERE code = ?'''
        data = (code,)
        
        self.db.delete_data(query, data)
 
    def update_stock_in_monitoring(self, id, stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate):
        query = '''UPDATE monitoring SET trade_round =?, price=?, quantity=?, buy_rate=?, sell_rate=? WHERE code = ?'''
        data = (trade_round, price, quantity, buy_rate, sell_rate, code)
        
        self.db.update_data(query, data)
        

    def start_monitoring(self):
        """모든 종목을 멀티 쓰레드로 모니터링"""
        try:
            max_core = os.cpu_count()-1
            results = []
            errors = []
            stocks = self.read_all_stocks(self.COUNTRY_CODE.value)
            
            self.logger.log_info("Moni 1. start_monitoring")
            self.logger.log_debug("  - max_core %s, stock count %s", max_core, len(stocks))
            with ThreadPoolExecutor(max_workers=max_core) as executor:
                futures = [executor.submit(self.algorithm.run_algorithm, MonitoringData(**stock)) for stock in stocks]

                for future in as_completed(futures):
                    try:
                        result = future.result() 
                        results.append(result)
                    except Exception as e:
                        errors.append(e)            
            print(results)
            if len(errors) == 0:        
                for result in results:
                    if result.QueryOp is QueryOp.UPDATE:
                         

                        self.logger.log_info("Moni 2-1. update %s", result.MonitoringData.to_tuple())          

                        self.update_stock_in_monitoring(*(result.MonitoringData.to_tuple()))
                    elif result.QueryOp is QueryOp.DELETE:
 
                        self.logger.log_info("Moni 2-2. delete %s", result.MonitoringData.code)                     
                        self.delete_stock_in_monitoring(result.MonitoringData.code)

        except Exception as e:
            self.logger.log_error("Moni 2-3. error %s", e) 
        finally:
            if errors:
                for err in errors:                            

                    self.logger.log_error("Moni 2. error %s", err)
            
            self.logger.log_info("Moni 3. end")                            
            self.logger.proc_log()
            self.algorithm.broker_manager.logger.proc_log()
            



class MonitoringKRManager(MonitoringManager):
    COUNTRY_CODE = CountryCode.KR

class MonitoringUSManager(MonitoringManager):
    COUNTRY_CODE = CountryCode.US
