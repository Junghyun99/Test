from concurrent.futures import ThreadPoolExecutor, as_completed 
import os
from src.service.repository.monitoring_db import MonitoringDB
from src.util.enums import CountryCode

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

    def add_stock_in_monitoring(self, stock_name, code, country_code, trade_round, price, buy_rate, sell_rate):
        """새로운 종목 추가"""
        query = '''INSERT INTO monitoring (stock_name, code, country_code, trade_round, price, buy_rate, sell_rate)
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        data = (stock_name, code, country_code, trade_round, price, buy_rate, sell_rate)
        self.db.insert_data(query, data)

    def delete_stock_in_monitoring(self, code):
        """종목 삭제"""
        query = "DELETE FROM monitoring WHERE code = ?"
        data = (code,)
        self.db.delete_data(query, data)
 
    def update_stock_in_monitoring(self):
        pass

    def start_monitoring(self):
        """모든 종목을 멀티 쓰레드로 모니터링"""
        max_core = os.cpu_count()-1
        results = []
        stocks = self.read_all_stocks(self.COUNTRY_CODE.value)
        with ThreadPoolExecutor(max_workers=max_core) as executor:
            # 각 ID에 대해 fetch_data 작업을 비동기로 제출
            futures = [executor.submit(self.algorithm.fetch_func, stock) for stock in stocks]
            # *stock 으로 풀어서 인풋할수도
            # 작업 완료를 기다리며 결과 수집
            for future in as_completed(futures):
                try:
                    result = future.result()  # 작업 결과 가져오기
                    # 매수매도에 따라 모니터링 객체를 업데이트
                    results.append(result)
                except Exception as e:
                    print(e)
        for result in results:
            if result.QueryOp is QueryOp.


class MonitoringKRManager(MonitoringManager):
    COUNTRY_CODE = CountryCode.KR

class MonitoringUSManager(MonitoringManager):
    COUNTRY_CODE = CountryCode.US
