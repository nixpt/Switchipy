"""
Automatic theme switching based on time of day.

This module provides:
- Time-based theme switching
- Dark mode time detection
- Background thread management
"""

import time
from .themes import get_current_mode

def start_auto_switch(app):
    """
    Start the auto-switch thread that monitors time and switches themes.
    
    This function runs in a continuous loop, checking every minute if
    the theme should be switched based on the current time and configured
    dark mode hours.
    
    Args:
        app: Main application instance with config and toggle_theme method
    """
    while True:
        try:
            # Only proceed if auto-switch is enabled
            if app.config.get('auto_switch_enabled', False):
                # Get current theme mode
                current_mode = get_current_mode()
                
                # Check if we should be in dark mode based on time
                should_be_dark = app.is_dark_time()
                
                # Switch to dark theme if it's dark time but we're in light mode
                if should_be_dark and current_mode == "light":
                    app.toggle_theme()
                
                # Switch to light theme if it's light time but we're in dark mode
                elif not should_be_dark and current_mode == "dark":
                    app.toggle_theme()
            
            # Wait 60 seconds before next check
            time.sleep(60)
            
        except Exception as e:
            # Log errors but continue running
            print(f"[AutoSwitch] Error: {e}")
            time.sleep(60)  # Wait before retrying
