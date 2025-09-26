#!/usr/bin/env python3
"""
Switchipy Icon Testing Script

This script demonstrates the enhanced icon functionality
and creates sample icons for testing.
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from switchipy.icons import (
    create_enhanced_icon, create_animated_icon, create_icon_with_fallback,
    get_available_themes, clear_icon_cache, get_icon_info
)

def test_icon_themes():
    """Test different icon themes."""
    print("🎨 Testing Icon Themes")
    print("=" * 30)
    
    themes = get_available_themes()
    modes = ['light', 'dark']
    
    for theme in themes:
        print(f"\n📁 Theme: {theme}")
        for mode in modes:
            try:
                icon_path = create_enhanced_icon(mode, theme, size=64, show_text=True)
                print(f"  ✓ {mode}: {icon_path}")
            except Exception as e:
                print(f"  ✗ {mode}: Error - {e}")

def test_icon_sizes():
    """Test different icon sizes."""
    print("\n📏 Testing Icon Sizes")
    print("=" * 30)
    
    sizes = [32, 48, 64, 96, 128]
    mode = 'light'
    theme = 'modern'
    
    for size in sizes:
        try:
            icon_path = create_enhanced_icon(mode, theme, size=size)
            info = get_icon_info(icon_path)
            print(f"  ✓ {size}x{size}: {icon_path} ({info.get('file_size', 0)} bytes)")
        except Exception as e:
            print(f"  ✗ {size}x{size}: Error - {e}")

def test_animated_icons():
    """Test animated icon creation."""
    print("\n🎬 Testing Animated Icons")
    print("=" * 30)
    
    try:
        frame_paths = create_animated_icon('light', 'default', size=64, frame_count=8)
        print(f"  ✓ Created {len(frame_paths)} animation frames")
        for i, path in enumerate(frame_paths):
            print(f"    Frame {i}: {path}")
    except Exception as e:
        print(f"  ✗ Animation error: {e}")

def test_fallback_icons():
    """Test fallback icon creation."""
    print("\n🔄 Testing Fallback Icons")
    print("=" * 30)
    
    modes = ['light', 'dark']
    
    for mode in modes:
        try:
            icon_path = create_icon_with_fallback(mode, 'default')
            info = get_icon_info(icon_path)
            print(f"  ✓ {mode}: {icon_path} ({info.get('file_size', 0)} bytes)")
        except Exception as e:
            print(f"  ✗ {mode}: Error - {e}")

def create_icon_gallery():
    """Create a gallery of all icon variations."""
    print("\n🖼️ Creating Icon Gallery")
    print("=" * 30)
    
    gallery_dir = Path.home() / 'Pictures' / 'switchipy_icons'
    gallery_dir.mkdir(parents=True, exist_ok=True)
    
    themes = get_available_themes()
    modes = ['light', 'dark']
    sizes = [32, 64, 96]
    
    for theme in themes:
        theme_dir = gallery_dir / theme
        theme_dir.mkdir(exist_ok=True)
        
        for mode in modes:
            mode_dir = theme_dir / mode
            mode_dir.mkdir(exist_ok=True)
            
            for size in sizes:
                try:
                    icon_path = create_enhanced_icon(mode, theme, size=size, show_text=True)
                    
                    # Copy to gallery
                    gallery_icon = mode_dir / f"switchipy_{theme}_{mode}_{size}.png"
                    import shutil
                    shutil.copy2(icon_path, gallery_icon)
                    
                    print(f"  ✓ {theme}/{mode}/{size}: {gallery_icon}")
                except Exception as e:
                    print(f"  ✗ {theme}/{mode}/{size}: Error - {e}")
    
    print(f"\n📁 Gallery created at: {gallery_dir}")

def main():
    """Main testing function."""
    print("🚀 Switchipy Icon Testing")
    print("=" * 50)
    
    # Test icon themes
    test_icon_themes()
    
    # Test different sizes
    test_icon_sizes()
    
    # Test animated icons
    test_animated_icons()
    
    # Test fallback icons
    test_fallback_icons()
    
    # Create icon gallery
    create_icon_gallery()
    
    print("\n✅ Icon testing complete!")
    print("\nTo view the icons:")
    print(f"  ls -la {Path.home() / '.cache' / 'switchipy' / 'icons'}")
    print(f"  ls -la {Path.home() / 'Pictures' / 'switchipy_icons'}")

if __name__ == "__main__":
    main()
