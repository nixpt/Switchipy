#!/usr/bin/env python3
"""
Test suite for switchipy.icons module.
"""
import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from switchipy.icons import create_icon, update_icon, ICON_PATH

class TestIcons(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_icon_path = ICON_PATH
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Restore original icon path
        import switchipy.icons
        switchipy.icons.ICON_PATH = self.original_icon_path
    
    def test_create_icon_light(self):
        """Test creating light mode icon"""
        result_path = create_icon("light")
        self.assertIsInstance(result_path, str)
        self.assertTrue(os.path.exists(result_path))
    
    def test_create_icon_dark(self):
        """Test creating dark mode icon"""
        result_path = create_icon("dark")
        self.assertIsInstance(result_path, str)
        self.assertTrue(os.path.exists(result_path))
    
    @patch('switchipy.icons.GLib.idle_add')
    @patch('switchipy.icons.create_icon')
    def test_update_icon(self, mock_create, mock_idle_add):
        """Test updating icon"""
        mock_indicator = MagicMock()
        mock_create.return_value = "/tmp/test_icon.png"
        
        update_icon(mock_indicator, "light")
        
        mock_create.assert_called_once_with("light")
        mock_idle_add.assert_called_once()
    
    def test_icon_path_constant(self):
        """Test icon path constant"""
        from switchipy.icons import ICON_PATH
        self.assertEqual(ICON_PATH, "/tmp/switchipy_icon.png")

if __name__ == '__main__':
    unittest.main()
