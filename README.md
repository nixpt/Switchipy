# Switchipy - XFCE Theme Switcher

A system tray application for switching between light and dark themes on XFCE with automatic time-based switching and global hotkey support.

## Features

- 🎨 **Theme Detection**: Automatically detects light/dark theme pairs
- ⏰ **Auto-Switch**: Time-based automatic theme switching
- ⌨️ **Global Hotkeys**: Quick theme switching with keyboard shortcuts
- 🖥️ **System Tray**: Clean system tray integration
- 💻 **CLI Interface**: Command-line control for scripting and automation
- ⚙️ **Persistent Config**: Saves settings between sessions
- 🎯 **XFCE Integration**: Native XFCE theme switching

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd LightSwitch

# Install Switchipy
make install
# or
python3 scripts/install.py
```

### Usage

**GUI Application:**
```bash
switchipy
```

**Command Line:**
```bash
switchipy-cli current          # Show current theme
switchipy-cli toggle          # Toggle light/dark
switchipy-cli list            # List available themes
switchipy-cli set Adwaita-dark # Set specific theme
```

## Installation

### Automatic Installation

```bash
make install
```

This will:
- Install to `~/.local/share/switchipy/`
- Create launcher scripts in `~/.local/bin/`
- Set up desktop integration
- Install Python dependencies
- Create initial configuration

### Manual Installation

```bash
# Install system dependencies
make install-deps
# or manually:
sudo pacman -S xfconf zenity  # Arch/Manjaro
sudo apt install xfconf zenity  # Ubuntu/Debian

# Install Python dependencies
pip install --user pynput Pillow

# Run installer
python3 scripts/install.py
```

## Usage

### GUI Application

Launch the system tray application:

```bash
switchipy
```

Features:
- Right-click system tray icon for menu
- Toggle theme with hotkey (Ctrl+Alt+T)
- Auto-switch based on time
- Theme selection from detected pairs

### Command Line Interface

```bash
# Show current theme
switchipy-cli current

# Toggle between light/dark
switchipy-cli toggle

# List available themes
switchipy-cli list

# Set specific theme
switchipy-cli set Adwaita-dark

# Show configuration
switchipy-cli config

# Control auto-switch
switchipy-cli auto on
switchipy-cli interval 19:00 05:00

# Check time status
switchipy-cli time
```

### Configuration

Configuration is stored in `~/.switchipy_config.json`:

```json
{
  "auto_switch_enabled": true,
  "dark_start": "19:00",
  "dark_end": "05:00",
  "hotkey": "<ctrl>+<alt>+t",
  "last_theme": "Adwaita-dark"
}
```

## Development

### Project Structure

```
LightSwitch/
├── app.py                    # Main GUI application
├── switchipy_cli.py         # CLI interface
├── scripts/                  # Installation scripts
│   ├── install.py           # Python installer
│   ├── uninstall.py         # Python uninstaller
│   ├── install.sh           # Shell installer wrapper
│   └── uninstall.sh         # Shell uninstaller wrapper
├── switchipy/               # Core package
│   ├── themes.py            # Theme management
│   ├── config.py            # Configuration
│   ├── icons.py             # Icon generation
│   ├── hotkey.py            # Hotkey functionality
│   ├── autoswitch.py        # Auto-switching
│   ├── utils.py             # Utilities
│   └── cli.py               # CLI implementation
├── tests/                   # Test suite
├── docs/                    # Documentation
└── Makefile                 # Build automation
```

### Development Commands

```bash
make help          # Show all available commands
make install       # Install to system
make uninstall     # Uninstall from system
make test          # Run test suite
make run           # Run GUI application
make cli           # Show CLI help
make clean         # Clean temporary files
make package       # Create distribution package
```

### Testing

```bash
# Run all tests
make test

# Run specific test
python3 -m unittest tests.test_themes

# Run with verbose output
make test-verbose
```

## Documentation

- [API Documentation](docs/API.md) - Complete API reference
- [CLI Documentation](docs/CLI.md) - Command-line interface guide
- [Installation Guide](docs/INSTALLATION.md) - Detailed installation instructions
- [Development Guide](docs/DEVELOPMENT.md) - Contributing and development

## Requirements

- **Operating System**: Linux (XFCE desktop environment)
- **Python**: 3.6 or higher
- **Dependencies**: 
  - `xfconf-query` (XFCE configuration tool)
  - `zenity` (GTK dialog tool)
  - `pynput` (Python package for hotkeys)
  - `Pillow` (Python package for image processing)

## Uninstallation

```bash
make uninstall
# or
python3 scripts/uninstall.py
```

Or manually:
```bash
rm -rf ~/.local/share/switchipy
rm -f ~/.local/bin/switchipy ~/.local/bin/switchipy-cli
rm -f ~/.local/share/applications/switchipy.desktop
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
- Check the [documentation](docs/)
- Run `switchipy-cli --help` for CLI usage
- Check system dependencies with `which xfconf-query zenity`
# Trigger workflow
