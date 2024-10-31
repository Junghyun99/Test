from abc import ABC, abstractmethod
import yaml

class YamlManager(ABC):
    COUNTRY_CODE = "KR_STOCK"
    def __init__(self, file_path):
        self.file_path = file_path

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

    @abstractmethod    
    def create(self, new_entry):
        """KR_STOCK 항목에 새 데이터를 추가."""
        data = self._read()
        if COUNTRY_CODE not in data:
            data[COUNTRY_CODE] = []
      data[Country_code].append(new_entry)
        self._write(data)

    @abstractmethod
    def read(self, identifier):
        """KR_STOCK 데이터 가져오기."""
        data = self.read() 
        if COUNTRY_CODE in data:
            if identifier:
                return [entry for entry in data[COUNTRY_CODE] if entry.get("code") == identifier] 
            return data[section] 
        return None

    @abstractmethod
    def update(self, identifier, updated_data):
        """KR_STOCK에서 특정 항목 수정."""
        data = self._read()
        if COUNTRY_CODE in data:
            for entry in data[COUNTRY_CODE]:
                if entry.get("code") == identifier:
                    entry.update(updated_data)
                    self._write(data)
                    return True
        return False

    @abstractmethod 
    def delete(self, identifier):
        """KR_STOCK에서 특정 항목 삭제."""
        data = self._read()
        if COUNTRY_CODE in data:
            original_length = len(data[COUNTRY_CODE])
            data[COUNTRY_CODE] = [entry for entry in data[COUNTRY_CODE] if entry.get("code") != identifier]
            if len(data[COUNTRY_CODE]) < original_length:
                self._write(data)
                return True
        return False