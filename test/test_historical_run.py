import pytest

@pytest.mark.large_test
class TestHistoricalRun:

    @pytest.fixture(autouse=True)
    def setup(self):
        # 각 테스트 메서드 실행 전에 실행되는 setup 코드
        pass

    def test_add(self):
        # 더하기 테스트        
        assert 1 == 1