"""
Theme management module for Switchipy.

This module handles:
- Theme detection and mapping
- Getting/setting current theme
- Finding light/dark theme counterparts
- Theme mode detection (light/dark)
"""

import collections
import re
from pathlib import Path
from .utils import xfconf_query_get, xfconf_query_set

# Theme directories to scan for available themes
THEME_DIRS = [
    Path.home() / ".themes",  # User themes
    Path("/usr/share/themes"),  # System themes
]

# XFCE configuration settings
XFCONF_CHANNEL = "xsettings"
XFCONF_PROPERTY = "/Net/ThemeName"

def list_all_themes():
    """
    Get a list of all available themes.
    
    Returns:
        set: Set of theme names found in theme directories
    """
    themes = set()
    
    # Scan each theme directory
    for directory in THEME_DIRS:
        if not directory.exists():
            continue
            
        # Get all subdirectories (themes)
        for theme_path in directory.iterdir():
            if theme_path.is_dir():
                themes.add(theme_path.name)
    
    return sorted(themes)

def generate_theme_map():
    """
    Generate a mapping between light and dark theme variants.
    
    This function scans theme directories and creates mappings between
    light and dark variants of the same theme (e.g., Adwaita <-> Adwaita-Dark).
    
    Returns:
        dict: Mapping of theme names to their counterparts
              Format: {"light1,light2": "dark1", "dark1": "light1,light2"}
    """
    # Group themes by base name (removing -dark, -light, -black, -noir suffixes)
    theme_groups = collections.defaultdict(list)
    
    # Scan theme directories
    for directory in THEME_DIRS:
        if not directory.exists():
            continue
            
        for theme_path in directory.iterdir():
            if not theme_path.is_dir():
                continue
                
            theme_name = theme_path.name
            
            # Remove common dark/light suffixes to get base name
            base_name = re.sub(r"-(dark|light|black|noir)", "", theme_name, flags=re.IGNORECASE)
            theme_groups[base_name].append(theme_name)
    
    # Create mappings between light and dark variants
    mapping = {}
    
    for base_name, themes in theme_groups.items():
        light_variants = []
        dark_variants = []
        
        # Separate light and dark variants
        for theme in themes:
            if re.search(r"dark|black|noir", theme, flags=re.IGNORECASE):
                dark_variants.append(theme)
            else:
                light_variants.append(theme)
        
        # Create bidirectional mapping if both variants exist
        if light_variants and dark_variants:
            # Sort for consistent ordering
            light_str = ",".join(sorted(light_variants))
            dark_str = ",".join(sorted(dark_variants))
            
            # Create bidirectional mapping
            mapping[light_str] = dark_str
            mapping[dark_str] = light_str
    
    return mapping

def get_current_theme():
    """
    Get the currently active theme.
    
    Returns:
        str: Current theme name, or empty string if not found
    """
    return xfconf_query_get(XFCONF_CHANNEL, XFCONF_PROPERTY) or ""

def set_theme(theme_name):
    """
    Set the active theme.
    
    Args:
        theme_name (str): Name of the theme to set
    """
    # Set the main theme
    xfconf_query_set(XFCONF_CHANNEL, XFCONF_PROPERTY, theme_name)
    
    # Also set XFWM (window manager) theme if it exists
    for directory in THEME_DIRS:
        xfwm_path = directory / theme_name / "xfwm4"
        if xfwm_path.exists():
            xfconf_query_set("xfwm4", "/general/theme", theme_name)
            break

def find_counterpart_theme(theme_name, theme_map):
    """
    Find the counterpart theme (light <-> dark variant).
    
    Args:
        theme_name (str): Current theme name
        theme_map (dict): Theme mapping dictionary
        
    Returns:
        str | None: Counterpart theme name or None if not found
    """
    # Search through theme mappings
    for key, value in theme_map.items():
        # Check if current theme is in the key (light themes)
        if theme_name in key.split(","):
            return value.split(",")[0]  # Return first dark variant
        
        # Check if current theme is in the value (dark themes)
        if theme_name in value.split(","):
            return key.split(",")[0]  # Return first light variant
    
    return None

def get_current_mode(theme_name=None):
    """
    Determine if current theme is light or dark mode.
    
    Args:
        theme_name (str, optional): Theme name to check. 
                                   If None, uses current theme.
    
    Returns:
        str: "light" or "dark"
    """
    # Use provided theme name or get current theme
    if theme_name is None:
        theme_name = get_current_theme()
    
    # Check for dark mode indicators in theme name
    if re.search(r"dark|black|noir", theme_name, flags=re.IGNORECASE):
        return "dark"
    else:
        return "light"
