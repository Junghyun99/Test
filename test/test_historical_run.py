import pytest

from datetime import datetime, timedelta
from freezegun import freeze_time


def mock_get_


@pytest.mark.large_test
class TestHistoricalPrice:

    @pytest.fixture(autouse=True)
    def setup(self):
        # 각 테스트 메서드 실행 전에 실행되는 setup 코드
        pass

    def test_get_price(mocker):
    # 특정 함수만 모킹
    mocker.patch(".method_to_mock", return_value="Mocked Response")

    obj = ExampleClass()

    # 모킹된 함수 확인
    assert obj.method_to_mock() == "Mocked Response"

    # 다른 메서드는 원래 동작 유지
    assert obj.method_to_keep() == "Keep Original Behavior"




@pytest.mark.large_test
class TestHistoricalRun:

    @pytest.fixture(autouse=True)
    def setup(self):
        # 각 테스트 메서드 실행 전에 실행되는 setup 코드
        pass

    @freeze_time("2024-01-01 00:00:00")
    def test_main():
        initial_time = datetime.now()

        for i in range(100):
            with freeze_time(initial_time + timedelta(days=i)):
                print(f"Iteration {i + 1}, 날짜: {datetime.now()}")
                #main()