import pytest

from datetime import datetime, timedelta
from freezegun import freeze_time

from src.service.broker.dummy_broker_api import DummyBrokerAPI

import pandas as pd

@pytest.fixture
def temp_round_file():
    file_path = "test/csv/stock_round_config.yaml"

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        return {}        
    except yaml.YAMLError as e:
        raise RuntimeError(f"Failed to parse YAML file {self.file_path}: {e}")

    




@pytest.mark.large_test
class TestHistoriRound:
    pass

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

@pytest.mark.large_test
class TestHistoricalPrice:

    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        mocker.patch("src.service.broker.dummy_broker_api.DummyBrokerAPI.get_current_price", side_effect=mock_get_current_price)

        self.broker = DummyBrokerAPI()
 

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
class TestHistoricalRun:

    @pytest.fixture(autouse=True)
    def setup(self):
        # 각 테스트 메서드 실행 전에 실행되는 setup 코드
        pass

    @freeze_time("2024-01-01 00:00:00")
    def test_main(self):
        initial_time = datetime.now()

        for i in range(100):
            with freeze_time(initial_time + timedelta(days=i)):
                print(f"Iteration {i + 1}, 날짜: {datetime.now()}")
                #main()