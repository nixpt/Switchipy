# Switchipy API Documentation

## Overview

Switchipy is a XFCE theme switcher application that provides automatic and manual theme switching capabilities.

## Core Modules

### themes.py

Theme management and detection functionality.

#### Functions

##### `generate_theme_map() -> dict`
Generates a mapping between light and dark theme variants.

**Returns:**
- `dict`: Mapping of theme names to their counterparts

**Example:**
```python
theme_map = generate_theme_map()
# Returns: {"Adwaita,Adwaita-Light": "Adwaita-Dark", "Adwaita-Dark": "Adwaita,Adwaita-Light"}
```

##### `get_current_theme() -> str`
Gets the currently active theme.

**Returns:**
- `str`: Current theme name

##### `set_theme(theme_name: str) -> None`
Sets the active theme.

**Parameters:**
- `theme_name` (str): Name of the theme to set

##### `find_counterpart_theme(theme_name: str, theme_map: dict) -> str | None`
Finds the counterpart theme (light/dark variant).

**Parameters:**
- `theme_name` (str): Current theme name
- `theme_map` (dict): Theme mapping dictionary

**Returns:**
- `str | None`: Counterpart theme name or None if not found

##### `get_current_mode(theme_name: str = None) -> str`
Determines if current theme is light or dark mode.

**Parameters:**
- `theme_name` (str, optional): Theme name to check, defaults to current theme

**Returns:**
- `str`: "light" or "dark"

### config.py

Configuration management functionality.

#### Functions

##### `load_config() -> dict`
Loads configuration from file or returns defaults.

**Returns:**
- `dict`: Configuration dictionary

##### `save_config(config: dict) -> None`
Saves configuration to file.

**Parameters:**
- `config` (dict): Configuration dictionary to save

#### Constants

##### `DEFAULT_CONFIG`
Default configuration values:
```python
{
    "auto_switch_enabled": False,
    "dark_start": "19:00",
    "dark_end": "05:00",
    "hotkey": "<ctrl>+<alt>+t"
}
```

### icons.py

Icon generation and management.

#### Functions

##### `create_icon(mode: str) -> str`
Creates a theme mode icon.

**Parameters:**
- `mode` (str): "light" or "dark"

**Returns:**
- `str`: Path to created icon file

##### `update_icon(indicator, mode: str) -> None`
Updates the system tray icon.

**Parameters:**
- `indicator`: GTK AppIndicator object
- `mode` (str): "light" or "dark"

### hotkey.py

Global hotkey functionality.

#### Functions

##### `register_hotkey(callback: callable) -> None`
Registers a global hotkey for theme switching.

**Parameters:**
- `callback` (callable): Function to call when hotkey is pressed

**Hotkey:** `Ctrl+Alt+T`

### autoswitch.py

Automatic theme switching based on time.

#### Functions

##### `start_auto_switch(app) -> None`
Starts the auto-switch thread.

**Parameters:**
- `app`: Main application instance

## Main Application

### SwitchipyApp Class

Main application class that coordinates all functionality.

#### Methods

##### `__init__()`
Initializes the application, sets up system tray, and starts background threads.

##### `toggle_theme(_=None) -> None`
Toggles between light and dark themes.

##### `is_dark_time() -> bool`
Checks if current time is within dark mode hours.

**Returns:**
- `bool`: True if dark mode should be active

##### `set_dark_interval(_) -> None`
Opens dialog to set dark mode time interval.

##### `toggle_auto_switch(_) -> None`
Toggles automatic theme switching on/off.

##### `rebuild_menu() -> None`
Rebuilds the system tray context menu.

##### `run() -> None`
Starts the GTK main loop.

## Usage Examples

### Basic Theme Switching

```python
from themes import get_current_theme, set_theme, find_counterpart_theme, generate_theme_map

# Get current theme
current = get_current_theme()
print(f"Current theme: {current}")

# Generate theme map
theme_map = generate_theme_map()

# Find counterpart
counterpart = find_counterpart_theme(current, theme_map)
if counterpart:
    set_theme(counterpart)
```

### Configuration Management

```python
from config import load_config, save_config

# Load configuration
config = load_config()
print(f"Auto-switch enabled: {config['auto_switch_enabled']}")

# Update configuration
config['auto_switch_enabled'] = True
save_config(config)
```

### Hotkey Registration

```python
from hotkey import register_hotkey

def my_callback():
    print("Hotkey pressed!")

register_hotkey(my_callback)
```

## Error Handling

All functions include proper error handling:

- **Theme operations**: Graceful fallback on xfconf-query failures
- **Configuration**: Default values on file read errors
- **Hotkeys**: Optional functionality if pynput unavailable
- **Icons**: Safe file operations with proper cleanup

## Dependencies

- **System**: xfconf-query, zenity
- **Python**: PyGObject, pynput, Pillow
- **Desktop**: XFCE with AppIndicator support
