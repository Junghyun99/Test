from src.interface.algorithm import Algorithm
from src.util.enums import CountryCode

class ManualTradeManager(Algorithm):
    COUNTRY_CODE = CountryCode.KR

    def __init__(self, monitoring_manager, broker_manager, trade_db_manager, logger):      
        self.monitoring_manager = monitoring_manager
        self.broker_manager = broker_manager
        self.trade_db_manager = trade_db_manager
        self.logger = logger


    
    def run_algorithm(self, moniData:MonitoringData):
        """
    stock_name: str
    code: str
    country_code: CountryCode
    trade_round: int
    price : float
    quantity : int
    buy_rate: int
    sell_rate: int 
        """
        pass

    def handle_trade(self, code, stock_name, quantity, order_type, price=None):
        """
        수동 매수/매도 처리 함수.
        :param code: 종목 코드
        :param stock_name: 종목 이름
        :param quantity: 거래 수량
        :param order_type: 거래 타입 ("BUY" or "SELL")
        :param price: 거래 가격 (선택적, 기본값은 None)
        """
        self.logger.info(f"Manual trade initiated for {code} - {order_type} {quantity} units.")

        # 진행 중인지 확인
        monitoring_data = self.monitoring_manager.read()
        existing_stock =    self.monitoring_manager.check_already_existing_monitoring(code)

        if existing_stock:
            # 진행 중인 종목이면 모니터링에서 제거 및 자동매매 종료
            self.logger.info(f"Stopping auto-trade for {code}.")
            self.monitoring_manager.delete_stock_in_monitoring(code)
        else:
            self.logger.info(f"No active monitoring found for {code}.")

        # 브로커를 통해 거래 시도
        self.logger.info(f"Attempting to place a {order_type} order for {code}.")
        status, transaction_info = self.broker_manager.place_market_order(code, quantity, order_type, price)

        if not status:
            self.logger.error(f"Failed to place {order_type} order for {code}.")
            return

        # 거래 성공 시 거래 내역 기록
        transaction_id, executed_price, executed_quantity = transaction_info
        self.logger.info(f"{order_type} order successful for {code}: {transaction_id}, "
                         f"Price: {executed_price}, Quantity: {executed_quantity}.")
        self.trade_db_manager.add(stock_name, code, transaction_id, order_type, executed_price, executed_quantity)

        # 모니터링에 신규 종목 추가
        if order_type == "BUY":
            self.logger.info(f"Adding {code} to monitoring for tracking.")
            self.monitoring_manager.add(code, stock_name, executed_price, executed_quantity)