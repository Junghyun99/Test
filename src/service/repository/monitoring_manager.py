from concurrent.futures import ThreadPoolExecutor, as_completed 
import os
from src.service.repository.monitoring_db import MonitoringDB
from src.model.monitoring_db_model import MonitoringData
from src.util.enums import CountryCode, QueryOp

class MonitoringManager:
    COUNTRY_CODE = CountryCode.KR

    def __init__(self, algorithm):
        self.db = MonitoringDB()
        self.algorithm = algorithm

    def read_all_stocks(self, country_code):
        """모니터링 DB에서 모든 종목 읽기"""
        query = "SELECT * FROM monitoring WHERE country_code=?"
        data = (country_code,)
        return self.db.read_data(query, data)

    def add_stock_in_monitoring(self, stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate):
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
 
    def update_stock_in_monitoring(self, stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate):
        query = '''UPDATE INTO monitoring SET trade_round =?, price=?, quantity=?, buy_rate=?, sell_rate=? WHERE code = ?'''
        data = (trade_round, price, quantity, buy_rate, sell_rate, code)
        self.db.update_data(query, data)

    def start_monitoring(self):
        """모든 종목을 멀티 쓰레드로 모니터링"""
        max_core = os.cpu_count()-1
        results = []
        errors = []
        stocks = self.read_all_stocks(self.COUNTRY_CODE.value)
        with ThreadPoolExecutor(max_workers=max_core) as executor:
            futures = [executor.submit(self.algorithm.run_algorithm, MonitoringData(*stock)) for stock in stocks]

            for future in as_completed(futures):
                try:
                    result = future.result() 
                    results.append(result)
                except Exception as e:
                    errors.append(e)
                    
        for result in results:
            if result.QueryOp is QueryOp.UPDATE:
                self.update_stock_in_monitoring(*(result.MonitoringData.to_tuple()))
            elif result.QueryOp is QueryOp.DELETE:
                self.delete_stock_in_monitoring(result.MonitoringData.code)

        
        if errors:
        # 에러 상세 정보 출력
            for error in errors:
                print(f"Error at index {error['index']} with item {error['item']}: {error['error']}")
            raise Exception("One or more errors occurred.")


class MonitoringKRManager(MonitoringManager):
    COUNTRY_CODE = CountryCode.KR

class MonitoringUSManager(MonitoringManager):
    COUNTRY_CODE = CountryCode.US
