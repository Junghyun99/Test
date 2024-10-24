# main.py

import threading
from trading_round_calculator import TradingRoundCalculator
from stock_trader import StockTrader
from dummy_broker_api import DummyBrokerAPI
from trade_logger import TradeLogger
from stock_stack_db import StockStackDB

# 종목별 설정
stocks = {
    "삼성전자": 100,
    "LG전자": 80,
    "SK하이닉스": 120
}

sell_percentages = [5, 4.5, 4.2, 4, 3.8, 3.5, 3.3, 3, 2.8, 2.5]
buy_percentages = [3, 2.9, 2.8, 2.7, 2.6, 2.5, 2.4, 2.3, 2.2, 2.1]
amounts = [1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800]

# 각각의 종목에 대해 StockTrader 인스턴스를 생성
def run_trader(stock_symbol, initial_price, db):
    calculator = TradingRoundCalculator(initial_buy_price=initial_price, 
                                        sell_percentages=sell_percentages, 
                                        buy_percentages=buy_percentages, 
                                        amounts=amounts)
    calculator.setup_trading_rounds()

    logger = TradeLogger()
    broker_api = DummyBrokerAPI(stock_prices={stock_symbol: initial_price})

    # 데이터베이스에서 기존 스택 상태를 불러오기
    stock_trader = StockTrader(calculator, logger, broker_api, db)
    stock_trader.load_stack(stock_symbol)  # 이전 스택 로드

    # 한 번만 거래 판단 후 실행
    stock_trader.execute_trade(stock_symbol=stock_symbol)

    # 스택 상태를 데이터베이스에 저장
    stock_trader.save_stack(stock_symbol)

    logger.display_trade_history()

# SQLite DB 설정
db = StockStackDB()

# 멀티스레드로 각 종목에 대해 StockTrader 실행
threads = []
for stock_symbol, initial_price in stocks.items():
    t = threading.Thread(target=run_trader, args=(stock_symbol, initial_price, db))
    threads.append(t)
    t.start()

# 모든 스레드가 끝날 때까지 대기
for t in threads:
    t.join()

print("모든 종목의 거래가 완료되었습니다.")