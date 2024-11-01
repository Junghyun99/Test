# trading_round_calculator.py

class TradingRoundCalculator:
    def __init__(self, initial_buy_price, sell_percentage_list, buy_percentage_list, amount_list):
        """
        매수 초기 가격과 각 차수별 매수/매도 비율, 금액 리스트를 받아 초기화합니다.
        """
        self.initial_buy_price = initial_buy_price
        self.sell_percentage_list = sell_percentage_list
        self.buy_percentage_list = buy_percentage_list
        self.amount_list = amount_list
        self.rounds = []

    def setup_trading_rounds(self):
        """
        각 차수의 매수가, 매도가, 매수 금액을 계산하여 거래 라운드를 설정합니다.
        """
        for i in range(len(self.buy_percentage_list)):
            buy_price = self.calculate_price(self.initial_buy_price, self.buy_percentage_list[i], is_buy=True)
            sell_price = self.calculate_price(self.initial_buy_price, self.sell_percentage_list[i], is_buy=False)
            amount = self.amount_list[i]
            self.rounds.append({
                'buy_price': buy_price,
                'sell_price': sell_price,
                'amount': amount
            })

    @staticmethod
    def calculate_price(base_price, percentage, is_buy):
        """
        기본 가격과 비율을 받아 매수가 또는 매도가를 계산합니다.
        :param base_price: 기준 가격
        :param percentage: 비율 (%)
        :param is_buy: 매수 여부 (True: 매수가, False: 매도가)
        :return: 계산된 가격
        """
        return base_price * (1 - percentage / 100) if is_buy else base_price * (1 + percentage / 100)