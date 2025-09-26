#!/usr/bin/env python3
"""
Switchipy Autostart Manager

This script helps users enable/disable Switchipy autostart
for different desktop environments and window managers.
"""

import os
import shutil
import subprocess
from pathlib import Path

# Autostart directories
AUTOSTART_DIRS = {
    'gnome': Path.home() / '.config' / 'autostart',
    'xfce': Path.home() / '.config' / 'autostart',
    'kde': Path.home() / '.config' / 'autostart',
    'i3': Path.home() / '.config' / 'i3',
    'openbox': Path.home() / '.config' / 'openbox',
    'awesome': Path.home() / '.config' / 'awesome',
}

# Desktop file template
DESKTOP_TEMPLATE = """[Desktop Entry]
Type=Application
Name=Switchipy
Comment=XFCE Theme Switcher
Exec=switchipy
Icon=switchipy
Terminal=false
NoDisplay=false
Hidden=false
X-GNOME-Autostart-enabled=true
X-GNOME-Autostart-Delay=10
StartupNotify=false
Categories=System;Settings;
Keywords=theme;dark;light;xfce;switcher;
"""

def detect_desktop_environment():
    """Detect the current desktop environment."""
    desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
    session = os.environ.get('DESKTOP_SESSION', '').lower()
    
    if 'gnome' in desktop or 'gnome' in session:
        return 'gnome'
    elif 'xfce' in desktop or 'xfce' in session:
        return 'xfce'
    elif 'kde' in desktop or 'kde' in session:
        return 'kde'
    elif 'i3' in desktop or 'i3' in session:
        return 'i3'
    elif 'openbox' in desktop or 'openbox' in session:
        return 'openbox'
    elif 'awesome' in desktop or 'awesome' in session:
        return 'awesome'
    else:
        return 'unknown'

def enable_autostart(desktop_env=None):
    """Enable Switchipy autostart for the specified desktop environment."""
    if desktop_env is None:
        desktop_env = detect_desktop_environment()
    
    print(f"🔧 Enabling autostart for {desktop_env}...")
    
    if desktop_env in ['gnome', 'xfce', 'kde']:
        # Use desktop file
        autostart_dir = AUTOSTART_DIRS[desktop_env]
        autostart_dir.mkdir(parents=True, exist_ok=True)
        
        desktop_file = autostart_dir / 'switchipy.desktop'
        with open(desktop_file, 'w') as f:
            f.write(DESKTOP_TEMPLATE)
        
        print(f"  ✓ Created {desktop_file}")
        
    elif desktop_env == 'i3':
        # Add to i3 config
        i3_config = Path.home() / '.config' / 'i3' / 'config'
        if i3_config.exists():
            with open(i3_config, 'r') as f:
                content = f.read()
            
            if 'switchipy' not in content:
                with open(i3_config, 'a') as f:
                    f.write('\n# Switchipy autostart\nexec --no-startup-id switchipy\n')
                print(f"  ✓ Added to {i3_config}")
            else:
                print(f"  ✓ Already configured in {i3_config}")
        else:
            print(f"  ⚠️ i3 config not found at {i3_config}")
    
    elif desktop_env == 'openbox':
        # Add to openbox autostart
        openbox_autostart = Path.home() / '.config' / 'openbox' / 'autostart'
        if openbox_autostart.exists():
            with open(openbox_autostart, 'r') as f:
                content = f.read()
            
            if 'switchipy' not in content:
                with open(openbox_autostart, 'a') as f:
                    f.write('\n# Switchipy autostart\nswitchipy &\n')
                print(f"  ✓ Added to {openbox_autostart}")
            else:
                print(f"  ✓ Already configured in {openbox_autostart}")
        else:
            print(f"  ⚠️ Openbox autostart not found at {openbox_autostart}")
    
    elif desktop_env == 'awesome':
        # Add to awesome config
        awesome_config = Path.home() / '.config' / 'awesome' / 'rc.lua'
        if awesome_config.exists():
            with open(awesome_config, 'r') as f:
                content = f.read()
            
            if 'switchipy' not in content:
                with open(awesome_config, 'a') as f:
                    f.write('\n-- Switchipy autostart\nawful.spawn("switchipy")\n')
                print(f"  ✓ Added to {awesome_config}")
            else:
                print(f"  ✓ Already configured in {awesome_config}")
        else:
            print(f"  ⚠️ Awesome config not found at {awesome_config}")
    
    else:
        print(f"  ⚠️ Unknown desktop environment: {desktop_env}")
        print("  Please configure autostart manually")

