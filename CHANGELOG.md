# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-09-25

### Added
- Initial release of Switchipy
- System tray application for XFCE theme switching
- Automatic theme detection for light/dark pairs
- Time-based automatic theme switching
- Global hotkey support (Ctrl+Alt+S)
- Command-line interface for scripting and automation
- Persistent configuration with JSON storage
- Comprehensive test suite
- Complete documentation
- Installation and uninstallation scripts
- Desktop integration with application menu
- Icon generation for system tray
- Support for multiple theme variants (hdpi, xhdpi, solid)
- Configuration management with validation
- Auto-switching with configurable time intervals
- CLI commands for all functionality
- Makefile for build automation
- Package structure with proper entry points

### Features
- **Theme Management**: Automatic detection of light/dark theme pairs
- **Auto-Switch**: Configurable time-based theme switching
- **Global Hotkeys**: Quick theme toggling with keyboard shortcuts
- **System Tray**: Clean integration with system tray
- **CLI Interface**: Full command-line control for automation
- **Configuration**: Persistent settings with JSON storage
- **XFCE Integration**: Native XFCE theme switching support
- **Documentation**: Comprehensive user and developer documentation
- **Testing**: Complete test suite with coverage
- **Installation**: Easy installation and uninstallation

### Technical Details
- Python 3.6+ compatibility
- GTK 3.0 integration
- XFCE configuration management
- Thread-safe hotkey handling
- Modular package structure
- Comprehensive error handling
- Cross-distribution Linux support

## [Unreleased]

### Planned
- GNOME support
- KDE support
- Wayland compatibility
- Theme preview functionality
- Advanced scheduling options
- Plugin system
- Remote theme switching
- Theme backup and restore
