import yaml
from src.util.enums import CountryCode


class YamlManager:
    COUNTRY_CODE = CountryCode.KR
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

    def _get_country_data(self):
        """현재 COUNTRY_CODE 데이터를 가져오거나 빈 리스트 생성."""
        data = self._read()
        if self.COUNTRY_CODE not in data:
            data[self.COUNTRY_CODE] = []
        return data[self.COUNTRY_CODE]

    def _save_country_data(self, country_data):
        """COUNTRY_CODE 데이터를 저장."""
        data = self._read()
        data[self.COUNTRY_CODE] = country_data
        self._write(data)

    def create(self, new_entry):
        """KR_STOCK 항목에 새 데이터를 추가."""
        data = self._get_country_data() 
       
        # 중복 검사
        if any(entry.get("code") == new_entry.get("code") for entry in data):
            raise ValueError("Duplicate entry detected")
        data.append(new_entry)
        self._save_country_data(data)

    def read_all(self):
        """KR_STOCK 데이터를 모두 가져오기."""
        country_data = self._get_country_data()
        return country_data.get(self.COUNTRY_CODE, [])

    def read_by_id(self, identifier):
        """특정 ID로 데이터를 가져오기."""
        country_data = self.read_all()
        for entry in country_data:
            if entry.get("code") == identifier:
                return entry
        return []


    def read(self, identifier=None):
        """KR_STOCK 데이터 가져오기."""
        data = self._read() 
        if self.COUNTRY_CODE not in data:
            return []

        filterd_data = data[self.COUNTRY_CODE]
        if identifier:

            for entry in filterd_data:
                if entry.get("code") == identifier:
                    return [entry]

        return data[self.COUNTRY_CODE] 

    def update(self, identifier, updated_data):
        """KR_STOCK에서 특정 항목 수정."""
        if "code" in updated_data:
            raise ValueError("Cannot modify the 'code' field.")

        country_data = self._get_country_data()
        for entry in country_data:
            if entry.get("code") == identifier:
                entry.update(updated_data)
         
                self._save_country_data(country_data)
                return
        raise KeyError(f"Entry with code '{identifier}' not found.")
 

    def delete(self, identifier):
        """KR_STOCK에서 특정 항목 삭제."""
        data = self._get_country_data()
        org_length = len(data)
        data = [entry for entry in data if entry.get("code") != identifier]
        if len(data) < org_length:
            self._write(data)
        else:
            raise ValueError("Cannot found the 'code' entry.")