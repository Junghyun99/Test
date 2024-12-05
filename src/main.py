from src.service.repository.monitoring_manager import MonitoringKrManager, MonitoringUsManager
from src.service.repository.trade_db_manager import TradeDbManager
from src.service.algorithm.magicsplit_algorithm import MagicSplit
from src.sevice.broker.broker_manager import BrokerManager
from src.sevice.yaml.yaml_manager import YamlKrManager, YamlUsManager 


def run_common():
    trade_db_manager = TradeDbManager()
    algorithm = MagicSplit()
    broker_manager = BrokerManager()


def run_kr(algorithm):
    moni_manager = MonitoringKrManager(algorithm)
    yaml_manager = YamlKrManager()
    

def run_us(algorithm):
    moni_manager = MonitoringUsManager(algorithm) 
    yaml_manager = YamlUsManager()
