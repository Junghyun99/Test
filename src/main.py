from src.service.repository.monitoring_manager import MonitoringKRManager, MonitoringUSManager
from src.service.repository.trade_db_manager import TradeDbManager
from src.service.algorithm.magicsplit_algorithm import MagicSplit
from src.sevice.broker.broker_manager import BrokerManager
from src.sevice.yaml.yaml_manager import YamlKrManager, YamlUsManager 

from src.service.broker.dummy_broker_api import DummyBrokerAPI 
from src.util.enums import CountryCode

file_path = "src/config/stock_round_config.yaml"

def get_yaml_manager(country_code, file_path):
    manager_classes = {
        CountryCode.KR: YamlKrManager,
        CountryCode.US: YamlUsManager,
    }
    return manager_classes[country_code](file_path)

def get_monitoring_manager(country_code, algo):
    manager_classes = {
        CountryCode.KR: MonitoringKRManager,
        CountryCode.US: MonitoringUSManager,
    }
    return manager_classes[country_code](algo)


def run(country_code):
    trade = TradeDbManager()    
    yaml = get_yaml_manager(country_code, file_path)
    broker = BrokerManager(DummyBrokerAPI())
    algorithm = MagicSplit(broker, trade, yaml)
    moni = get_monitoring_manager(country_code, algorithm)

    try:
        moni.start_monitoring()
    finally:
        trade.close()
        moni.close()

def parse_country_code(arg):
    country_code_map = {
        "KR": CountryCode.KR,
        "US": CountryCode.US,
    }
    return country_code_map.get(arg.upper())



def main():
    import argparse

    # ArgumentParser 객체 생성
    parser = argparse.ArgumentParser(description="Run stock monitoring system")
    
    # country 인자를 추가 (선택적, 기본값은 'KR')
    parser.add_argument(
        "country",  # 명령행에서 받을 인자 이름
        nargs="?",  # 선택적 인자
        choices=["KR", "US"],  # 유효한 값 제한
        default="KR",  # 기본값
        help="Country code for the stock monitoring system (KR/US)"
    )
    
    
    # 명령행 인자 파싱
    args = parser.parse_args()
    
    try:
        # country 인자를 CountryCode로 변환
        country_code = parse_country_code(args.country)
        if country_code is None:
            raise ValueError(f"Invalid country code: {args.country}")
        
        # run 함수 실행
        run(country_code)
    
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)



if __name__ == "__main__":
    main()
