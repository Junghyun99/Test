# trade_logger.py

class TradeLogger:
    def __init__(self):
        self.trade_history = []

    def log_transaction(self, stock_symbol, action, amount, price, transaction_number):
        self.trade_history.append({
            'stock_symbol': stock_symbol,
            'action': action,
            'amount': amount,
            'price': price,
            'transaction_number': transaction_number
        })

    def display_trade_history(self):
        print("\n거래 기록:")
        for trade in self.trade_history:
            print(f"종목: {trade['stock_symbol']}, 액션: {trade['action']}, 수량: {trade['amount']}, 가격: {trade['price']}, 거래번호: {trade['transaction_number']}")