import yaml
from pathlib import Path

class YamlManager:
    def __init__(self, config_file = "src/config/config.yaml"):
        self.config_file = config_file
    def _set_logger_class_yaml_config(self):
        # YAML 설정 로드
        with open(self.config_file, "r") as file:
            config = yaml.safe_load(file)

        logger = config['logger_class']
        log_dir = Path(logger['log_dir'])
        self.system_log_file = log_dir / logger['system_log_file']
        self.transaction_log_file = log_dir / logger['transaction_log_file']

        # 디렉토리 생성 (없으면 생성)
        log_dir.mkdir(parents=True, exist_ok=True)
    
    def _set_db_class_yaml_config(self):
        # YAML 설정 로드
        with open(self.config_file, "r") as file:
            config = yaml.safe_load(file)

        sql_db = config['db_class']
        db_dir = Path(sql_db['db_dir'])
        self.monitoring_db_file = db_dir / sql_db['monitoring_db_file']
        self.stock_trade_db_file = db_dir / sql_db['stock_trade_db_file']

        # 디렉토리 생성 (없으면 생성)
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def _set_stock_round_yaml_config(self):
        # YAML 설정 로드
        with open(self.config_file, "r") as file:
            config = yaml.safe_load(file)

        stock_round = config['stock_round_yaml']
        self.stock_round_path = stock_round['path']
        
    def _write(self, data):
        try:
            """YAML 파일 쓰기 (내부에서만 호출)"""
            with open(self.file_path, 'w', encoding='utf-8') as file:
                yaml.dump(data, file, allow_unicode=True)
        except Exception as e:
            raise RuntimeError(f"Failed to write to file {self.file_path}: {e}")

    def _read(self):
        """YAML 파일 읽기 (내부에서만 호출)"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            return {}	
        except yaml.YAMLError as e:
            raise RuntimeError(f"Failed to parse YAML file {self.file_path}: {e}")