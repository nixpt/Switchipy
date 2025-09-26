# Switchipy CLI Documentation

## Overview

Switchipy provides a comprehensive command-line interface for controlling theme switching from the terminal. This is perfect for scripting, automation, and quick theme management.

## Installation

The CLI is included with the main Switchipy package. No additional installation is required.

## Usage

### Basic Syntax

```bash
python3 switchipy_cli.py <command> [options]
```

### Available Commands

#### 1. List Available Themes

```bash
python3 switchipy_cli.py list
```

Shows all available light/dark theme pairs detected on your system.

**Example Output:**
```
Available Theme Pairs:
==================================================
Light: Adwaita
Dark:  Adwaita-dark
------------------------------
Light: WhiteSur-Light
Dark:  WhiteSur-Dark
------------------------------
```

#### 2. Show Current Theme

```bash
python3 switchipy_cli.py current
```

Displays the currently active theme and mode.

**Example Output:**
```
Current Theme: WhiteSur-Dark
Current Mode:  dark
```

#### 3. Toggle Theme

```bash
python3 switchipy_cli.py toggle
```

Switches between light and dark variants of the current theme.

**Example Output:**
```
Switched to: WhiteSur-Light (light mode)
```

#### 4. Set Specific Theme

```bash
python3 switchipy_cli.py set <theme-name>
```

Sets a specific theme by name.

**Examples:**
```bash
python3 switchipy_cli.py set Adwaita-dark
python3 switchipy_cli.py set WhiteSur-Light
```

#### 5. Show Configuration

```bash
python3 switchipy_cli.py config
```

Displays current configuration settings.

**Example Output:**
```
Current Configuration:
==============================
auto_switch_enabled: True
dark_start: 19:00
dark_end: 05:00
last_theme: WhiteSur-Dark
```

#### 6. Control Auto-Switch

```bash
python3 switchipy_cli.py auto on    # Enable auto-switch
python3 switchipy_cli.py auto off   # Disable auto-switch
```

#### 7. Set Dark Mode Hours

```bash
python3 switchipy_cli.py interval <start-time> <end-time>
```

Sets the time interval for automatic dark mode activation.

**Examples:**
```bash
python3 switchipy_cli.py interval 19:00 05:00    # 7 PM to 5 AM
python3 switchipy_cli.py interval 20:00 06:00    # 8 PM to 6 AM
```

#### 8. Check Time Status

```bash
python3 switchipy_cli.py time
```

Checks if the current time is within dark mode hours.

**Example Output:**
```
Current time: 21:30
Dark mode hours: 19:00 - 05:00
Should be dark mode: Yes
```

## Scripting Examples

### Bash Script for Time-Based Theme Switching

```bash
#!/bin/bash
# Auto theme switcher script

# Check if it's dark time
if python3 switchipy_cli.py time | grep -q "Yes"; then
    # Switch to dark theme
    python3 switchipy_cli.py set WhiteSur-Dark
else
    # Switch to light theme
    python3 switchipy_cli.py set WhiteSur-Light
fi
```

### Python Script for Theme Management

```python
#!/usr/bin/env python3
import subprocess
import sys

def run_cli(command):
    """Run a CLI command and return output."""
    result = subprocess.run(
        ['python3', 'switchipy_cli.py'] + command,
        capture_output=True, text=True
    )
    return result.stdout.strip()

# Get current theme
current = run_cli(['current'])
print(f"Current: {current}")

# Toggle theme
run_cli(['toggle'])
print("Theme toggled")

# Check if should be dark mode
time_check = run_cli(['time'])
print(f"Time check: {time_check}")
```

### Cron Job for Automatic Theme Switching

Add to crontab (`crontab -e`):

```bash
# Switch to dark theme at 7 PM
0 19 * * * /path/to/switchipy_cli.py set WhiteSur-Dark

# Switch to light theme at 6 AM
0 6 * * * /path/to/switchipy_cli.py set WhiteSur-Light
```

## Error Handling

The CLI provides clear error messages for common issues:

- **Theme not found**: "No counterpart found for <theme-name>"
- **Invalid time format**: "Invalid time format. Use HH:MM"
- **Configuration errors**: "Error: <error-message>"

## Integration with System Tray App

The CLI and system tray application share the same configuration file (`~/.switchipy_config.json`), so changes made via CLI are immediately reflected in the GUI and vice versa.

## Advanced Usage

### Batch Operations

```bash
# Set up automatic dark mode for winter
python3 switchipy_cli.py interval 17:00 07:00
python3 switchipy_cli.py auto on

# Quick theme switching for presentations
python3 switchipy_cli.py set Adwaita        # Light theme
python3 switchipy_cli.py set Adwaita-dark  # Dark theme
```

### Monitoring and Logging

```bash
# Log theme changes
echo "$(date): $(python3 switchipy_cli.py current)" >> ~/theme-log.txt

# Check theme status periodically
watch -n 60 'python3 switchipy_cli.py current'
```

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure you have access to XFCE configuration
2. **Theme Not Found**: Use `list` command to see available themes
3. **Time Format**: Use 24-hour format (HH:MM) for time settings

### Debug Mode

For detailed error information, run with Python's verbose mode:

```bash
python3 -v switchipy_cli.py current
```

## Aliases and Shortcuts

Add to your shell configuration (`.bashrc` or `.zshrc`):

```bash
# Short aliases
alias theme='python3 /path/to/switchipy_cli.py'
alias theme-toggle='python3 /path/to/switchipy_cli.py toggle'
alias theme-current='python3 /path/to/switchipy_cli.py current'
alias theme-list='python3 /path/to/switchipy_cli.py list'

# Usage
theme current
theme-toggle
theme-list
```
