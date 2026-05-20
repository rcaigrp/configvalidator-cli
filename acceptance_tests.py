import unittest
import json
import os
from unittest.mock import patch
import click.testing
import config_validator

class TestConfigValidator(unittest.TestCase):
    def setUp(self):
        self.runner = click.testing.CliRunner()

    @patch('config_validator.scan_directory')
    @patch('config_validator.load_config')
    def test_criterion_1_2_scan_parse(self, mock_load, mock_scan):
        mock_scan.return_value = ['/tmp/test.yaml']
        def load_side_effect(path):
            if path.endswith('.yaml'):
                return {'config': 'value'}
            return {}
        mock_load.side_effect = load_side_effect
        
        result = self.runner.invoke(config_validator.main, ['/path', '/schema.json'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('valid', result.output)

    @patch('config_validator.scan_directory')
    @patch('config_validator.load_config')
    def test_criterion_3_validate_schema(self, mock_load, mock_scan):
        mock_scan.return_value = ['/tmp/test.yaml']
        def load_side_effect(path):
            if path.endswith('.yaml'):
                return {'config': 'value'}
            return {}
        mock_load.side_effect = load_side_effect
        
        result = self.runner.invoke(config_validator.main, ['/path', '/schema.json'])
        self.assertEqual(result.exit_code, 0)

    def test_criterion_4_rich_output(self):
        with patch('config_validator.load_config') as mock_load:
            mock_load.return_value = {}
            with patch('config_validator.scan_directory') as mock_scan:
                mock_scan.return_value = []
                result = self.runner.invoke(config_validator.main, ['/path', '/schema.json'])
                self.assertEqual(result.exit_code, 0)
                self.assertIn('|', result.output)

    def test_criterion_5_dry_run(self):
        with patch('config_validator.load_config') as mock_load:
            mock_load.return_value = {}
            with patch('config_validator.scan_directory') as mock_scan:
                mock_scan.return_value = []
                result = self.runner.invoke(config_validator.main, ['/path', '/schema.json', '--dry-run'])
                self.assertEqual(result.exit_code, 0)

    def test_criterion_6_export_json(self):
        with patch('config_validator.load_config') as mock_load:
            mock_load.return_value = {}
            with patch('config_validator.scan_directory') as mock_scan:
                mock_scan.return_value = []
                result = self.runner.invoke(config_validator.main, ['/path', '/schema.json', '--export', '/tmp/out.json'])
                self.assertEqual(result.exit_code, 0)
                self.assertTrue(os.path.exists('/tmp/out.json'))

if __name__ == '__main__':
    unittest.main()
