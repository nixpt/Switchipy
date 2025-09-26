"""
Enhanced Icon generation and management module for Switchipy.

This module handles:
- Creating theme mode icons (light/dark) with multiple styles
- Updating system tray icons with animations
- Icon caching and optimization
- Multiple icon themes and sizes
- Error handling and fallbacks
"""

import os
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from gi.repository import GLib

# Icon configuration
ICON_CONFIG = {
    'size': 64,
    'cache_dir': Path.home() / '.cache' / 'switchipy' / 'icons',
    'tmp_path': '/tmp/switchipy_icon.png',
    'fallback_icon': '/usr/share/pixmaps/switchipy.png'
}

# Legacy constant for backward compatibility
ICON_PATH = "/tmp/switchipy_icon.png"

# Icon themes and styles
ICON_THEMES = {
    'default': {
        'sun_color_light': '#FFD700',
        'sun_color_dark': '#606060',
        'moon_color_light': '#606060',
        'moon_color_dark': '#FFFFFF',
        'outline_color': '#303030',
        'background': 'transparent'
    },
    'modern': {
        'sun_color_light': '#FFA500',
        'sun_color_dark': '#4A4A4A',
        'moon_color_light': '#4A4A4A',
        'moon_color_dark': '#E6E6FA',
        'outline_color': '#2C2C2C',
        'background': 'transparent'
    },
    'minimal': {
        'sun_color_light': '#FFD700',
        'sun_color_dark': '#808080',
        'moon_color_light': '#808080',
        'moon_color_dark': '#F0F0F0',
        'outline_color': '#404040',
        'background': 'transparent'
    }
}

def ensure_cache_dir():
    """Ensure the icon cache directory exists."""
    ICON_CONFIG['cache_dir'].mkdir(parents=True, exist_ok=True)

def get_icon_path(mode, theme='default', size=None):
    """
    Get the path for a cached icon.
    
    Args:
        mode (str): "light" or "dark"
        theme (str): Icon theme name
        size (int): Icon size (defaults to config size)
        
    Returns:
        Path: Path to the cached icon file
    """
    if size is None:
        size = ICON_CONFIG['size']
    
    cache_dir = ICON_CONFIG['cache_dir']
    return cache_dir / f"switchipy_{theme}_{mode}_{size}.png"

