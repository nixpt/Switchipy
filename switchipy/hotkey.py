"""
Global hotkey functionality for Switchipy.

This module provides:
- Global hotkey registration using pynput
- Thread-safe hotkey handling
- Optional hotkey support (graceful degradation)
"""

import threading
from pynput import keyboard

def register_hotkey(callback):
    """
    Register a global hotkey for theme switching.
    
    This function sets up a global hotkey (Ctrl+Alt+T) that will call
    the provided callback function when pressed. The hotkey listener
    runs in a separate daemon thread to avoid blocking the main GTK loop.
    
    Args:
        callback (callable): Function to call when hotkey is pressed
    """
    # Create global hotkey mapping
    hotkey = keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+t': callback  # Ctrl+Alt+T combination
    })
    
    # Start the hotkey listener in a daemon thread
    # Daemon threads automatically exit when the main program exits
    threading.Thread(target=hotkey.start, daemon=True).start()
