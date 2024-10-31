import pytest
import os
import yaml
from src.service.yaml.yaml_kr_manager import YamlKrManager

@pytest.fixture
def yaml_file(tmp_path):
    """테스트용 YAML 파일을 생성하는 fixture."""
    return tmp_path / "test_data.yaml"

@pytest.fixture
def yaml_crud(yaml_file):
    """YamlCRUD 객체를 생성하는 fixture."""
    return YamlKrManager(str(yaml_file))

def test_create(yaml_crud, yaml_file):
    new_entry = {"name": "Test", "value": 100}
    yaml_crud.create(new_entry)

    # YAML 파일에서 데이터 읽기
    with open(yaml_file, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    
    assert data == [new_entry]

def test_read(yaml_crud, yaml_file):
    entry1 = {"name": "Test1", "value": 100}
    entry2 = {"name": "Test2", "value": 200}
    yaml_crud.create(entry1)
    yaml_crud.create(entry2)

    data = yaml_crud.read()
    assert data == [entry1, entry2]

def test_update(yaml_crud, yaml_file):
    entry = {"name": "Test", "value": 100}
    yaml_crud.create(entry)

    updated_data = {"value": 150}
    result = yaml_crud.update(0, updated_data)

    assert result is True
    assert yaml_crud.read()[0]["value"] == 150

def test_update_invalid_index(yaml_crud):
    result = yaml_crud.update(0, {"value": 150})
    assert result is False

def test_delete(yaml_crud, yaml_file):
    entry1 = {"name": "Test1", "value": 100}
    entry2 = {"name": "Test2", "value": 200}
    yaml_crud.create(entry1)
    yaml_crud.create(entry2)

    result = yaml_crud.delete(0)

    assert result is True
    assert yaml_crud.read() == [entry2]

def test_delete_invalid_index(yaml_crud):
    result = yaml_crud.delete(0)
    assert result is False
