#!/usr/bin/env python3
"""
Command Line Interface for Switchipy.

This module provides a CLI for controlling theme switching from the command line.
"""

import argparse
import sys
import json
from datetime import datetime
from . import (
    get_current_theme, set_theme, get_current_mode,
    generate_theme_map, find_counterpart_theme,
    load_config, save_config, DEFAULT_CONFIG
)

def list_themes():
    """List all available themes grouped by light/dark variants."""
    theme_map = generate_theme_map()
    
    if not theme_map:
        print("No theme pairs found.")
        return
    
    print("Available Theme Pairs:")
    print("=" * 50)
    
    for light_themes, dark_themes in theme_map.items():
        if "dark" not in light_themes.lower():
            print(f"Light: {light_themes}")
            print(f"Dark:  {dark_themes}")
            print("-" * 30)

def show_current():
    """Show current theme and mode."""
    current_theme = get_current_theme()
    current_mode = get_current_mode()
    
    print(f"Current Theme: {current_theme}")
    print(f"Current Mode:  {current_mode}")

def toggle_theme():
    """Toggle between light and dark themes."""
    current_theme = get_current_theme()
    theme_map = generate_theme_map()
    counterpart = find_counterpart_theme(current_theme, theme_map)
    
    if counterpart:
        set_theme(counterpart)
        new_mode = get_current_mode()
        print(f"Switched to: {counterpart} ({new_mode} mode)")
    else:
        print(f"No counterpart found for {current_theme}")
        print("Available themes:")
        list_themes()

def set_theme_by_name(theme_name):
    """Set a specific theme by name."""
    set_theme(theme_name)
    new_mode = get_current_mode()
    print(f"Set theme to: {theme_name} ({new_mode} mode)")

def show_config():
    """Show current configuration."""
    config = load_config()
    
    print("Current Configuration:")
    print("=" * 30)
    for key, value in config.items():
        print(f"{key}: {value}")

def set_auto_switch(enabled):
    """Enable or disable auto-switch."""
    config = load_config()
    config['auto_switch_enabled'] = enabled
    save_config(config)
    
    status = "enabled" if enabled else "disabled"
    print(f"Auto-switch {status}")

def set_dark_interval(start_time, end_time):
    """Set dark mode time interval."""
    config = load_config()
    config['dark_start'] = start_time
    config['dark_end'] = end_time
    save_config(config)
    
    print(f"Dark mode interval set to: {start_time} - {end_time}")

def is_dark_time():
    """Check if current time is within dark mode hours."""
    config = load_config()
    now = datetime.now().strftime("%H:%M")
    dark_start = config['dark_start']
    dark_end = config['dark_end']
    
    if dark_start < dark_end:
        is_dark = dark_start <= now < dark_end
    else:
        is_dark = now >= dark_start or now < dark_end
    
    print(f"Current time: {now}")
    print(f"Dark mode hours: {dark_start} - {dark_end}")
    print(f"Should be dark mode: {'Yes' if is_dark else 'No'}")
    
    return is_dark

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Switchipy CLI - XFCE Theme Switcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  switchipy list                    # List available themes
  switchipy current                 # Show current theme
  switchipy toggle                  # Toggle between light/dark
  switchipy set Adwaita-Dark        # Set specific theme
  switchipy config                  # Show configuration
  switchipy auto on                 # Enable auto-switch
  switchipy interval 19:00 05:00    # Set dark mode hours
  switchipy time                    # Check if should be dark mode
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List themes command
    subparsers.add_parser('list', help='List available theme pairs')
    
    # Show current command
    subparsers.add_parser('current', help='Show current theme and mode')
    
    # Toggle command
    subparsers.add_parser('toggle', help='Toggle between light and dark themes')
    
    # Set theme command
    set_parser = subparsers.add_parser('set', help='Set specific theme')
    set_parser.add_argument('theme', help='Theme name to set')
    
    # Config command
    subparsers.add_parser('config', help='Show current configuration')
    
    # Auto-switch commands
    auto_parser = subparsers.add_parser('auto', help='Control auto-switch')
    auto_parser.add_argument('state', choices=['on', 'off'], help='Enable or disable auto-switch')
    
    # Interval command
    interval_parser = subparsers.add_parser('interval', help='Set dark mode time interval')
    interval_parser.add_argument('start', help='Start time (HH:MM)')
    interval_parser.add_argument('end', help='End time (HH:MM)')
    
    # Time check command
    subparsers.add_parser('time', help='Check if current time is within dark mode hours')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Execute commands
        if args.command == 'list':
            list_themes()
        elif args.command == 'current':
            show_current()
        elif args.command == 'toggle':
            toggle_theme()
        elif args.command == 'set':
            set_theme_by_name(args.theme)
        elif args.command == 'config':
            show_config()
        elif args.command == 'auto':
            set_auto_switch(args.state == 'on')
        elif args.command == 'interval':
            set_dark_interval(args.start, args.end)
        elif args.command == 'time':
            is_dark_time()
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
