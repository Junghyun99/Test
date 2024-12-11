from src.interface.yaml_manager import YamlManager
from src.util.enums import CountryCode

class YamlKrManager(YamlManager):
    COUNTRY_CODE = "KR"
    def __init__(self,file_path = "src/config/stock_round_config.yaml"):
        super().__init__(file_path)

class YamlUsManager(YamlManager):
    COUNTRY_CODE = "US"
    def __init__(self,file_path = "src/config/stock_round_config.yaml"):
        super().__init__(file_path)
