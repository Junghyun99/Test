from src.interface.stock_round_yaml import StockRoundYaml
from src.util.enums import CountryCode

from src.service.logging.logger_manager import logger_manager

system_logger = logger_manager.get_logger('SYSTEM')

class StockRoundYamlKrManager(StockRoundYaml):
    COUNTRY_CODE = "KR"
    def __init__(self,file_path = "src/config/stock_round_config.yaml"):
        super().__init__(file_path)
        system_logger.log_info("create StockRoundYamlKrManager instance, init")

class StockRoundYamlUsManager(StockRoundYaml):
    COUNTRY_CODE = "US"
    def __init__(self,file_path = "src/config/stock_round_config.yaml"):
        super().__init__(file_path)
        system_logger.log_info("create StockRoundYamlUsManager instance, init")

