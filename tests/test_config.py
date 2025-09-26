#!/usr/bin/env python3
"""
Test suite for switchipy.config module.
"""
import unittest
import json
import tempfile
import os
from unittest.mock import patch, mock_open, MagicMock
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from switchipy.config import load_config, save_config, DEFAULT_CONFIG

class TestConfig(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_config = {
            "auto_switch_enabled": True,
            "dark_start": "20:00",
            "dark_end": "06:00",
            "last_theme": "Adwaita-Dark"
        }
    
    @patch('switchipy.config.CONFIG_PATH')
    def test_load_config_existing(self, mock_path):
        """Test loading existing config"""
        mock_path.exists.return_value = True
        with patch("builtins.open", mock_open(read_data=json.dumps(self.test_config))):
            config = load_config()
            self.assertEqual(config, self.test_config)
    
    @patch('switchipy.config.CONFIG_PATH')
    def test_load_config_default(self, mock_path):
        """Test loading default config when file doesn't exist"""
        mock_path.exists.return_value = False
        
        config = load_config()
        self.assertEqual(config, DEFAULT_CONFIG)
    
    @patch('switchipy.config.CONFIG_PATH')
    def test_load_config_error(self, mock_path):
        """Test loading config with error"""
        mock_path.exists.return_value = True
        mock_path.open.side_effect = Exception("File error")
        
        config = load_config()
        self.assertEqual(config, DEFAULT_CONFIG)
    
    @patch('switchipy.config.CONFIG_PATH')
    def test_save_config(self, mock_path):
        """Test saving config"""
        with patch("builtins.open", mock_open()) as mock_file_open:
            save_config(self.test_config)
            mock_file_open.assert_called_once_with(mock_path, "w")
    
    def test_default_config_structure(self):
        """Test default config structure"""
        self.assertIn("auto_switch_enabled", DEFAULT_CONFIG)
        self.assertIn("dark_start", DEFAULT_CONFIG)
        self.assertIn("dark_end", DEFAULT_CONFIG)
        self.assertIn("last_theme", DEFAULT_CONFIG)
        
        self.assertIsInstance(DEFAULT_CONFIG["auto_switch_enabled"], bool)
        self.assertIsInstance(DEFAULT_CONFIG["dark_start"], str)
        self.assertIsInstance(DEFAULT_CONFIG["dark_end"], str)
        self.assertIsInstance(DEFAULT_CONFIG["last_theme"], str)

if __name__ == '__main__':
    unittest.main()
