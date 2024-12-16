from src.util.yaml_manager import YamlManager

class StockRoundYaml(YamlManager):
    COUNTRY_CODE = "KR"
    def __int__(self, config_file):
        super().__init__(config_file)
        self._set_stock_round_yaml_config()
        self.file_path = self.stock_round_path
        print("file path %s",self.File_path)
        
    def _get_country_data(self):
        """현재 COUNTRY_CODE 데이터를 가져오거나 빈 리스트 생성."""
        data = self._read()
        print ("%s",data)
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
        return self._get_country_data()

    def read_by_id(self, identifier):
        """특정 ID로 데이터를 가져오기."""
        country_data = self.read_all()
        for entry in country_data:
            if entry.get("code") == identifier:
                return [entry]
        return []

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
            self._save_country_data(data)
        else:
            raise ValueError("Cannot found the 'code' entry.")