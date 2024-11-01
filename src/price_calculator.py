class PriceCalculator:
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