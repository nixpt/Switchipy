#!/usr/bin/env python3
"""
Switchipy Installation Script

This script installs Switchipy to the user's local directory and creates
necessary symlinks and desktop files for system integration.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import json

# Installation paths
INSTALL_DIR = Path.home() / ".local" / "share" / "switchipy"
BIN_DIR = Path.home() / ".local" / "bin"
DESKTOP_DIR = Path.home() / ".local" / "share" / "applications"
ICON_DIR = Path.home() / ".local" / "share" / "icons"

def check_dependencies():
    """Check if required system dependencies are available."""
    print("🔍 Checking dependencies...")
    
    required_commands = ["xfconf-query", "zenity"]
    missing = []
    
    for cmd in required_commands:
        try:
            subprocess.run(["which", cmd], check=True, capture_output=True)
            print(f"  ✓ {cmd}")
        except subprocess.CalledProcessError:
            missing.append(cmd)
            print(f"  ✗ {cmd}")
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("Please install them first:")
        print("  Arch/Manjaro: sudo pacman -S xfconf zenity")
        print("  Ubuntu/Debian: sudo apt install xfconf zenity")
        return False
    
    return True

def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    
    directories = [INSTALL_DIR, BIN_DIR, DESKTOP_DIR, ICON_DIR]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}")

def install_files():
    """Install Switchipy files to the installation directory."""
    print("📦 Installing files...")
    
    # Files to install
    files_to_install = [
        "app.py",
        "switchipy_cli.py", 
        "requirements.txt",
        "README.md",
        "LICENSE"
    ]
    
    # Copy files
    for file in files_to_install:
        if os.path.exists(file):
            shutil.copy2(file, INSTALL_DIR / file)
            print(f"  ✓ {file}")
    
    # Copy switchipy package directory
    if os.path.exists("switchipy"):
        shutil.copytree("switchipy", INSTALL_DIR / "switchipy", dirs_exist_ok=True)
        print("  ✓ switchipy/ package")
    
    # Copy tests directory
    if os.path.exists("tests"):
        shutil.copytree("tests", INSTALL_DIR / "tests", dirs_exist_ok=True)
        print("  ✓ tests/ directory")
    
    # Copy docs directory
    if os.path.exists("docs"):
        shutil.copytree("docs", INSTALL_DIR / "docs", dirs_exist_ok=True)
        print("  ✓ docs/ directory")

def create_launcher_scripts():
    """Create launcher scripts."""
    print("🚀 Creating launcher scripts...")
    
    # GUI launcher
    gui_script = BIN_DIR / "switchipy"
    with open(gui_script, 'w') as f:
        f.write(f'''#!/usr/bin/env python3
"""
Switchipy GUI Launcher
"""
import sys
import os
sys.path.insert(0, "{INSTALL_DIR}")
os.chdir("{INSTALL_DIR}")
from app import main
if __name__ == "__main__":
    main()
''')
    gui_script.chmod(0o755)
    print(f"  ✓ {gui_script}")
    
    # CLI launcher
    cli_script = BIN_DIR / "switchipy-cli"
    with open(cli_script, 'w') as f:
        f.write(f'''#!/usr/bin/env python3
"""
Switchipy CLI Launcher
"""
import sys
import os
sys.path.insert(0, "{INSTALL_DIR}")
os.chdir("{INSTALL_DIR}")
from switchipy_cli import main
if __name__ == "__main__":
    main()
''')
    cli_script.chmod(0o755)
    print(f"  ✓ {cli_script}")

def create_desktop_file():
    """Create desktop file for system integration."""
    print("🖥️ Creating desktop file...")
    
    desktop_file = DESKTOP_DIR / "switchipy.desktop"
    with open(desktop_file, 'w') as f:
        f.write(f'''[Desktop Entry]
Name=Switchipy
Comment=XFCE Theme Switcher
Exec={BIN_DIR}/switchipy
Icon=switchipy
Terminal=false
Type=Application
Categories=System;Settings;
StartupNotify=true
''')
    print(f"  ✓ {desktop_file}")

def create_icon():
    """Create application icon."""
    print("🎨 Creating application icon...")
    
    # Create a simple SVG icon
    icon_svg = ICON_DIR / "switchipy.svg"
    with open(icon_svg, 'w') as f:
        f.write('''<?xml version="1.0" encoding="UTF-8"?>
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <circle cx="20" cy="32" r="12" fill="#FFD700" stroke="#333" stroke-width="2"/>
  <circle cx="44" cy="32" r="12" fill="#606060" stroke="#333" stroke-width="2"/>
  <circle cx="32" cy="32" r="8" fill="#FFD700"/>
</svg>''')
    print(f"  ✓ {icon_svg}")

def install_python_dependencies():
    """Install Python dependencies."""
    print("🐍 Installing Python dependencies...")
    
    try:
        # Install dependencies to user directory
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--user", 
            "--break-system-packages", "-r", str(INSTALL_DIR / "requirements.txt")
        ], check=True)
        print("  ✓ Python dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"  ⚠️ Warning: Could not install dependencies: {e}")
        print("  You may need to install them manually:")
        print("    pip install --user pynput Pillow")

def create_config():
    """Create initial configuration."""
    print("⚙️ Creating configuration...")
    
    config_file = Path.home() / ".switchipy_config.json"
    if not config_file.exists():
        default_config = {
            "auto_switch_enabled": False,
            "dark_start": "19:00",
            "dark_end": "05:00",
            "last_theme": ""
        }
        
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        print(f"  ✓ {config_file}")

def update_shell_profile():
    """Update shell profile to include bin directory in PATH."""
    print("🔧 Updating shell profile...")
    
    shell_profile = None
    if os.path.exists(str(Path.home() / ".bashrc")):
        shell_profile = Path.home() / ".bashrc"
    elif os.path.exists(str(Path.home() / ".zshrc")):
        shell_profile = Path.home() / ".zshrc"
    
    if shell_profile:
        # Check if PATH already includes the bin directory
        with open(shell_profile, 'r') as f:
            content = f.read()
        
        if str(BIN_DIR) not in content:
            with open(shell_profile, 'a') as f:
                f.write(f'''
# Switchipy PATH
export PATH="$PATH:{BIN_DIR}"
''')
            print(f"  ✓ Updated {shell_profile}")
        else:
            print(f"  ✓ {shell_profile} already configured")
    else:
        print("  ⚠️ Could not find shell profile to update")

def main():
    """Main installation function."""
    print("🚀 Switchipy Installation")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py") or not os.path.exists("switchipy"):
        print("❌ Error: Please run this script from the Switchipy source directory")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install files
    install_files()
    
    # Create launcher scripts
    create_launcher_scripts()
    
    # Create desktop file
    create_desktop_file()
    
    # Create icon
    create_icon()
    
    # Install Python dependencies
    install_python_dependencies()
    
    # Create configuration
    create_config()
    
    # Update shell profile
    update_shell_profile()
    
    print("\n🎉 Installation complete!")
    print("\nTo use Switchipy:")
    print(f"  GUI: {BIN_DIR}/switchipy")
    print(f"  CLI: {BIN_DIR}/switchipy-cli")
    print("\nYou may need to restart your shell or run:")
    print(f"  export PATH=\"$PATH:{BIN_DIR}\"")
    print("\nTo uninstall, run:")
    print(f"  rm -rf {INSTALL_DIR}")
    print(f"  rm -f {BIN_DIR}/switchipy {BIN_DIR}/switchipy-cli")
    print(f"  rm -f {DESKTOP_DIR}/switchipy.desktop")

if __name__ == "__main__":
    main()
