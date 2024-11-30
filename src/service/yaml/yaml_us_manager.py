from src.interface.yaml_manager import YamlManager 
from src.util.enums import CountryCode

class YamlUsManager(YamlManager):
    COUNTRY_CODE = "US"
    def __init__(self,file_path):
        super().__init__(file_path)