from src.service.repository.monitoring_manager import MonitoringKrManager, MonitoringUsManager
from src.service.repository.trade_db_manager import TradeDbManager
from src.service.algorithm.magicsplit_algorithm import MagicSplit
from src.sevice.broker.broker_manager import BrokerManager
from src.sevice.yaml.yaml_manager import YamlKrManager, YamlUsManager 

from src.service.broker.dummy_broker_api import DummyBrokerAPI

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


def run_common(country_code):
    trade = TradeDbManager()    
    yaml = get_yaml_manager(country_code)
    broker = BrokerManager(DummyBrokerAPI())
    algorithm = MagicSplit(broker, trade, yaml)
    moni = get_monitoring_manager(country_code, algorithm)
    moni.start_monitoring()
