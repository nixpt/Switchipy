#!/usr/bin/env python3
"""
Switchipy - XFCE Theme Switcher
A system tray application for switching between light and dark themes on XFCE.

Features:
- Theme switching with system tray integration
- Auto-switch based on time of day
- Global hotkey support (Ctrl+Alt+T)
- Configuration management
- Theme detection and pairing

Author: Prabin Thapa
License: MIT
"""

import threading
import subprocess
import re
import gi

# Fix GTK version conflicts by requiring specific versions before import
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, AppIndicator3, GLib

# Import from the switchipy package
from switchipy import (
    load_config, save_config,
    generate_theme_map, get_current_theme, set_theme, find_counterpart_theme, get_current_mode,
    update_icon,
    start_auto_switch,
    register_hotkey
)

# Try to import hotkey functionality - make it optional
try:
    from switchipy import register_hotkey
    HOTKEY_AVAILABLE = True
except ImportError:
    HOTKEY_AVAILABLE = False
    print("[App] Hotkey functionality not available - pynput not installed")

class SwitchipyApp:
    """
    Main application class that coordinates all functionality.
    
    This class manages:
    - System tray integration
    - Theme switching logic
    - Configuration management
    - Auto-switch functionality
    - Hotkey registration
    """
    
    def __init__(self):
        """Initialize the application and set up all components."""
        # Load configuration from file or use defaults
        self.config = load_config()
        
        # Generate theme mapping for light/dark pairs
        self.theme_map = generate_theme_map()
        
        # Create system tray indicator
        self.indicator = AppIndicator3.Indicator.new(
            "switchipy",  # Unique identifier
            "",  # Icon path (will be set later)
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        # Set initial icon based on current theme mode
        update_icon(self.indicator, get_current_mode())
        
        # Build the context menu
        self.rebuild_menu()

        # Start auto-switch thread for time-based theme switching
        threading.Thread(target=start_auto_switch, args=(self,), daemon=True).start()
        
        # Register global hotkey if pynput is available
        if HOTKEY_AVAILABLE:
            register_hotkey(self.toggle_theme)
            print("[App] Hotkey registered: Ctrl+Alt+T")
        else:
            print("[App] Hotkey functionality disabled")

    def toggle_theme(self, _=None):
        """
        Toggle between light and dark themes.
        
        Args:
            _: Unused parameter (for compatibility with GTK callbacks)
        """
        # Get current theme
        current = get_current_theme()
        
        # Find the counterpart theme (light <-> dark)
        counterpart = find_counterpart_theme(current, self.theme_map)
        
        if counterpart:
            # Switch to the counterpart theme
            set_theme(counterpart)
            # Update the system tray icon to reflect the new mode
            update_icon(self.indicator, get_current_mode())
        else:
            print(f"[Toggle] No counterpart found for {current}")

    def is_dark_time(self):
        """
        Check if current time is within dark mode hours.
        
        Returns:
            bool: True if dark mode should be active based on time
        """
        from datetime import datetime
        
        # Get current time in HH:MM format
        now = datetime.now().strftime("%H:%M")
        
        # Get configured dark mode time range
        dark_start = self.config["dark_start"]
        dark_end = self.config["dark_end"]
        
        # Handle time ranges that cross midnight (e.g., 22:00 to 06:00)
        if dark_start < dark_end:
            # Normal range (e.g., 19:00 to 05:00)
            return dark_start <= now < dark_end
        else:
            # Cross-midnight range (e.g., 22:00 to 06:00)
            return now >= dark_start or now < dark_end

    def set_dark_interval(self, _):
        """
        Open dialog to set dark mode time interval.
        
        Args:
            _: Unused parameter (for GTK callback compatibility)
        """
        try:
            # Use zenity to show input dialog
            result = subprocess.run([
                "zenity", "--entry", "--title=Set Dark Interval",
                "--text=Enter dark interval HH:MM-HH:MM",
                f"--entry-text={self.config['dark_start']}-{self.config['dark_end']}"
            ], capture_output=True, text=True, check=True)
            
            # Parse the input
            interval = result.stdout.strip()
            
            # Validate format (HH:MM-HH:MM)
            if re.match(r"^\d{2}:\d{2}-\d{2}:\d{2}$", interval):
                start, end = interval.split("-")
                self.config['dark_start'] = start
                self.config['dark_end'] = end
                save_config(self.config)
                self.rebuild_menu()
            else:
                print("Invalid time format. Use HH:MM-HH:MM")
        except Exception as e:
            print(f"Could not set dark interval: {e}")

    def toggle_auto_switch(self, _):
        """
        Toggle automatic theme switching on/off.
        
        Args:
            _: Unused parameter (for GTK callback compatibility)
        """
        # Toggle the auto-switch setting
        self.config['auto_switch_enabled'] = not self.config['auto_switch_enabled']
        
        # Save the updated configuration
        save_config(self.config)
        
        # Rebuild menu to show updated status
        self.rebuild_menu()

    def rebuild_menu(self):
        """Rebuild the system tray context menu with current settings."""
        menu = Gtk.Menu()

        # Main toggle button
        toggle_item = Gtk.MenuItem(label="Toggle Theme")
        toggle_item.connect("activate", self.toggle_theme)
        menu.append(toggle_item)

        menu.append(Gtk.SeparatorMenuItem())

        # Auto-switch toggle with current status
        auto_status = "ON" if self.config.get('auto_switch_enabled', False) else "OFF"
        auto_label = f"Auto-Switch [{auto_status}]"
        auto_item = Gtk.MenuItem(label=auto_label)
        auto_item.connect("activate", self.toggle_auto_switch)
        menu.append(auto_item)

        # Dark interval setting with current values
        interval_label = f"Set Dark Interval ({self.config['dark_start']}-{self.config['dark_end']})"
        interval_item = Gtk.MenuItem(label=interval_label)
        interval_item.connect("activate", self.set_dark_interval)
        menu.append(interval_item)

        # Hotkey info (if available)
        if HOTKEY_AVAILABLE:
            hotkey_item = Gtk.MenuItem(label="Hotkey: Ctrl+Alt+T")
            hotkey_item.set_sensitive(False)  # Make it non-clickable (info only)
            menu.append(hotkey_item)

        menu.append(Gtk.SeparatorMenuItem())

        # Theme selection submenus
        light_submenu = Gtk.Menu()
        dark_submenu = Gtk.Menu()

        # Populate theme submenus based on detected themes
        for key, value in self.theme_map.items():
            if "dark" in key.lower():
                # Add dark themes to dark submenu
                for theme in key.split(","):
                    item = Gtk.MenuItem(label=theme)
                    item.connect("activate", lambda _, t=theme: set_theme(t))
                    dark_submenu.append(item)
            else:
                # Add light themes to light submenu
                for theme in key.split(","):
                    item = Gtk.MenuItem(label=theme)
                    item.connect("activate", lambda _, t=theme: set_theme(t))
                    light_submenu.append(item)

        # Create submenu items
        light_item = Gtk.MenuItem(label="Light Themes")
        light_item.set_submenu(light_submenu)
        dark_item = Gtk.MenuItem(label="Dark Themes")
        dark_item.set_submenu(dark_submenu)

        menu.append(light_item)
        menu.append(dark_item)

        menu.append(Gtk.SeparatorMenuItem())

        # Quit option
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", lambda _: Gtk.main_quit())
        menu.append(quit_item)

        # Show all menu items and set the menu
        menu.show_all()
        self.indicator.set_menu(menu)

    def run(self):
        """Start the GTK main loop to run the application."""
        Gtk.main()

def main():
    """
    Main entry point for the application.
    
    Checks for required system dependencies and starts the application.
    """
    # Check for required system commands
    required_commands = ["xfconf-query", "zenity"]
    
    for cmd in required_commands:
        try:
            subprocess.run(["which", cmd], check=True, capture_output=True)
        except Exception:
            print(f"FATAL: '{cmd}' command not found. Please install it.")
            exit(1)

    # Create and run the application
    app = SwitchipyApp()
    app.run()

if __name__ == "__main__":
    main()
