# stock_trader.py

import time

class StockTrader:
    def __init__(self, calculator, logger, broker_api, db):
        self.calculator = calculator
        self.logger = logger
        self.broker_api = broker_api
        self.db = db
        self.stack = []

    def load_stack(self, stock_symbol):
        # 데이터베이스에서 스택 로드
        self.stack = self.db.load_stack(stock_symbol)
        if self.stack:
            print(f"{stock_symbol} 스택 로드 완료: {self.stack}")
        else:
            print(f"{stock_symbol} 초기 상태로 시작")

    def save_stack(self, stock_symbol):
        # 현재 스택을 데이터베이스에 저장
        self.db.save_stack(stock_symbol, self.stack)
        print(f"{stock_symbol} 스택 저장 완료: {self.stack}")

    def execute_trade(self, stock_symbol):
        rounds = self.calculator.rounds
        for trading_round in rounds:
            buy_price = trading_round['buy_price']
            sell_price = trading_round['sell_price']
            amount = trading_round['amount']

            current_price = self.broker_api.get_current_price(stock_symbol)

            # 매수 조건 확인
            if current_price <= buy_price:
                transaction_number = self.broker_api.buy(stock_symbol, amount)
                self.logger.log_transaction(stock_symbol, '매수', amount, current_price, transaction_number)
                print(f"{stock_symbol} 매수 완료: 거래번호 {transaction_number}")

                # 거래 완료 여부 확인
                while True:
                    status = self.broker_api.check_transaction_status(transaction_number)
                    if status == "완료":
                        self.stack.append(('매수', amount))
                        print(f"{stock_symbol} 거래 완료: 매수")
                        break
                    elif status == "취소":
                        print(f"{stock_symbol} 거래 취소됨")
                        return
                    time.sleep(1)

            # 매도 조건 확인
            elif current_price >= sell_price:
                transaction_number = self.broker_api.sell(stock_symbol, amount)
                self.logger.log_transaction(stock_symbol, '매도', amount, current_price, transaction_number)
                print(f"{stock_symbol} 매도 완료: 거래번호 {transaction_number}")

                # 거래 완료 여부 확인
                while True:
                    status = self.broker_api.check_transaction_status(transaction_number)
                    if status == "완료":
                        if ('매수', amount) in self.stack:
                            self.stack.remove(('매수', amount))
                        print(f"{stock_symbol} 거래 완료: 매도")
                        break
                    elif status == "취소":
                        print(f"{stock_symbol} 거래 취소됨")
                        return
                    time.sleep(1)