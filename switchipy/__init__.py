"""
Switchipy - XFCE Theme Switcher Package

A system tray application for switching between light and dark themes on XFCE.

This package provides:
- Theme management and detection
- Configuration handling
- Icon generation
- Hotkey functionality
- Auto-switching capabilities
- Command line interface
"""

__version__ = "1.0.0"
__author__ = "Prabin Thapa"
__license__ = "MIT"
__email__ = "prabin@example.com"

# Import main components for easy access
from .themes import (
    generate_theme_map,
    get_current_theme,
    set_theme,
    find_counterpart_theme,
    get_current_mode
)

from .config import load_config, save_config, DEFAULT_CONFIG

from .icons import create_icon, update_icon

from .hotkey import register_hotkey

from .autoswitch import start_auto_switch

from .utils import run_cmd, xfconf_query_get, xfconf_query_set

# CLI functionality
from .cli import main as cli_main

__all__ = [
    # Theme functions
    'generate_theme_map',
    'get_current_theme', 
    'set_theme',
    'find_counterpart_theme',
    'get_current_mode',
    
    # Config functions
    'load_config',
    'save_config',
    'DEFAULT_CONFIG',
    
    # Icon functions
    'create_icon',
    'update_icon',
    
    # Hotkey functions
    'register_hotkey',
    
    # Auto-switch functions
    'start_auto_switch',
    
    # Utility functions
    'run_cmd',
    'xfconf_query_get',
    'xfconf_query_set',
    
    # CLI
    'cli_main'
]
