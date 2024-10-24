# trading_round_calculator.py

class TradingRoundCalculator:
    def __init__(self, initial_buy_price, sell_percentages, buy_percentages, amounts):
        self.initial_buy_price = initial_buy_price
        self.sell_percentages = sell_percentages
        self.buy_percentages = buy_percentages
        self.amounts = amounts
        self.rounds = []

    def setup_trading_rounds(self):
        for i in range(len(self.buy_percentages)):
            buy_price = self.initial_buy_price * (1 - self.buy_percentages[i] / 100)
            sell_price = self.initial_buy_price * (1 + self.sell_percentages[i] / 100)
            amount = self.amounts[i]
            self.rounds.append({
                'buy_price': buy_price,
                'sell_price': sell_price,
                'amount': amount
            })