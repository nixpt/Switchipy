# Switchipy Icons Documentation

## Overview

The enhanced icons module provides sophisticated icon generation with multiple themes, sizes, animations, and fallback mechanisms. It's designed to be robust, efficient, and highly customizable.

## Features

### 🎨 Multiple Icon Themes
- **Default**: Classic sun/moon design with gold/white colors
- **Modern**: Contemporary design with orange/lavender colors  
- **Minimal**: Clean, simple design with muted colors

### 📏 Multiple Sizes
- Support for 32x32, 48x48, 64x64, 96x96, 128x128 pixels
- Automatic scaling and optimization
- High-DPI support

### 🎬 Animation Support
- Rotating icon animations
- Configurable frame count
- Smooth transitions

### 🔄 Fallback System
- System icon detection
- Minimal fallback icons
- Error handling and recovery

### 💾 Caching System
- Intelligent icon caching
- Cache management utilities
- Performance optimization

## Usage

### Basic Icon Creation

```python
from switchipy.icons import create_enhanced_icon

# Create a light mode icon
icon_path = create_enhanced_icon('light', 'default', size=64)

# Create a dark mode icon with modern theme
icon_path = create_enhanced_icon('dark', 'modern', size=96, show_text=True)
```

### Icon Themes

```python
from switchipy.icons import get_available_themes, create_enhanced_icon

# Get available themes
themes = get_available_themes()
print(themes)  # ['default', 'modern', 'minimal']

# Create icons for each theme
for theme in themes:
    icon_path = create_enhanced_icon('light', theme, size=64)
    print(f"{theme}: {icon_path}")
```

### Animated Icons

```python
from switchipy.icons import create_animated_icon

# Create 8-frame animation
frame_paths = create_animated_icon('light', 'default', size=64, frame_count=8)
print(f"Created {len(frame_paths)} animation frames")
```

### Fallback Icons

```python
from switchipy.icons import create_icon_with_fallback

# Create icon with automatic fallback
icon_path = create_icon_with_fallback('dark', 'modern', size=64)
```

### System Tray Integration

```python
from switchipy.icons import update_icon

# Update system tray icon
update_icon(indicator, 'light', theme='modern', animated=False)
```

## Configuration

### Icon Configuration

```python
ICON_CONFIG = {
    'size': 64,                                    # Default size
    'cache_dir': Path.home() / '.cache' / 'switchipy' / 'icons',
    'tmp_path': '/tmp/switchipy_icon.png',
    'fallback_icon': '/usr/share/pixmaps/switchipy.png'
}
```

### Theme Customization

```python
ICON_THEMES = {
    'custom': {
        'sun_color_light': '#FF6B35',      # Custom sun color
        'sun_color_dark': '#4A4A4A',       # Custom sun color (dark)
        'moon_color_light': '#4A4A4A',     # Custom moon color
        'moon_color_dark': '#E6E6FA',      # Custom moon color (dark)
        'outline_color': '#2C2C2C',        # Custom outline color
        'background': 'transparent'         # Background type
    }
}
```

## Advanced Features

### Icon Information

```python
from switchipy.icons import get_icon_info

# Get detailed icon information
info = get_icon_info('/path/to/icon.png')
print(f"Size: {info['size']}")
print(f"Mode: {info['mode']}")
print(f"Format: {info['format']}")
print(f"File size: {info['file_size']} bytes")
```

### Cache Management

```python
from switchipy.icons import clear_icon_cache

# Clear all cached icons
clear_icon_cache()
```

### Custom Icon Creation

```python
from switchipy.icons import create_sun_icon, create_moon_icon

# Create individual sun and moon icons
sun_icon = create_sun_icon(64, '#FFD700', '#303030')
moon_icon = create_moon_icon(64, '#FFFFFF', '#303030')
```

## Icon Themes

### Default Theme
- **Colors**: Gold sun (#FFD700), White moon (#FFFFFF)
- **Style**: Classic sun/moon design
- **Use case**: General purpose, high contrast

### Modern Theme
- **Colors**: Orange sun (#FFA500), Lavender moon (#E6E6FA)
- **Style**: Contemporary design
- **Use case**: Modern desktop environments

### Minimal Theme
- **Colors**: Muted gold (#FFD700), Light gray (#F0F0F0)
- **Style**: Clean, simple design
- **Use case**: Minimalist interfaces

## Performance Optimization

### Caching Strategy
- Icons are cached by theme, mode, and size
- Automatic cache directory creation
- Efficient file naming convention

### Memory Management
- Lazy loading of icon resources
- Automatic cleanup of temporary files
- Optimized image processing

### Error Handling
- Graceful fallback to system icons
- Minimal fallback icon generation
- Comprehensive error logging

## Testing and Development

### Icon Testing Script

```bash
# Run comprehensive icon tests
python3 examples/test_icons.py
```

### Manual Testing

```python
# Test specific icon creation
from switchipy.icons import create_enhanced_icon

# Test all combinations
themes = ['default', 'modern', 'minimal']
modes = ['light', 'dark']
sizes = [32, 64, 96]

for theme in themes:
    for mode in modes:
        for size in sizes:
            icon_path = create_enhanced_icon(mode, theme, size)
            print(f"Created: {icon_path}")
```

### Icon Gallery

The testing script automatically creates an icon gallery at:
```
~/Pictures/switchipy_icons/
├── default/
│   ├── light/
│   └── dark/
├── modern/
│   ├── light/
│   └── dark/
└── minimal/
    ├── light/
    └── dark/
```

## Troubleshooting

### Common Issues

1. **Icon not displaying:**
   - Check if PIL/Pillow is installed
   - Verify icon file permissions
   - Check system tray icon size requirements

2. **Performance issues:**
   - Clear icon cache: `clear_icon_cache()`
   - Use smaller icon sizes
   - Disable animations

3. **Theme not found:**
   - Use `get_available_themes()` to list themes
   - Check theme configuration
   - Fallback to 'default' theme

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable detailed icon logging
from switchipy.icons import create_enhanced_icon
icon_path = create_enhanced_icon('light', 'default', size=64)
```

## Integration Examples

### System Tray Application

```python
from switchipy.icons import update_icon
from gi.repository import AppIndicator3

# Create indicator
indicator = AppIndicator3.Indicator.new(
    "switchipy", "switchipy", AppIndicator3.IndicatorCategory.APPLICATION_STATUS
)

# Update with enhanced icon
update_icon(indicator, 'light', theme='modern', animated=False)
```

### CLI Integration

```python
from switchipy.icons import create_icon_with_fallback

# Create icon for CLI display
icon_path = create_icon_with_fallback('dark', 'minimal', size=32)
print(f"Icon created: {icon_path}")
```

### Configuration Integration

```python
# Load user preferences
config = load_config()
theme = config.get('icon_theme', 'default')
size = config.get('icon_size', 64)
animated = config.get('icon_animated', False)

# Create icon based on preferences
icon_path = create_enhanced_icon('light', theme, size, animated=animated)
```

## Future Enhancements

### Planned Features
- SVG icon support
- Custom icon uploads
- Icon theme editor
- Real-time icon updates
- Icon animation controls
- High-DPI scaling
- Icon accessibility features

### Contributing
- Add new icon themes
- Improve animation algorithms
- Optimize performance
- Add accessibility features
- Create icon templates
