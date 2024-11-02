from src.interface.yaml_manager import YamlManager 

class YamlUsManager(YamlManager):
    COUNTRY_CODE = "US_STOCK"
    def __init__(self,file_path):
        super().__init__(file_path)