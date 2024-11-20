from src.interface.yaml_manager import YamlManager
from src.util.enums import CountryCode

class YamlKrManager(YamlManager):
    COUNTRY_CODE = CountryCode.KR
    def __init__(self,file_path):
        super().__init__(file_path)