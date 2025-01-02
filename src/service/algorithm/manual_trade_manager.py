from src.util.price_calculator import PriceCalculator
from src.interface.algorithm import Algorithm
from src.util.enums import CountryCode

class ManualTradeManager(Algorithm):
    COUNTRY_CODE = CountryCode.KR

    def __init__(self, monitoring_manager, broker_manager, trade_db_manager, logger):      
        self.monitoring_manager = monitoring_manager
        self.broker_manager = broker_manager
        self.trade_db_manager = trade_db_manager
        self.logger = logger


       

    def handle_trade(self, code, stock_name, buy_price):       
        self.logger.info(f"Manual trade initiated for {code}")

        # 진행 중인지 확인       
        existing_stock =    self.monitoring_manager.check_already_existing_monitoring(code)

        if existing_stock:
            return
            # 모니터링중인 종목은 수동거래 안됨

            # 진행 중인 종목이면 모니터링에서 제거 및 자동매매 종료
            self.logger.info(f"Stopping auto-trade for {code}.")
            self.monitoring_manager.delete_stock_in_monitoring(code)
        else:
            self.logger.info(f"No active monitoring found for {code}.")


        current_price = self.broker_manager.get_current_price(code)
        quantity = PriceCalculator.calculate_quantity(buy_price, current_price)


        # 브로커를 통해 거래 시도
        self.logger.info(f"Attempting to place a {order_type} order for {code}.")
        status, transaction_info = self.broker_manager.place_market_order(code, quantity, "BUY")

        if not status:
            self.logger.error(f"Failed to place {order_type} order for {code}.")
            return

        # 거래 성공 시 거래 내역 기록
        transaction_id, executed_price, executed_quantity = transaction_info
        self.logger.info(f"{order_type} order successful for {code}: {transaction_id}, "
                         f"Price: {executed_price}, Quantity: {executed_quantity}.")
         self.trade_db_manager.record_buy_transaction(stock_name, code, transaction_id, self.COUNTRY_CODE, 1, executed_price, executed_quantity)

        # 모니터링에 신규 종목 추가
        buy_rate = 5
        sell_rate = 5
        self.monitoring_manager.add_stock_in_monitoring(0, stock_name, code, self.COUNTRY_CODE, 1, executed_price, executed_quantity, buy_rate, sell_rate)