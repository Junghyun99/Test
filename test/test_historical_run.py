import pytest
import os
from datetime import datetime, timedelta
from freezegun import freeze_time
from src.service.logging.logger_manager import LoggerManager
from src.service.repository.monitoring_db import MonitoringDB
from src.service.repository.stock_trade_db import StockTradeDB

from src.service.broker.dummy_broker_api import DummyBrokerAPI
from src.main import MainApp
import pandas as pd


def mock_get_current_price(symbol):
    initial_time = datetime.now()
    formatted_time = initial_time.strftime("%d/%m/%Y")

    # CSV 파일 읽기
    file_name = f"test/csv/historical_data_{symbol}.csv"
    df = pd.read_csv(file_name)
    df_price = df[df["Date"] == formatted_time] 
    if df_price.empty:
        return 0

    return df_price["Price"].values[0]

@pytest.fixture
def mock_broker(mocker):
    mocker.patch("src.service.broker.dummy_broker_api.DummyBrokerAPI.get_current_price", side_effect=mock_get_current_price)

    mocker.patch("sys.argv", ["program", "US","--config","test/test_config.yaml"])

    return DummyBrokerAPI() 




@pytest.mark.large_test
class TestHistoricalPrice:

    @pytest.fixture(autouse=True)
    def setup(self, mock_broker):
        self.broker = mock_broker
 

    def test_get_csv(self):
        symbol = "AAPL"
        # CSV 파일 읽기
        file_name = f"test/csv/historical_data_{symbol}.csv"
        df = pd.read_csv(file_name)
        df_price = df[df["Date"] == "12/11/2024"]       

        assert df_price["Price"].values[0] == 224.23

    @freeze_time("2024-11-12 00:00:00")
    def test_time(self):
        initial_time = datetime.now()
        formatted_time = initial_time.strftime("%d/%m/%Y")

        assert formatted_time == "12/11/2024"

    @freeze_time("2024-11-12 00:00:00")
    def test_get_current_price(self):
        symbol = "AAPL"
        
        price = self.broker.get_current_price(symbol) 
        assert price == 224.23


    @freeze_time("2024-11-11 00:00:00")
    def test_time_range(self):
        symbol = "AAPL"
        initial_time = datetime.now()
        prices = [224.23, 224.23, 225.12, 228.22, 225, 0, 0, 228.02, 228.28, 229]

        for i in range(10):
            with freeze_time(initial_time + timedelta(days=i)):
                print(f"Iteration {i + 1}, 날짜: {datetime.now()}")
                assert self.broker.get_current_price(symbol) == prices[i]




@pytest.mark.large_test
class TestHistoricalMock:
    
    def mock_get_broker(self):
        return self.broker 
    
    @pytest.fixture(autouse=True)
    def setup(self, mock_broker):        
        self.broker = mock_broker 
   
    @freeze_time("2024-11-12 00:00:00")
    def test_get_broker(self, mocker):
        symbol = "AAPL"       
        mocker.patch("src.main.MainApp.get_broker", side_effect=self.mock_get_broker)
        assert MainApp().get_broker().get_current_price(symbol) == 224.23

@pytest.mark.large_test
class TestHistoricalMonitoring:

    @pytest.fixture(autouse=True)
    def setup(self):  
        self.file_path ="test/db/Monitoring.db"
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))  # 디렉토리 생성  
        self.logger = LoggerManager("test/test_config.yaml").get_logger('SYSTEM')
        db = MonitoringDB(self.logger, self.file_path)
                       
        query = '''INSERT INTO monitoring(stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        data = ('aaple', 'AAPL', 'US', 0, 100000.0, 1, 5, 3)
        db.insert_data(query, data)
        
        yield
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


    def test_monitoring(self):
        db = MonitoringDB(self.logger, self.file_path)
        result = db.read_data("SELECT * FROM monitoring WHERE code=?", ('AAPL',))
        assert result[0][2] == 'AAPL'
        

@pytest.mark.large_test
class TestHistoricalRun:

    def mock_get_broker(self):
        return self.broker 

    @pytest.fixture(autouse=True)
    def setup_monitoring_db(self):
        self.file_path ="test/db/Monitoring.db"
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))  # 디렉토리 생성  
        self.logger = LoggerManager("test/test_config.yaml").get_logger('SYSTEM')
        db = MonitoringDB(self.logger, self.file_path)
                       
        query = '''INSERT INTO monitoring(stock_name, code, country_code, trade_round, price, quantity, buy_rate, sell_rate) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        data = ('aaple', 'AAPL', 'US', 0, 10000.0, 1, 5, 3)
        db.insert_data(query, data)
        
        yield
        if os.path.exists(self.file_path):
            os.remove(self.file_path)




    @pytest.fixture(autouse=True)
    def setup(self, mock_broker):                        
        self.broker = mock_broker    
        self.app = MainApp()    

    @freeze_time("2024-11-12 00:00:00")
    def test_main_one_shot(self):
        self.app.run()
        file_path = "test/db/StockTrade.db"
        
        self.logger = LoggerManager("test/test_config.yaml").get_logger('SYSTEM')
        db = StockTradeDB(self.logger, file_path)
        result = db.read_data("SELECT * FROM history")
        assert result[0][3] == 'TX123'

        
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        assert 1 == 2