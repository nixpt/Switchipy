#!/usr/bin/env python3
"""
Test suite for switchipy.themes module.

This module tests:
- Theme map generation
- Current theme detection
- Theme setting functionality
- Counterpart theme finding
- Theme mode detection
"""
import unittest
import subprocess
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from switchipy.themes import (
    generate_theme_map, 
    get_current_theme, 
    set_theme, 
    find_counterpart_theme, 
    get_current_mode
)

class TestThemes(unittest.TestCase):
    """Test cases for theme management functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        # Sample theme mapping for testing
        self.test_themes = {
            "Adwaita,Adwaita-Light": "Adwaita-Dark",
            "Adwaita-Dark": "Adwaita,Adwaita-Light"
        }
    
    @patch('switchipy.themes.THEME_DIRS')
    def test_generate_theme_map(self, mock_dirs):
        """Test theme map generation with mocked directories."""
        # Mock theme directories
        mock_dir = MagicMock()
        mock_dir.exists.return_value = True
        
        # Create mock theme objects
        mock_theme1 = MagicMock()
        mock_theme1.name = "Adwaita"
        mock_theme1.is_dir.return_value = True
        
        mock_theme2 = MagicMock()
        mock_theme2.name = "Adwaita-Light"
        mock_theme2.is_dir.return_value = True
        
        mock_theme3 = MagicMock()
        mock_theme3.name = "Adwaita-Dark"
        mock_theme3.is_dir.return_value = True
        
        mock_dir.iterdir.return_value = [mock_theme1, mock_theme2, mock_theme3]
        mock_dirs.__iter__.return_value = [mock_dir]
        
        # Test theme map generation
        theme_map = generate_theme_map()
        self.assertIsInstance(theme_map, dict)
        self.assertGreater(len(theme_map), 0)
    
    @patch('switchipy.themes.xfconf_query_get')
    def test_get_current_theme(self, mock_xfconf):
        """Test getting current theme with mocked xfconf."""
        # Mock successful xfconf query
        mock_xfconf.return_value = "Adwaita-Dark"
        
        theme = get_current_theme()
        self.assertEqual(theme, "Adwaita-Dark")
        mock_xfconf.assert_called_once()
    
    @patch('switchipy.themes.xfconf_query_get')
    def test_get_current_theme_error(self, mock_xfconf):
        """Test get_current_theme with error handling."""
        # Mock failed xfconf query
        mock_xfconf.return_value = None
        
        theme = get_current_theme()
        self.assertEqual(theme, "")
    
    @patch('switchipy.themes.xfconf_query_set')
    def test_set_theme(self, mock_xfconf):
        """Test setting theme with mocked xfconf."""
        set_theme("Adwaita-Dark")
        self.assertTrue(mock_xfconf.called)
    
    def test_find_counterpart_theme(self):
        """Test finding counterpart themes."""
        theme_map = {
            "Adwaita,Adwaita-Light": "Adwaita-Dark",
            "Adwaita-Dark": "Adwaita,Adwaita-Light"
        }
        
        # Test finding light counterpart
        counterpart = find_counterpart_theme("Adwaita-Dark", theme_map)
        self.assertEqual(counterpart, "Adwaita")
        
        # Test finding dark counterpart
        counterpart = find_counterpart_theme("Adwaita", theme_map)
        self.assertEqual(counterpart, "Adwaita-Dark")
        
        # Test no counterpart found
        counterpart = find_counterpart_theme("Unknown", theme_map)
        self.assertIsNone(counterpart)
    
    def test_get_current_mode(self):
        """Test theme mode detection (light/dark)."""
        # Test dark mode detection
        mode = get_current_mode("Adwaita-Dark")
        self.assertEqual(mode, "dark")
        
        # Test light mode detection
        mode = get_current_mode("Adwaita-Light")
        self.assertEqual(mode, "light")
        
        # Test with None (should get current theme)
        with patch('switchipy.themes.get_current_theme', return_value="Adwaita-Dark"):
            mode = get_current_mode()
            self.assertEqual(mode, "dark")

if __name__ == '__main__':
    unittest.main()
