# test_trading_algorithm.py

import pytest
from trading_algorithm import TradingRound, TradingAlgorithm

# TradingRound 클래스 테스트
def test_trading_round():
    round_number = 1
    buy_price = 100
    sell_percentage = 5
    buy_percentage = 3
    quantity = 10

    trading_round = TradingRound(round_number, buy_price, sell_percentage, quantity, buy_percentage)

    assert trading_round.buy_price == 100
    assert trading_round.sell_price == 105.00  # 100 * (1 + 5/100) = 105
    assert trading_round.calculate_next_buy_price() == 97.00  # 100 * (1 - 3/100) = 97


# TradingAlgorithm 클래스 테스트
def test_trading_algorithm():
    initial_buy_price = 100
    sell_percentages = [5, 4.5, 4.2, 4, 3.8, 3.5, 3.3, 3, 2.8, 2.5]  # 각 차수별 매도 퍼센트
    buy_percentages = [3, 2.9, 2.8, 2.7, 2.6, 2.5, 2.4, 2.3, 2.2, 2.1]  # 각 차수별 매수 퍼센트
    quantity = 10
    rounds = 10

    algorithm = TradingAlgorithm(initial_buy_price, sell_percentages, buy_percentages, quantity, rounds)
    algorithm.setup_trading_rounds()

    # 첫 번째 차수 확인
    assert algorithm.trading_rounds[0].buy_price == 100
    assert algorithm.trading_rounds[0].sell_price == 105.00  # 100 * (1 + 5/100)

    # 두 번째 차수 확인
    assert algorithm.trading_rounds[1].buy_price == 97.00  # 100 * (1 - 3/100)
    assert algorithm.trading_rounds[1].sell_price == pytest.approx(101.37, 0.01)  # 97 * (1 + 4.5/100)

    # 마지막 차수 (10차) 확인
    assert algorithm.trading_rounds[9].buy_price == pytest.approx(77.20, 0.01)  # 마지막 차수의 매수가
    assert algorithm.trading_rounds[9].sell_price == pytest.approx(79.13, 0.01)  # 마지막 차수의 매도가


# 테스트 실행: pytest에서 수행될 때 테스트 실행
if __name__ == "__main__":
    pytest.main()