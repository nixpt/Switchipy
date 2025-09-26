"""
Configuration management module for Switchipy.

This module handles:
- Loading and saving configuration
- Default configuration values
- Configuration file management
"""

import json
from pathlib import Path

# Configuration file path in user's home directory
CONFIG_PATH = Path.home() / ".switchipy_config.json"

# Default configuration values
DEFAULT_CONFIG = {
    "auto_switch_enabled": False,  # Whether auto-switch is enabled
    "dark_start": "19:00",        # Start time for dark mode (24-hour format)
    "dark_end": "05:00",          # End time for dark mode (24-hour format)
    "last_theme": ""              # Last used theme (for future use)
}

def load_config():
    """
    Load configuration from file or return defaults.
    
    Returns:
        dict: Configuration dictionary with user settings or defaults
    """
    # Check if config file exists
    if CONFIG_PATH.exists():
        try:
            # Load configuration from JSON file
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception:
            # If loading fails, fall back to defaults
            pass
    
    # Return default configuration
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """
    Save configuration to file.
    
    Args:
        config (dict): Configuration dictionary to save
    """
    try:
        # Save configuration as JSON with indentation for readability
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
    except Exception:
        # Print error message if saving fails
        print("[Config] Could not save config")