def disable_autostart(desktop_env=None):
    """Disable Switchipy autostart for the specified desktop environment."""
    if desktop_env is None:
        desktop_env = detect_desktop_environment()
    
    print(f"�� Disabling autostart for {desktop_env}...")
    
    if desktop_env in ['gnome', 'xfce', 'kde']:
        # Remove desktop file
        autostart_dir = AUTOSTART_DIRS[desktop_env]
        desktop_file = autostart_dir / 'switchipy.desktop'
        
        if desktop_file.exists():
            desktop_file.unlink()
            print(f"  ✓ Removed {desktop_file}")
        else:
            print(f"  ✓ No autostart file found")
    
    elif desktop_env == 'i3':
        # Remove from i3 config
        i3_config = Path.home() / '.config' / 'i3' / 'config'
        if i3_config.exists():
            with open(i3_config, 'r') as f:
                lines = f.readlines()
            
            # Remove switchipy lines
            new_lines = [line for line in lines if 'switchipy' not in line]
            
            if len(new_lines) != len(lines):
                with open(i3_config, 'w') as f:
                    f.writelines(new_lines)
                print(f"  ✓ Removed from {i3_config}")
            else:
                print(f"  ✓ No switchipy configuration found")
    
    elif desktop_env == 'openbox':
        # Remove from openbox autostart
        openbox_autostart = Path.home() / '.config' / 'openbox' / 'autostart'
        if openbox_autostart.exists():
            with open(openbox_autostart, 'r') as f:
                lines = f.readlines()
            
            # Remove switchipy lines
            new_lines = [line for line in lines if 'switchipy' not in line]
            
            if len(new_lines) != len(lines):
                with open(openbox_autostart, 'w') as f:
                    f.writelines(new_lines)
                print(f"  ✓ Removed from {openbox_autostart}")
            else:
                print(f"  ✓ No switchipy configuration found")
    
    elif desktop_env == 'awesome':
        # Remove from awesome config
        awesome_config = Path.home() / '.config' / 'awesome' / 'rc.lua'
        if awesome_config.exists():
            with open(awesome_config, 'r') as f:
                lines = f.readlines()
            
            # Remove switchipy lines
            new_lines = [line for line in lines if 'switchipy' not in line]
            
            if len(new_lines) != len(lines):
                with open(awesome_config, 'w') as f:
                    f.writelines(new_lines)
                print(f"  ✓ Removed from {awesome_config}")
            else:
                print(f"  ✓ No switchipy configuration found")
    
    else:
        print(f"  ⚠️ Unknown desktop environment: {desktop_env}")
        print("  Please remove autostart configuration manually")

def show_status():
    """Show current autostart status."""
    desktop_env = detect_desktop_environment()
    print(f"🖥️ Desktop Environment: {desktop_env}")
    
    if desktop_env in ['gnome', 'xfce', 'kde']:
        autostart_dir = AUTOSTART_DIRS[desktop_env]
        desktop_file = autostart_dir / 'switchipy.desktop'
        
        if desktop_file.exists():
            print(f"  ✓ Autostart enabled: {desktop_file}")
        else:
            print(f"  ✗ Autostart disabled")
    
    elif desktop_env == 'i3':
        i3_config = Path.home() / '.config' / 'i3' / 'config'
        if i3_config.exists():
            with open(i3_config, 'r') as f:
                content = f.read()
            
            if 'switchipy' in content:
                print(f"  ✓ Autostart enabled in {i3_config}")
            else:
                print(f"  ✗ Autostart disabled")
        else:
            print(f"  ✗ i3 config not found")
    
    elif desktop_env == 'openbox':
        openbox_autostart = Path.home() / '.config' / 'openbox' / 'autostart'
        if openbox_autostart.exists():
            with open(openbox_autostart, 'r') as f:
                content = f.read()
            
            if 'switchipy' in content:
                print(f"  ✓ Autostart enabled in {openbox_autostart}")
            else:
                print(f"  ✗ Autostart disabled")
        else:
            print(f"  ✗ Openbox autostart not found")
    
    elif desktop_env == 'awesome':
        awesome_config = Path.home() / '.config' / 'awesome' / 'rc.lua'
        if awesome_config.exists():
            with open(awesome_config, 'r') as f:
                content = f.read()
            
            if 'switchipy' in content:
                print(f"  ✓ Autostart enabled in {awesome_config}")
            else:
                print(f"  ✗ Autostart disabled")
        else:
            print(f"  ✗ Awesome config not found")
    
    else:
        print(f"  ⚠️ Unknown desktop environment")

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) < 2:
        print("Switchipy Autostart Manager")
        print("=" * 30)
        print("Usage:")
        print("  python3 scripts/enable_autostart.py enable [desktop]")
        print("  python3 scripts/enable_autostart.py disable [desktop]")
        print("  python3 scripts/enable_autostart.py status")
        print("")
        print("Supported desktops: gnome, xfce, kde, i3, openbox, awesome")
        return
    
    command = sys.argv[1].lower()
    desktop = sys.argv[2] if len(sys.argv) > 2 else None
    
    if command == 'enable':
        enable_autostart(desktop)
    elif command == 'disable':
        disable_autostart(desktop)
    elif command == 'status':
        show_status()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
