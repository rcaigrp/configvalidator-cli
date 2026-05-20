import os
import json
import tempfile
import pytest
import click.testing
from unittest.mock import patch, MagicMock
import yaml

import sys
sys.path.insert(0, '/workspace/projects/ConfigValidator-CLI')
from config_validator import process_configs, scan_files, main

@pytest.fixture
def runner():
    return click.testing.CliRunner()

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

def test_criterion_1_scan_recursive(temp_dir):
    sub_dir = os.path.join(temp_dir, 'sub')
    os.makedirs(sub_dir)
    file_path = os.path.join(sub_dir, 'config.json')
    with open(file_path, 'w') as f:
        json.dump({"key": "val"}, f)
    
    with patch('config_validator.os.walk') as mock_walk:
        mock_walk.return_value = [(sub_dir, [], ['config.json'])]
        files = scan_files(temp_dir)
        assert len(files) == 1
        assert files[0] == file_path

def test_criterion_2_parse_json_yaml(temp_dir):
    schema = {"required": ["key"]}
    with patch('config_validator.os.walk') as mock_walk:
        mock_walk.return_value = [(temp_dir, [], ['config.json', 'config.yaml'])]
        
        def mock_open(path, mode='r'):
            if path.endswith('.json'):
                return MagicMock(read=lambda: '{"key": "val"}')
            else:
                return MagicMock(read=lambda: 'key: val')
                
        with patch('builtins.open', mock_open):
            results = process_configs(temp_dir, schema)
            assert len(results) == 2

def test_criterion_3_validate_schema(temp_dir):
    schema = {"required": ["key"]}
    config_valid = {"key": "val"}
    config_invalid = {"other": "val"}
    from config_validator import validate_schema
    assert validate_schema(config_valid, schema)[0] == True
    assert validate_schema(config_invalid, schema)[0] == False

def test_criterion_4_rich_table_output(temp_dir):
    runner = click.testing.CliRunner()
    schema_path = os.path.join(temp_dir, 'schema.json')
    config_path = os.path.join(temp_dir, 'config.json')
    
    with open(schema_path, 'w') as f:
        json.dump({"required": ["key"]}, f)
    with open(config_path, 'w') as f:
        json.dump({"key": "val"}, f)
        
    result = runner.invoke(main, [temp_dir, '--schema', schema_path])
    assert result.exit_code == 0
    assert "config.json" in result.stdout or "File" in result.stdout

def test_criterion_5_dry_run(temp_dir):
    runner = click.testing.CliRunner()
    schema_path = os.path.join(temp_dir, 'schema.json')
    config_path = os.path.join(temp_dir, 'config.json')
    output_path = os.path.join(temp_dir, 'output.json')
    
    with open(schema_path, 'w') as f:
        json.dump({"required": ["key"]}, f)
    with open(config_path, 'w') as f:
        json.dump({"key": "val"}, f)
        
    result = runner.invoke(main, [temp_dir, '--schema', schema_path, '--output', output_path, '--dry-run'])
    assert result.exit_code == 0
    assert not os.path.exists(output_path)

def test_criterion_6_export_json(temp_dir):
    runner = click.testing.CliRunner()
    schema_path = os.path.join(temp_dir, 'schema.json')
    config_path = os.path.join(temp_dir, 'config.json')
    output_path = os.path.join(temp_dir, 'output.json')
    
    with open(schema_path, 'w') as f:
        json.dump({"required": ["key"]}, f)
    with open(config_path, 'w') as f:
        json.dump({"key": "val"}, f)
        
    result = runner.invoke(main, [temp_dir, '--schema', schema_path, '--output', output_path])
    assert result.exit_code == 0
    assert os.path.exists(output_path)
    with open(output_path) as f:
        data = json.load(f)
    assert len(data) > 0