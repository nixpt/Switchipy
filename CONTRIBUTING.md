# Contributing to Switchipy

Thank you for your interest in contributing to Switchipy! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites
- Python 3.8+
- XFCE desktop environment
- xfconf-query
- zenity
- GTK3 development libraries

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/nixpt/Switchipy.git
   cd Switchipy
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests**
   ```bash
   python -m pytest tests/ -v
   ```

## How to Contribute

### Reporting Issues
- Use the GitHub issue tracker
- Provide detailed information about your system
- Include steps to reproduce the issue

### Submitting Changes
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`python -m pytest tests/ -v`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Style
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Include type hints where appropriate

### Testing
- All new features must include tests
- Maintain or improve test coverage
- Test on different Python versions (3.8+)

## Development Guidelines

### Project Structure
```
switchipy/
├── switchipy/          # Main package
├── tests/              # Test suite
├── docs/               # Documentation
├── examples/           # Example scripts
└── scripts/           # Installation scripts
```

### Key Components
- `themes.py` - Theme detection and switching
- `icons.py` - Icon generation and management
- `hotkey.py` - Global hotkey handling
- `cli.py` - Command-line interface
- `config.py` - Configuration management

## Release Process

1. Update version in `VERSION` file
2. Update `CHANGELOG.md`
3. Create a git tag (`git tag v1.0.1`)
4. Push the tag (`git push origin v1.0.1`)
5. GitHub Actions will automatically create a release

## Questions?

Feel free to open an issue for any questions about contributing!
