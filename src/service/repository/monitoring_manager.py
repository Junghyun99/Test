from concurrent.futures import ThreadPoolExecutor
import time

def main():
data_ids = [1, 2, 3, 4, 5] # 작업할 ID 목록
results = []

# 스레드 풀을 생성하고 스레드를 관리
with ThreadPoolExecutor(max_workers=3) as executor:
    # 각 ID에 대해 fetch_data 작업을 비동기로 제출
    futures = [executor.submit(fetch_data, data_id) for data_id in data_ids]

    # 작업 완료를 기다리며 결과 수집
    for future in as_completed(futures):
        result = future.result()  # 작업 결과 가져오기
        results.append(result)
        print(result)

print("All tasks completed.")



import threading
import time
from monitoring_db import MonitoringDB  # MonitoringDB 클래스는 앞서 정의한 것 사용
import requests  # 종목의 현재 가격을 읽기 위한 요청 모듈

class MonitoringManager:
    def __init__(self):
        self.db = MonitoringDB()
        self.threads = []

    def load_all_stocks(self):
        """모니터링 DB에서 모든 종목 읽기"""
        query = "SELECT * FROM monitoring"
        return self.db.read_data(query)

    def add_stock(self, stock_name, code, country_code, trade_round, price, buy_rate, sell_rate):
        """새로운 종목 추가"""
        query = '''INSERT INTO monitoring (stock_name, code, country_code, trade_round, price, buy_rate, sell_rate)
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        data = (stock_name, code, country_code, trade_round, price, buy_rate, sell_rate)
        self.db.insert_data(query, data)

    def delete_stock(self, stock_id):
        """종목 삭제"""
        query = "DELETE FROM monitoring WHERE id = ?"
        data = (stock_id,)
        self.db.delete_data(query, data)

    def start_monitoring(self):
        """모든 종목을 멀티 쓰레드로 모니터링"""
        stocks = self.load_all_stocks()
        for stock in stocks:
            thread = threading.Thread(target=self.monitor_stock, args=(stock,))
            thread.start()
            self.threads.append(thread)

        # 모든 쓰레드의 종료를 기다림
        for thread in self.threads:
            thread.join()

    def monitor_stock(self, stock):
        """개별 종목을 모니터링하는 함수 (쓰레드별 실행)"""
        stock_name, code, country_code, trade_round, price, buy_rate, sell_rate = stock[1:7]
        buy_price = price * (1 - buy_rate / 100)
        sell_price = price * (1 + sell_rate / 100)

        attempts = 0
        while attempts < 10:
            current_price = self.get_current_price(code)

            if current_price >= sell_price:
                self.execute_trade(stock, "sell", current_price)
                return
            elif current_price <= buy_price:
                self.execute_trade(stock, "buy", current_price)
                return
            else:
                time.sleep(3)  # 3초 대기
                attempts += 1

        # 거래가 펜딩 상태에서 계속 실패한 경우 거래 취소
        print(f"{stock_name} 거래 취소: 최대 시도 횟수 초과")

    def get_current_price(self, code):
        """현재 종목의 가격을 API를 통해 읽기 (여기서는 가상 API 요청 예제)"""
        # 실제 구현에서는 적절한 API를 사용하여 가격을 가져와야 함
        response = requests.get(f"https://api.stockprice.com/{code}")
        return response.json().get("price", 0)

    def execute_trade(self, stock, action, current_price):
        """매수 또는 매도 실행 후 모니터링 DB 업데이트"""
        stock_id = stock[0]
        query = "UPDATE monitoring SET price = ?, trade_round = trade_round + 1 WHERE id = ?"
        data = (current_price, stock_id)
        self.db.update_data(query, data)
        print(f"{stock[1]} {action} 성공: 가격 {current_price}로 {action}")