def create_sun_icon(size, color, outline_color, x_offset=0, y_offset=0):
    """
    Create a sun icon with rays.
    
    Args:
        size (int): Icon size
        color (str): Sun color
        outline_color (str): Outline color
        x_offset (int): X position offset
        y_offset (int): Y position offset
        
    Returns:
        Image: Sun icon
    """
    sun_size = size // 3
    sun_x = (size // 4) + x_offset
    sun_y = (size // 4) + y_offset
    
    # Create sun image
    sun_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sun_dc = ImageDraw.Draw(sun_img)
    
    # Draw sun rays
    ray_length = sun_size // 2
    center_x, center_y = sun_x + sun_size // 2, sun_y + sun_size // 2
    
    for angle in range(0, 360, 30):
        import math
        rad = math.radians(angle)
        end_x = center_x + ray_length * math.cos(rad)
        end_y = center_y + ray_length * math.sin(rad)
        sun_dc.line([(center_x, center_y), (end_x, end_y)], fill=color, width=2)
    
    # Draw sun circle
    sun_dc.ellipse((sun_x, sun_y, sun_x + sun_size, sun_y + sun_size), 
                   fill=color, outline=outline_color, width=2)
    
    return sun_img

def create_moon_icon(size, color, outline_color, x_offset=0, y_offset=0):
    """
    Create a moon icon with crescent shape.
    
    Args:
        size (int): Icon size
        color (str): Moon color
        outline_color (str): Outline color
        x_offset (int): X position offset
        y_offset (int): Y position offset
        
    Returns:
        Image: Moon icon
    """
    moon_size = size // 3
    moon_x = (size // 2) + x_offset
    moon_y = (size // 4) + y_offset
    
    # Create moon image
    moon_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    moon_dc = ImageDraw.Draw(moon_img)
    
    # Draw moon crescent
    moon_dc.ellipse((moon_x, moon_y, moon_x + moon_size, moon_y + moon_size), 
                    fill=color, outline=outline_color, width=2)
    
    # Create crescent effect
    crescent_x = moon_x + moon_size // 3
    moon_dc.ellipse((crescent_x, moon_y, crescent_x + moon_size, moon_y + moon_size), 
                    fill=(0, 0, 0, 0), outline=outline_color, width=2)
    
    return moon_img

def create_enhanced_icon(mode, theme='default', size=None, show_text=False):
    """
    Create an enhanced system tray icon.
    
    Args:
        mode (str): "light" or "dark" - determines icon appearance
        theme (str): Icon theme name
        size (int): Icon size
        show_text (bool): Whether to show mode text
        
    Returns:
        str: Path to the created icon file
    """
    if size is None:
        size = ICON_CONFIG['size']
    
    # Get theme colors
    theme_colors = ICON_THEMES.get(theme, ICON_THEMES['default'])
    
    # Create base image
    if theme_colors['background'] == 'transparent':
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    else:
        image = Image.new("RGBA", (size, size), theme_colors['background'])
    
    dc = ImageDraw.Draw(image)
    
    # Determine colors based on mode
    if mode == "light":
        sun_color = theme_colors['sun_color_light']
        moon_color = theme_colors['moon_color_light']
        active_color = sun_color
    else:  # dark mode
        sun_color = theme_colors['sun_color_dark']
        moon_color = theme_colors['moon_color_dark']
        active_color = moon_color
    
    outline_color = theme_colors['outline_color']
    
    # Create sun and moon icons
    sun_icon = create_sun_icon(size, sun_color, outline_color)
    moon_icon = create_moon_icon(size, moon_color, outline_color)
    
    # Composite icons onto base image
    image = Image.alpha_composite(image, sun_icon)
    image = Image.alpha_composite(image, moon_icon)
    
    # Add visual indicator for active mode
    indicator_size = size // 8
    indicator_x = size - indicator_size - 4
    indicator_y = size - indicator_size - 4
    
    dc.ellipse((indicator_x, indicator_y, indicator_x + indicator_size, indicator_y + indicator_size),
               fill=active_color, outline=outline_color, width=1)
    
    # Add text if requested
    if show_text:
        try:
            # Try to use a system font
            font_size = size // 8
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        if font:
            text = mode.upper()
            text_bbox = dc.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            text_x = (size - text_width) // 2
            text_y = size - text_height - 4
            
            # Draw text with outline
            dc.text((text_x-1, text_y-1), text, font=font, fill=outline_color)
            dc.text((text_x+1, text_y+1), text, font=font, fill=outline_color)
            dc.text((text_x, text_y), text, font=font, fill=active_color)
    
    # Save the icon
    ensure_cache_dir()
    icon_path = get_icon_path(mode, theme, size)
    image.save(icon_path)
    
    # Also save to temp path for immediate use
    image.save(ICON_CONFIG['tmp_path'])
    
    return str(icon_path)

def create_animated_icon(mode, theme='default', size=None, frame_count=8):
    """
    Create an animated icon with rotation effect.
    
    Args:
        mode (str): "light" or "dark"
        theme (str): Icon theme name
        size (int): Icon size
        frame_count (int): Number of animation frames
        
    Returns:
        list: List of icon file paths
    """
    if size is None:
        size = ICON_CONFIG['size']
    
    ensure_cache_dir()
    frame_paths = []
    
    for frame in range(frame_count):
        # Calculate rotation angle
        angle = (360 / frame_count) * frame
        
        # Create base icon
        base_icon = create_enhanced_icon(mode, theme, size, show_text=False)
        
        # Load and rotate the icon
        with Image.open(base_icon) as img:
            rotated = img.rotate(angle, expand=False)
            
            # Save frame
            frame_path = ICON_CONFIG['cache_dir'] / f"switchipy_{theme}_{mode}_{size}_frame_{frame}.png"
            rotated.save(frame_path)
            frame_paths.append(str(frame_path))
    
    return frame_paths

def get_system_icon(mode):
    """
    Try to get a system icon for the theme mode.
    
    Args:
        mode (str): "light" or "dark"
        
    Returns:
        str: Path to system icon or None
    """
    # Common system icon paths
    system_icons = [
        f"/usr/share/pixmaps/switchipy-{mode}.png",
        f"/usr/share/icons/hicolor/64x64/apps/switchipy-{mode}.png",
        f"/usr/share/icons/Adwaita/64x64/apps/switchipy-{mode}.png",
        f"/usr/share/icons/gnome/64x64/apps/switchipy-{mode}.png"
    ]
    
    for icon_path in system_icons:
        if os.path.exists(icon_path):
            return icon_path
    
    return None

def create_icon_with_fallback(mode, theme='default', size=None):
    """
    Create an icon with system fallback.
    
    Args:
        mode (str): "light" or "dark"
        theme (str): Icon theme name
        size (int): Icon size
        
    Returns:
        str: Path to the created icon file
    """
    # Try to get system icon first
    system_icon = get_system_icon(mode)
    if system_icon:
        return system_icon
    
    # Create custom icon
    try:
        return create_enhanced_icon(mode, theme, size)
    except Exception as e:
        print(f"[Icons] Error creating icon: {e}")
        
        # Try fallback icon
        if os.path.exists(ICON_CONFIG['fallback_icon']):
            return ICON_CONFIG['fallback_icon']
        
        # Create minimal fallback
        return create_minimal_icon(mode, size)

def create_minimal_icon(mode, size=None):
    """
    Create a minimal fallback icon.
    
    Args:
        mode (str): "light" or "dark"
        size (int): Icon size
        
    Returns:
        str: Path to the created icon file
    """
    if size is None:
        size = ICON_CONFIG['size']
    
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)
    
    # Simple circle with mode indicator
    color = "#FFD700" if mode == "light" else "#FFFFFF"
    dc.ellipse((size//4, size//4, 3*size//4, 3*size//4), 
               fill=color, outline="#000000", width=2)
    
    # Save minimal icon
    ensure_cache_dir()
    icon_path = ICON_CONFIG['cache_dir'] / f"switchipy_minimal_{mode}_{size}.png"
    image.save(icon_path)
    
    return str(icon_path)

def update_icon(indicator, mode, theme='default', animated=False):
    """
    Update the system tray icon with enhanced features.
    
    Args:
        indicator: GTK AppIndicator object
        mode (str): "light" or "dark" - determines icon appearance
        theme (str): Icon theme name
        animated (bool): Whether to use animated icon
    """
    try:
        if animated:
            # Create animated icon frames
            frame_paths = create_animated_icon(mode, theme)
            # Use first frame for now (could be enhanced with actual animation)
            icon_path = frame_paths[0] if frame_paths else create_icon_with_fallback(mode, theme)
        else:
            # Create static icon
            icon_path = create_icon_with_fallback(mode, theme)
        
        # Update the system tray icon using GTK's idle_add for thread safety
        GLib.idle_add(indicator.set_icon, icon_path)
        
    except Exception as e:
        print(f"[Icons] Error updating icon: {e}")
        # Fallback to minimal icon
        try:
            fallback_path = create_minimal_icon(mode)
            GLib.idle_add(indicator.set_icon, fallback_path)
        except Exception as fallback_error:
            print(f"[Icons] Fallback icon creation failed: {fallback_error}")

def clear_icon_cache():
    """Clear the icon cache directory."""
    try:
        import shutil
        if ICON_CONFIG['cache_dir'].exists():
            shutil.rmtree(ICON_CONFIG['cache_dir'])
        print("[Icons] Cache cleared")
    except Exception as e:
        print(f"[Icons] Error clearing cache: {e}")

def get_available_themes():
    """Get list of available icon themes."""
    return list(ICON_THEMES.keys())

def get_icon_info(icon_path):
    """
    Get information about an icon file.
    
    Args:
        icon_path (str): Path to icon file
        
    Returns:
        dict: Icon information
    """
    try:
        with Image.open(icon_path) as img:
            return {
                'size': img.size,
                'mode': img.mode,
                'format': img.format,
                'file_size': os.path.getsize(icon_path)
            }
    except Exception as e:
        return {'error': str(e)}

# Legacy function for backward compatibility

def create_icon(mode: str):
    """
    Create enhanced high-contrast icons for the system tray.
    
    Args:
        mode (str): "light" or "dark" - determines icon appearance
        
    Returns:
        str: Path to the created icon file
    """
    size = 64
    image = Image.new("RGBA", (size, size), (0,0,0,0))
    dc = ImageDraw.Draw(image)
    
    if mode == "light":
        # Enhanced sun with rays
        sun_color = "#FFD700"
        outline_color = "#B8860B"
        
        # Draw sun rays (8 rays)
        center_x, center_y = 32, 32
        ray_length = 20
        for angle in range(0, 360, 45):
            import math
            rad = math.radians(angle)
            end_x = center_x + ray_length * math.cos(rad)
            end_y = center_y + ray_length * math.sin(rad)
            dc.line([(center_x, center_y), (end_x, end_y)], fill=sun_color, width=3)
        
        # Draw sun circle
        dc.ellipse((16, 16, 48, 48), fill=sun_color, outline=outline_color, width=2)
        
    else:
        # Enhanced moon with better crescent
        moon_color = "#E6E6FA"
        outline_color = "#C0C0C0"
        
        # Draw main moon circle
        dc.ellipse((16, 16, 48, 48), fill=moon_color, outline=outline_color, width=2)
        
        # Create crescent effect with better positioning
        crescent_x = 20
        dc.ellipse((crescent_x, 16, crescent_x + 32, 48), fill=(0, 0, 0, 0), outline=outline_color, width=2)

    image.save(ICON_PATH)
    return ICON_PATH
