import pytest

from datetime import datetime, timedelta
from freezegun import freeze_time

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