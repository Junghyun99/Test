import sys

from src.service.repository.monitoring_manager import MonitoringKrManager, MonitoringUsManager
from src.service.repository.trade_db_manager import TradeDbManager
from src.service.algorithm.magicsplit_algorithm import MagicSplit
from src.sevice.broker.broker_manager import BrokerManager
from src.sevice.yaml.yaml_manager import YamlKrManager, YamlUsManager 

from src.service.broker.dummy_broker_api import DummyBrokerAPI 
from src.util.enums import CountryCode

file_path = "src/config/stock_round_config.yaml"

def get_yaml_manager(country_code, file_path):
    manager_classes = {
        CountryCode.KR: YamlKrManager,
        CountryCode.US: YamlUsManager,
    }
    return manager_classes[country_code](file_path)

def get_monitoring_manager(country_code, algo):
    manager_classes = {
        CountryCode.KR: MonitoringKrManager,
        CountryCode.US: MonitoringUsManager,
    }
    return manager_classes[country_code](algo)


def run(country_code):
    trade = TradeDbManager()    
    yaml = get_yaml_manager(country_code, file_path)
    broker = BrokerManager(DummyBrokerAPI())
    algorithm = MagicSplit(broker, trade, yaml)
    moni = get_monitoring_manager(country_code, algorithm)

    try:
        moni.start_monitoring()
    finally:
        trade.close()
        moni.close()





# 명령행 인자의 개수 확인
if len(sys.argv) == 1:
    run(CountryCode.KR)
elif len(sys.argv) == 2:
    if sys.argv[1] == "KR":
        run(CountryCode.KR)
    elif sys.argv[1] == "US":
        run(CountryCode.US)