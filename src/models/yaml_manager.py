from abc import ABC, abstractmethod
import yaml

class YamlManager(ABC):
    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def create(self, new_entry):
        pass

    @abstractmethod
    def read(self, identifier):
        pass

    @abstractmethod
    def update(self, identifier, updated_data):
        pass

    @abstractmethod
    def delete(self, identifier):
        pass

    def _write(self, data):
        """YAML 파일 쓰기 (내부에서만 호출)"""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True)

    def _read(self):
        """YAML 파일 읽기 (내부에서만 호출)"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            return {}