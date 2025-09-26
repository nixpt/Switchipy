"""
Utility functions for Switchipy.

This module provides:
- Command execution helpers
- XFCE configuration utilities
- Error handling for system commands
"""

import subprocess

def run_cmd(cmd):
    """
    Execute a system command and return the output.
    
    Args:
        cmd (list): Command and arguments as a list
        
    Returns:
        str | None: Command output or None if command failed
    """
    try:
        # Run command and capture output
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        # Return None if command failed
        return None

def xfconf_query_get(channel, prop):
    """
    Get a value from XFCE configuration.
    
    Args:
        channel (str): XFCE configuration channel (e.g., 'xsettings')
        prop (str): Property path (e.g., '/Net/ThemeName')
        
    Returns:
        str | None: Configuration value or None if not found
    """
    return run_cmd(["xfconf-query", "-c", channel, "-p", prop])

def xfconf_query_set(channel, prop, value):
    """
    Set a value in XFCE configuration.
    
    Args:
        channel (str): XFCE configuration channel (e.g., 'xsettings')
        prop (str): Property path (e.g., '/Net/ThemeName')
        value (str): Value to set
    """
    run_cmd(["xfconf-query", "-c", channel, "-p", prop, "-s", value])
