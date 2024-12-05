import sys

from src.service.repository.monitoring_manager import MonitoringKrManager, MonitoringUsManager
from src.service.repository.trade_db_manager import TradeDbManager
from src.service.algorithm.magicsplit_algorithm import MagicSplit
from src.sevice.broker.broker_manager import BrokerManager
from src.sevice.yaml.yaml_manager import YamlKrManager, YamlUsManager 

from src.service.broker.dummy_broker_api import DummyBrokerAPI 
from src.util.enums import CountryCode

file_path = "src/config/stock_round_config.yaml"


def get_yaml_manager(country_code):
    if country_code == CountryCode.KR:
        return YamlKrManager(file_path)
    else:
        return YamlUsManager(file_path) 

def get_monitoring_manager(country_code, algo):
    if country_code == CountryCode.KR:
        return MonitoringKrManager(algo)
    else:
        return MonitoringUsManager(algo) 


def run(country_code):
    trade = TradeDbManager()    
    yaml = get_yaml_manager(country_code)
    broker = BrokerManager(DummyBrokerAPI())
    algorithm = MagicSplit(broker, trade, yaml)
    moni = get_monitoring_manager(country_code, algorithm)
    moni.start_monitoring()

    trade.close()
    moni.close()





# 명령행 인자의 개수 확인
if len(sys.argv) == 1:
    print("No arguments were provided!")
elif len(sys.argv) == 2:
    print(f"Only one argument provided: {sys.argv[1]}")
else:
    print(f"Multiple arguments provided: {sys.argv[1:]}")