import sys
import argparse

from src.service.repository.monitoring_manager import MonitoringKRManager, MonitoringUSManager
from src.service.repository.trade_db_manager import TradeDBManager
from src.service.algorithm.magicsplit_algorithm import MagicSplit
from src.service.broker.broker_manager import BrokerManager
from src.service.algorithm.stock_round_yaml_manager import StockRoundYamlKrManager, StockRoundYamlUsManager 

from src.service.broker.dummy_broker_api import DummyBrokerAPI 
from src.util.enums import CountryCode

from src.service.logging.logger_manager import LoggerManager

class MainApp:
    def __init__(self):
        self.args = None
        self.country_code = CountryCode.KR
        self.parser_argument()
        self.parse_country_code()
        self.parse_config_file()

    def parser_argument(self):
        # ArgumentParser 객체 생성
        parser = argparse.ArgumentParser(description="Run stock monitoring system")
    
        # country 인자를 추가 (선택적, 기본값은 'KR')
        parser.add_argument(
        "country",  # 명령행에서 받을 인자 이름
        nargs="?",  # 선택적 인자
        choices=["KR", "US", "kr", "us"],  # 유효한 값 제한
        default="KR",  # 기본값
        help="Country code for the stock monitoring system (KR/US)"
    )


        # config 인자 추가 (선택적, 기본값은 'src/config/config.yaml')
        parser.add_argument(
        "--config",  # 명령행에서 사용할 옵션 이름
        type=str,  # 입력 데이터 타입
        default="src/config/config.yaml",  # 기본값
        help="Path to the configuration file (default: src/config/config.yaml)"
)
      
        # 명령행 인자 파싱
        self.args = parser.parse_args()

    def parse_config_file(self):
        self.config_file = self.args.config

        
    def parse_country_code(self):
        country_code_map = {
        "KR": CountryCode.KR,
        "US": CountryCode.US,
        }
        self.country_code = country_code_map.get(self.args.country.upper())

        try:
            if self.country_code is None:
                raise ValueError(f"Invalid country code: {self.args.country}")
        
       
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    def get_stock_round_yaml_manager(self, logger):
        manager_classes = {
        CountryCode.KR: StockRoundYamlKrManager,
        CountryCode.US: StockRoundYamlUsManager,
    }
        return manager_classes[self.country_code](self.Config_file, logger)

    def get_monitoring_manager(self, algo, logger):
        manager_classes = {
        CountryCode.KR: MonitoringKRManager,
        CountryCode.US: MonitoringUSManager,
    }
        return manager_classes[self.country_code](algo, logger)


    def run(self):
        logger = LoggerManager(self.config_file)
        sys_logger = logger.get_logger('SYSTEM')    
        trade = TradeDBManager(sys_logger)    
        yaml = self.get_stock_round_yaml_manager(sys_logger)
        broker = BrokerManager(DummyBrokerAPI(),logger.get_logger('TRANSACTION'))
        algorithm = MagicSplit(broker, trade, yaml, sys_logger)
        moni = self.get_monitoring_manager(algorithm, sys_logger)

        try:
            moni.start_monitoring()
        finally:          
            trade.close_db()
            moni.close_db()



if __name__ == "__main__":
    MainApp().run()