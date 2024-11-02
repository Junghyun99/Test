from src.model.yaml_manager import YamlManager

class YamlKrManager(YamlManager):
    COUNTRY_CODE = "KR_STOCK"
    def __init__(self,file_path):
        super().__init__(file_path)