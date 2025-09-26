# Switchipy Installation Guide

## Quick Installation

### Automatic Installation

```bash
# Clone or download Switchipy
git clone <repository-url>
cd LightSwitch

# Run the installer
make install
# or
python3 scripts/install.py
```

### Manual Installation

```bash
# Install system dependencies first
sudo pacman -S xfconf zenity  # Arch/Manjaro
# or
sudo apt install xfconf zenity  # Ubuntu/Debian

# Install Python dependencies
pip install --user pynput Pillow

# Run the installer
python3 scripts/install.py
```

## Installation Details

The installer will:

1. **Check Dependencies**: Verify `xfconf-query` and `zenity` are available
2. **Create Directories**: Set up `~/.local/share/switchipy/`
3. **Install Files**: Copy all Switchipy files to the installation directory
4. **Create Launchers**: Add `switchipy` and `switchipy-cli` to `~/.local/bin/`
5. **Desktop Integration**: Create desktop file for system integration
6. **Install Dependencies**: Install Python packages
7. **Create Config**: Set up initial configuration
8. **Update PATH**: Add `~/.local/bin` to your shell profile

## Installation Locations

```
~/.local/share/switchipy/     # Main application files
~/.local/bin/switchipy        # GUI launcher
~/.local/bin/switchipy-cli    # CLI launcher
~/.local/share/applications/switchipy.desktop  # Desktop file
~/.local/share/icons/switchipy.svg  # Application icon
~/.switchipy_config.json      # Configuration file
```

## Usage After Installation

### GUI Application
```bash
switchipy
```

### Command Line Interface
```bash
switchipy-cli --help
switchipy-cli current
switchipy-cli toggle
```

### Desktop Integration
- Look for "Switchipy" in your application menu
- Add to favorites or dock for quick access

## Uninstallation

### Automatic Uninstallation
```bash
make uninstall
# or
python3 scripts/uninstall.py
```

### Manual Uninstallation
```bash
# Remove files
rm -rf ~/.local/share/switchipy
rm -f ~/.local/bin/switchipy
rm -f ~/.local/bin/switchipy-cli
rm -f ~/.local/share/applications/switchipy.desktop
rm -f ~/.local/share/icons/switchipy.svg

# Remove config (optional)
rm -f ~/.switchipy_config.json
```

## Troubleshooting

### PATH Issues
If commands are not found after installation:

```bash
# Add to PATH temporarily
export PATH="$PATH:$HOME/.local/bin"

# Or restart your shell
source ~/.bashrc  # or ~/.zshrc
```

### Permission Issues
```bash
# Make sure scripts are executable
chmod +x ~/.local/bin/switchipy
chmod +x ~/.local/bin/switchipy-cli
```

### Dependency Issues
```bash
# Check if dependencies are installed
which xfconf-query
which zenity

# Install missing dependencies
sudo pacman -S xfconf zenity  # Arch/Manjaro
sudo apt install xfconf zenity  # Ubuntu/Debian
```

### Python Dependencies
```bash
# Install Python packages manually
pip install --user --break-system-packages pynput Pillow
```

## Development Installation

For development work:

```bash
# Clone repository
git clone <repository-url>
cd LightSwitch

# Install in development mode
make install

# Run tests
make test

# Run from source
python3 app.py
python3 switchipy_cli.py
```

## System Requirements

- **Operating System**: Linux (XFCE desktop environment)
- **Python**: 3.6 or higher
- **Dependencies**: 
  - `xfconf-query` (XFCE configuration tool)
  - `zenity` (GTK dialog tool)
  - `pynput` (Python package for hotkeys)
  - `Pillow` (Python package for image processing)

## Package Management

### Create Distribution Package
```bash
make package
# Creates: dist/switchipy-YYYYMMDD.tar.gz
```

### Install from Package
```bash
# Extract package
tar -xzf switchipy-YYYYMMDD.tar.gz
cd LightSwitch

# Install
make install
```

## Advanced Configuration

### Custom Installation Directory
Edit `scripts/install.py` and change the `INSTALL_DIR` variable:

```python
INSTALL_DIR = Path.home() / ".local" / "share" / "my-custom-switchipy"
```

### System-wide Installation
For system-wide installation (requires root):

```bash
# Edit scripts/install.py to use /usr/local/share/switchipy
# Run with sudo
sudo python3 scripts/install.py
```

## Integration with Other Tools

### Desktop Environment
- **XFCE**: Full integration with theme switching
- **GNOME**: Limited functionality (theme detection may vary)
- **KDE**: Limited functionality (theme detection may vary)

### Window Managers
- **i3**: Can be used with i3bar or polybar
- **Openbox**: Works with system tray
- **Awesome**: Can be integrated with awesome widgets

### Automation
- **Cron**: Schedule theme changes
- **Systemd**: Service integration
- **Scripts**: Bash/Python automation
