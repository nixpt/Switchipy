#!/usr/bin/env python3
"""
Test suite for switchipy.hotkey module.
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from switchipy.hotkey import register_hotkey

class TestHotkey(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_callback = MagicMock()
    
    @patch('switchipy.hotkey.keyboard.GlobalHotKeys')
    @patch('switchipy.hotkey.threading.Thread')
    def test_register_hotkey(self, mock_thread, mock_hotkeys):
        """Test hotkey registration"""
        mock_hotkey_instance = MagicMock()
        mock_hotkeys.return_value = mock_hotkey_instance
        
        register_hotkey(self.test_callback)
        
        # Verify GlobalHotKeys was called with correct hotkey
        mock_hotkeys.assert_called_once_with({
            '<ctrl>+<alt>+t': self.test_callback
        })
        
        # Verify thread was started
        mock_thread.assert_called_once()
        mock_thread.return_value.start.assert_called_once()
    
    @patch('switchipy.hotkey.keyboard.GlobalHotKeys')
    @patch('switchipy.hotkey.threading.Thread')
    def test_register_hotkey_daemon(self, mock_thread, mock_hotkeys):
        """Test that hotkey thread is daemon"""
        register_hotkey(self.test_callback)
        
        # Verify thread is created as daemon
        mock_thread.assert_called_once()
        args, kwargs = mock_thread.call_args
        self.assertEqual(kwargs.get('daemon'), True)

if __name__ == '__main__':
    unittest.main()
