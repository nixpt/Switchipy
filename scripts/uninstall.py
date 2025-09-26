#!/usr/bin/env python3
"""
Switchipy Uninstallation Script

This script removes Switchipy from the system.
"""

import os
import shutil
from pathlib import Path

# Installation paths
INSTALL_DIR = Path.home() / ".local" / "share" / "switchipy"
BIN_DIR = Path.home() / ".local" / "bin"
DESKTOP_DIR = Path.home() / ".local" / "share" / "applications"
ICON_DIR = Path.home() / ".local" / "share" / "icons"
CONFIG_FILE = Path.home() / ".switchipy_config.json"

def remove_files():
    """Remove installed files."""
    print("🗑️ Removing files...")
    
    # Remove installation directory
    if INSTALL_DIR.exists():
        shutil.rmtree(INSTALL_DIR)
        print(f"  ✓ Removed {INSTALL_DIR}")
    
    # Remove launcher scripts
    launcher_scripts = [
        BIN_DIR / "switchipy",
        BIN_DIR / "switchipy-cli"
    ]
    
    for script in launcher_scripts:
        if script.exists():
            script.unlink()
            print(f"  ✓ Removed {script}")
    
    # Remove desktop file
    desktop_file = DESKTOP_DIR / "switchipy.desktop"
    if desktop_file.exists():
        desktop_file.unlink()
        print(f"  ✓ Removed {desktop_file}")
    
    # Remove icon
    icon_file = ICON_DIR / "switchipy.svg"
    if icon_file.exists():
        icon_file.unlink()
        print(f"  ✓ Removed {icon_file}")

def remove_config():
    """Remove configuration file (with confirmation)."""
    if CONFIG_FILE.exists():
        response = input(f"Remove configuration file {CONFIG_FILE}? [y/N]: ")
        if response.lower() in ['y', 'yes']:
            CONFIG_FILE.unlink()
            print(f"  ✓ Removed {CONFIG_FILE}")
        else:
            print(f"  ⚠️ Kept {CONFIG_FILE}")

def main():
    """Main uninstallation function."""
    print("🗑️ Switchipy Uninstallation")
    print("=" * 50)
    
    # Confirm uninstallation
    response = input("Are you sure you want to uninstall Switchipy? [y/N]: ")
    if response.lower() not in ['y', 'yes']:
        print("Uninstallation cancelled.")
        return
    
    # Remove files
    remove_files()
    
    # Remove config (with confirmation)
    remove_config()
    
    print("\n✅ Uninstallation complete!")
    print("Switchipy has been removed from your system.")

if __name__ == "__main__":
    main()
