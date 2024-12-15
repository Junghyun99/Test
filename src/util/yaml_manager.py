import yaml

class YamlManager:
    def __init__(self, file_path):
        self.file_path = file_path

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