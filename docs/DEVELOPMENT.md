# Development Guide

## Development Setup

### Prerequisites

- Python 3.8+
- XFCE desktop environment
- xfconf-query
- zenity
- GTK development libraries

### Installation

```bash
# Clone repository
git clone <repository-url>
cd LightSwitch

# Install system dependencies
# On Arch/Manjaro:
sudo pacman -S python-gobject python-pip xfconf zenity

# On Ubuntu/Debian:
sudo apt install python3-gi python3-pip xfconf zenity

# Install Python dependencies
python3 -m pip install --user --break-system-packages pynput Pillow
```

### Running Tests

```bash
# Run all tests
python3 tests/test_all.py

# Run specific test module
python3 tests/test_themes.py
python3 tests/test_config.py
python3 tests/test_icons.py
python3 tests/test_hotkey.py

# Run with verbose output
python3 -m unittest tests.test_themes -v
```

### Code Style

Follow PEP 8 guidelines:

```bash
# Check code style (if flake8 is available)
python3 -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## Architecture

### Module Structure

```
LightSwitch/
├── app.py              # Main application
├── themes.py           # Theme management
├── config.py           # Configuration
├── icons.py            # Icon generation
├── hotkey.py           # Hotkey handling
├── autoswitch.py       # Auto-switching
├── utils.py            # Utilities
├── tests/              # Test suite
│   ├── test_themes.py
│   ├── test_config.py
│   ├── test_icons.py
│   ├── test_hotkey.py
│   └── test_all.py
└── docs/               # Documentation
    ├── API.md
    └── DEVELOPMENT.md
```

### Design Patterns

- **Separation of Concerns**: Each module handles a specific aspect
- **Dependency Injection**: Functions accept dependencies as parameters
- **Error Handling**: Graceful degradation on failures
- **Optional Dependencies**: Hotkey functionality is optional

### Threading Model

- **Main Thread**: GTK main loop
- **Auto-switch Thread**: Background time checking
- **Hotkey Thread**: Global hotkey listening

## Testing

### Test Categories

1. **Unit Tests**: Individual function testing
2. **Integration Tests**: Module interaction testing
3. **Mock Tests**: External dependency mocking

### Test Structure

```python
class TestModuleName(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        pass
    
    def test_function_name(self):
        """Test description"""
        # Arrange
        # Act
        # Assert
        pass
```

### Mocking External Dependencies

```python
@patch('module.external_dependency')
def test_function(self, mock_dependency):
    mock_dependency.return_value = expected_value
    result = function_under_test()
    self.assertEqual(result, expected_result)
```

## Debugging

### Common Issues

1. **GTK Import Errors**
   - Ensure PyGObject is installed
   - Check GTK version compatibility

2. **Theme Detection Issues**
   - Verify theme directories exist
   - Check theme naming conventions

3. **Hotkey Not Working**
   - Check pynput installation
   - Verify desktop environment support

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit pull request

### Code Review Checklist

- [ ] Code follows PEP 8 style
- [ ] Tests cover new functionality
- [ ] Documentation is updated
- [ ] No breaking changes
- [ ] Error handling is appropriate

## Release Process

### Version Numbering

- **Major**: Breaking changes
- **Minor**: New features
- **Patch**: Bug fixes

### Release Checklist

- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release tag

## Performance Considerations

### Memory Usage

- Icons are cached in `/tmp/`
- Theme maps are generated once
- Threads are daemon threads

### CPU Usage

- Auto-switch checks every 60 seconds
- Hotkey listening is event-driven
- GTK main loop is efficient

### Optimization Tips

- Use `GLib.idle_add()` for UI updates
- Minimize subprocess calls
- Cache theme detection results
