#!/usr/bin/env python3
"""
Switchipy Theme Automation Example

This script demonstrates how to use Switchipy programmatically
for advanced theme automation scenarios.
"""

import time
import subprocess
from datetime import datetime, timedelta

def run_switchipy_cli(command):
    """Run a switchipy-cli command and return the output."""
    try:
        result = subprocess.run(
            ['switchipy-cli'] + command,
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return None

def get_current_theme():
    """Get the current theme."""
    output = run_switchipy_cli(['current'])
    if output:
        for line in output.split('\n'):
            if line.startswith('Current Theme:'):
                return line.split(': ')[1]
    return None

def is_dark_time():
    """Check if it's currently dark time."""
    output = run_switchipy_cli(['time'])
    if output:
        return 'Yes' in output
    return False

def set_theme(theme_name):
    """Set a specific theme."""
    return run_switchipy_cli(['set', theme_name])

def toggle_theme():
    """Toggle between light and dark themes."""
    return run_switchipy_cli(['toggle'])

def list_themes():
    """List all available themes."""
    return run_switchipy_cli(['list'])

def main():
    """Main automation example."""
    print("🎨 Switchipy Theme Automation Example")
    print("=" * 40)
    
    # Show current status
    print(f"Current theme: {get_current_theme()}")
    print(f"Is dark time: {is_dark_time()}")
    
    # List available themes
    print("\nAvailable themes:")
    themes = list_themes()
    if themes:
        print(themes)
    
    # Demonstrate theme switching
    print("\n🔄 Demonstrating theme switching...")
    
    # Toggle theme
    print("Toggling theme...")
    toggle_theme()
    time.sleep(1)
    print(f"New theme: {get_current_theme()}")
    
    # Toggle back
    print("Toggling back...")
    toggle_theme()
    time.sleep(1)
    print(f"Final theme: {get_current_theme()}")
    
    print("\n✅ Automation example complete!")

if __name__ == "__main__":
    main()
