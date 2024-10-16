class TradingRound:
    def __init__(self, round_number, buy_price, sell_percentage, quantity, buy_percentage):
        self.round_number = round_number
        self.buy_price = buy_price
        self.sell_percentage = sell_percentage
        self.quantity = quantity
        self.buy_percentage = buy_percentage
        self.sell_price = self.calculate_sell_price()

    def calculate_sell_price(self):
        return self.buy_price * (1 + self.sell_percentage / 100)

    def calculate_next_buy_price(self):
        return self.buy_price * (1 - self.buy_percentage / 100)


class TradingAlgorithm:
    def __init__(self, initial_buy_price, sell_percentages, buy_percentages, quantity, rounds=10):
        self.initial_buy_price = initial_buy_price
        self.sell_percentages = sell_percentages
        self.buy_percentages = buy_percentages
        self.quantity = quantity
        self.rounds = rounds
        self.trading_rounds = []

    def setup_trading_rounds(self):
        buy_price = self.initial_buy_price
        for i in range(self.rounds):
            sell_percentage = self._get_percentage(self.sell_percentages, i)
            buy_percentage = self._get_percentage(self.buy_percentages, i)
            trading_round = TradingRound(i + 1, buy_price, sell_percentage, self.quantity, buy_percentage)
            self.trading_rounds.append(trading_round)
            buy_price = trading_round.calculate_next_buy_price()

    def _get_percentage(self, percentage_list, index):
        # 매수/매도 퍼센트 리스트의 길이가 부족할 경우, 마지막 값을 사용
        return percentage_list[index] if index < len(percentage_list) else percentage_list[-1]

    def display_rounds(self):
        for trading_round in self.trading_rounds:
            print(f"{trading_round.round_number}차 매수가: {trading_round.buy_price:.2f}, 매도가: {trading_round.sell_price:.2f}, "
                  f"매수 퍼센트: {trading_round.buy_percentage}%, 매도 퍼센트: {trading_round.sell_percentage}%, 수량: {trading_round.quantity}")

# 초기 매수가 100, 매도 퍼센트와 매수 퍼센트 리스트로 입력
sell_percentages = [5, 4.5, 4.2, 4, 3.8, 3.5, 3.3, 3, 2.8, 2.5]  # 각 차수별 매도 퍼센트
buy_percentages = [3, 2.9, 2.8, 2.7, 2.6, 2.5, 2.4, 2.3, 2.2, 2.1]  # 각 차수별 매수 퍼센트

algorithm = TradingAlgorithm(initial_buy_price=100, sell_percentages=sell_percentages, buy_percentages=buy_percentages, quantity=10, rounds=10)
algorithm.setup_trading_rounds()
algorithm.display_rounds()