from src.interface.stock_round_yaml import StockRoundYaml
from src.util.enums import CountryCode

from src.service.logging.logger_manager import logger_manager

system_logger = logger_manager.get_logger('SYSTEM')

class StockRoundYamlKrManager(StockRoundYaml):
    COUNTRY_CODE = "KR"
    def __init__(self):
        super().__init__()
        system_logger.log_info("create StockRoundYamlKrManager instance, init")

class StockRoundYamlUsManager(StockRoundYaml):
    COUNTRY_CODE = "US"
    def __init__(self):
        super().__init__()
        system_logger.log_info("create StockRoundYamlUsManager instance, init")

