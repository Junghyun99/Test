from src.interface.stock_round_yaml import StockRoundYaml
from src.util.enums import CountryCode


class StockRoundYamlKrManager(StockRoundYaml):
    COUNTRY_CODE = "KR"
    def __init__(self, config_file, logger):
        super().__init__(config_file, logger)
        self.logger = logger
        self.logger.log_info("create StockRoundYamlKrManager instance, init")

class StockRoundYamlUsManager(StockRoundYaml):
    COUNTRY_CODE = "US"
    def __init__(self, config_file, logger):
        super().__init__(config_file, logger)
        self.logger = logger
        self.logger.log_info("create StockRoundYamlUsManager instance, init")

