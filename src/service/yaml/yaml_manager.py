from src.interface.yaml_manager import YamlManager
from src.util.enums import CountryCode

from src.service.logging.logger_manager import logger_manager

system_logger = logger_manager.get_logger('SYSTEM')

class YamlKrManager(YamlManager):
    COUNTRY_CODE = "KR"
    def __init__(self,file_path = "src/config/stock_round_config.yaml"):
        super().__init__(file_path)
        system_logger.log_info("create YamlKrManager instance, init")

class YamlUsManager(YamlManager):
    COUNTRY_CODE = "US"
    def __init__(self,file_path = "src/config/stock_round_config.yaml"):
        super().__init__(file_path)
        system_logger.log_info("create YamlUsManager instance, init")

