import sys
import argparse

from src.service.repository.monitoring_manager import MonitoringKRManager, MonitoringUSManager
from src.service.repository.trade_db_manager import TradeDBManager
from src.service.algorithm.magicsplit_algorithm import MagicSplit
from src.service.broker.broker_manager import BrokerManager
from src.service.yaml.yaml_manager import YamlKrManager, YamlUsManager 

from src.service.broker.dummy_broker_api import DummyBrokerAPI 
from src.util.enums import CountryCode

import src.service.repository.trade_db_manager as tdm


class MainApp:
    def __init__(self):
        self.args = None
        self.country_code = CountryCode.KR
        self.parser_argument()
        self.parse_country_code()
    

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
      
        # 명령행 인자 파싱
        self.args = parser.parse_args()

        
    def parse_country_code(self):
        country_code_map = {
        "KR": CountryCode.KR,
        "US": CountryCode.US,
        }
        self.country_code = country_code_map.get(self.args.country.upper())

        try:
            if self.country_code is None:
                raise ValueError(f"Invalid country code: {args.country}")
        
       
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    def get_yaml_manager(self):
        manager_classes = {
        CountryCode.KR: YamlKrManager,
        CountryCode.US: YamlUsManager,
    }
        return manager_classes[self.country_code]()

    def get_monitoring_manager(self, algo):
        manager_classes = {
        CountryCode.KR: MonitoringKRManager,
        CountryCode.US: MonitoringUSManager,
    }
        return manager_classes[self.country_code](algo)


    def run(self):
        trade = TradeDBManager()    
        print(trade)
        yaml = self.get_yaml_manager()
        broker = BrokerManager(DummyBrokerAPI())
        algorithm = MagicSplit(broker, trade, yaml)
        moni = self.get_monitoring_manager(algorithm)

        try:
            moni.start_monitoring()
        finally:
            print("Actual module path:", TradeDBManager.__module__)
            print("Module attributes:", dir(tdm))
            print("close")
            trade.close_db()
            moni.close_db()



if __name__ == "__main__":
    MainApp().run()