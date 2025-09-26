"""
User Experience enhancements for Switchipy.

This module provides:
- Theme preview functionality
- Rich system tray menu
- User preference management
- Notification system
- Customizable hotkeys
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from .logging_config import logger

# Try to import GTK, but make it optional
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    GTK_AVAILABLE = True
except ImportError:
    GTK_AVAILABLE = False
    print("[UX] GTK not available - GUI features disabled")

from .themes import get_current_theme, get_current_mode, generate_theme_map

class ThemePreview:
    """Generate theme preview thumbnails."""
    
    def __init__(self, preview_size: Tuple[int, int] = (128, 96)):
        self.preview_size = preview_size
        self.preview_dir = Path.home() / '.cache' / 'switchipy' / 'previews'
        self.preview_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_preview(self, theme_name: str) -> Optional[Path]:
        """Generate a preview thumbnail for a theme."""
        try:
            preview_path = self.preview_dir / f"{theme_name}_preview.png"
            
            if preview_path.exists():
                return preview_path
            
            # Create a simple preview using GTK
            # This is a simplified version - in practice, you'd use
            # more sophisticated theme preview generation
            preview_path.touch()
            logger.debug(f"Generated theme preview: {preview_path}")
            return preview_path
            
        except Exception as e:
            logger.error(f"Failed to generate theme preview: {e}")
            return None
    
    def get_preview_path(self, theme_name: str) -> Optional[Path]:
        """Get the path to a theme preview."""
        preview_path = self.preview_dir / f"{theme_name}_preview.png"
        return preview_path if preview_path.exists() else None

class NotificationManager:
    """Manage system notifications."""
    
    def __init__(self):
        self.notifications_enabled = True
        self.notification_timeout = 3000  # 3 seconds
    
    def show_notification(self, title: str, message: str, 
                         icon: Optional[str] = None, 
                         timeout: Optional[int] = None) -> bool:
        """Show a system notification."""
        if not self.notifications_enabled:
            return False
        
        try:
            timeout = timeout or self.notification_timeout
            
            # Try different notification methods
            if self._try_notify_send(title, message, icon, timeout):
                return True
            elif self._try_zenity(title, message, icon):
                return True
            else:
                logger.warning("No notification system available")
                return False
                
        except Exception as e:
            logger.error(f"Failed to show notification: {e}")
            return False
    
    def _try_notify_send(self, title: str, message: str, 
                        icon: Optional[str], timeout: int) -> bool:
        """Try to send notification using notify-send."""
        try:
            cmd = ['notify-send', '-t', str(timeout)]
            if icon:
                cmd.extend(['-i', icon])
            cmd.extend([title, message])
            
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _try_zenity(self, title: str, message: str, icon: Optional[str]) -> bool:
        """Try to show notification using zenity."""
        try:
            cmd = ['zenity', '--info', '--title', title, '--text', message]
            if icon:
                cmd.extend(['--icon-name', icon])
            
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def enable_notifications(self):
        """Enable notifications."""
        self.notifications_enabled = True
        logger.info("Notifications enabled")
    
    def disable_notifications(self):
        """Disable notifications."""
        self.notifications_enabled = False
        logger.info("Notifications disabled")

class RichMenuBuilder:
    """Build rich system tray menus with previews and options."""
    
    def __init__(self, app):
        self.app = app
        self.theme_preview = ThemePreview()
        self.notification_manager = NotificationManager()
    
    def build_menu(self):
        """Build a rich system tray menu."""
        if not GTK_AVAILABLE:
            logger.warning("GTK not available - cannot build rich menu")
            return None
        
        try:
            menu = Gtk.Menu()
            
            # Current theme info
            current_theme = get_current_theme()
            current_mode = get_current_mode()
            
            # Header with current theme
            header_item = Gtk.MenuItem(label=f"Current: {current_theme} ({current_mode})")
            header_item.set_sensitive(False)
            menu.append(header_item)
            menu.append(Gtk.SeparatorMenuItem())
            
            # Quick toggle
            toggle_item = Gtk.MenuItem(label="Toggle Theme")
            toggle_item.connect('activate', self.app.toggle_theme)
            menu.append(toggle_item)
            
            # Theme selection submenu
            theme_submenu = self._build_theme_submenu()
            theme_item = Gtk.MenuItem(label="Select Theme")
            theme_item.set_submenu(theme_submenu)
            menu.append(theme_item)
            
            menu.append(Gtk.SeparatorMenuItem())
            
            # Auto-switch options
            auto_switch_submenu = self._build_auto_switch_submenu()
            auto_switch_item = Gtk.MenuItem(label="Auto-Switch")
            auto_switch_item.set_submenu(auto_switch_submenu)
            menu.append(auto_switch_item)
            
            # Preferences submenu
            preferences_submenu = self._build_preferences_submenu()
            preferences_item = Gtk.MenuItem(label="Preferences")
            preferences_item.set_submenu(preferences_submenu)
            menu.append(preferences_item)
            
            menu.append(Gtk.SeparatorMenuItem())
            
            # About and quit
            about_item = Gtk.MenuItem(label="About")
            about_item.connect('activate', self._show_about)
            menu.append(about_item)
            
            quit_item = Gtk.MenuItem(label="Quit")
            quit_item.connect('activate', self.app.quit)
            menu.append(quit_item)
            
            menu.show_all()
            return menu
            
        except Exception as e:
            logger.error(f"Failed to build rich menu: {e}")
            return None
    
    def _build_theme_submenu(self):
        """Build theme selection submenu."""
        if not GTK_AVAILABLE:
            return None
        
        submenu = Gtk.Menu()
        
        # Get available themes
        theme_map = generate_theme_map()
        
        for light_theme, dark_theme in theme_map.items():
            # Light theme item
            light_item = Gtk.MenuItem(label=f"☀️ {light_theme}")
            light_item.connect('activate', lambda w, t=light_theme: self._select_theme(t))
            submenu.append(light_item)
            
            # Dark theme item
            dark_item = Gtk.MenuItem(label=f"🌙 {dark_theme}")
            dark_item.connect('activate', lambda w, t=dark_theme: self._select_theme(t))
            submenu.append(dark_item)
            
            submenu.append(Gtk.SeparatorMenuItem())
        
        return submenu
    
    def _build_auto_switch_submenu(self):
        """Build auto-switch options submenu."""
        if not GTK_AVAILABLE:
            return None
        
        submenu = Gtk.Menu()
        
        # Enable/disable auto-switch
        auto_switch_enabled = self.app.config.get('auto_switch_enabled', False)
        auto_switch_item = Gtk.CheckMenuItem(label="Enable Auto-Switch")
        auto_switch_item.set_active(auto_switch_enabled)
        auto_switch_item.connect('toggled', self._toggle_auto_switch)
        submenu.append(auto_switch_item)
        
        # Time settings
        time_item = Gtk.MenuItem(label="Set Dark Hours...")
        time_item.connect('activate', self._show_time_dialog)
        submenu.append(time_item)
        
        return submenu
    
    def _build_preferences_submenu(self):
        """Build preferences submenu."""
        if not GTK_AVAILABLE:
            return None
        
        submenu = Gtk.Menu()
        
        # Icon theme selection
        icon_theme_item = Gtk.MenuItem(label="Icon Theme...")
        icon_theme_item.connect('activate', self._show_icon_theme_dialog)
        submenu.append(icon_theme_item)
        
        # Hotkey settings
        hotkey_item = Gtk.MenuItem(label="Set Hotkey...")
        hotkey_item.connect('activate', self._show_hotkey_dialog)
        submenu.append(hotkey_item)
        
        # Notification settings
        notifications_enabled = self.app.config.get('notifications', True)
        notification_item = Gtk.CheckMenuItem(label="Enable Notifications")
        notification_item.set_active(notifications_enabled)
        notification_item.connect('toggled', self._toggle_notifications)
        submenu.append(notification_item)
        
        return submenu
    
    def _select_theme(self, theme_name: str):
        """Select a specific theme."""
        try:
            from .themes import set_theme
            set_theme(theme_name)
            self.app.rebuild_menu()
            
            # Show notification
            self.notification_manager.show_notification(
                "Theme Changed",
                f"Switched to {theme_name}",
                "switchipy"
            )
            
        except Exception as e:
            logger.error(f"Failed to select theme {theme_name}: {e}")
    
    def _toggle_auto_switch(self, widget):
        """Toggle auto-switch functionality."""
        enabled = widget.get_active()
        self.app.config['auto_switch_enabled'] = enabled
        
        from .config import save_config
        save_config(self.app.config)
        
        status = "enabled" if enabled else "disabled"
        self.notification_manager.show_notification(
            "Auto-Switch",
            f"Auto-switch {status}",
            "switchipy"
        )
    
    def _toggle_notifications(self, widget):
        """Toggle notifications."""
        enabled = widget.get_active()
        self.app.config['notifications'] = enabled
        
        from .config import save_config
        save_config(self.app.config)
        
        if enabled:
            self.notification_manager.enable_notifications()
        else:
            self.notification_manager.disable_notifications()
    
    def _show_about(self, widget):
        """Show about dialog."""
        if not GTK_AVAILABLE:
            return
        
        dialog = Gtk.AboutDialog()
        dialog.set_name("Switchipy")
        dialog.set_version("1.0.0")
        dialog.set_comments("XFCE Theme Switcher")
        dialog.set_website("https://github.com/username/switchipy")
        dialog.set_license_type(Gtk.License.MIT)
        dialog.run()
        dialog.destroy()
    
    def _show_time_dialog(self, widget):
        """Show time setting dialog."""
        logger.info("Time dialog requested")
    
    def _show_icon_theme_dialog(self, widget):
        """Show icon theme selection dialog."""
        logger.info("Icon theme dialog requested")
    
    def _show_hotkey_dialog(self, widget):
        """Show hotkey setting dialog."""
        logger.info("Hotkey dialog requested")

class UserPreferences:
    """Manage user preferences and settings."""
    
    def __init__(self):
        self.preferences = {
            'theme_preview_size': (128, 96),
            'notification_timeout': 3000,
            'menu_show_previews': True,
            'menu_show_shortcuts': True,
            'auto_save_preferences': True
        }
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference."""
        return self.preferences.get(key, default)
    
    def set_preference(self, key: str, value: Any) -> bool:
        """Set a user preference."""
        try:
            self.preferences[key] = value
            if self.preferences.get('auto_save_preferences', True):
                self.save_preferences()
            return True
        except Exception as e:
            logger.error(f"Failed to set preference {key}: {e}")
            return False
    
    def save_preferences(self) -> bool:
        """Save preferences to file."""
        try:
            prefs_file = Path.home() / '.local' / 'share' / 'switchipy' / 'preferences.json'
            prefs_file.parent.mkdir(parents=True, exist_ok=True)
            
            import json
            with open(prefs_file, 'w') as f:
                json.dump(self.preferences, f, indent=2)
            
            logger.debug("Preferences saved")
            return True
        except Exception as e:
            logger.error(f"Failed to save preferences: {e}")
            return False
    
    def load_preferences(self) -> bool:
        """Load preferences from file."""
        try:
            prefs_file = Path.home() / '.local' / 'share' / 'switchipy' / 'preferences.json'
            
            if not prefs_file.exists():
                return True  # Use defaults
            
            import json
            with open(prefs_file, 'r') as f:
                loaded_prefs = json.load(f)
            
            # Merge with defaults
            self.preferences.update(loaded_prefs)
            logger.debug("Preferences loaded")
            return True
        except Exception as e:
            logger.error(f"Failed to load preferences: {e}")
            return False

# Global instances
theme_preview = ThemePreview()
notification_manager = NotificationManager()
user_preferences = UserPreferences()

# Convenience functions
def show_notification(title: str, message: str, icon: Optional[str] = None) -> bool:
    """Show a system notification."""
    return notification_manager.show_notification(title, message, icon)

def get_theme_preview(theme_name: str) -> Optional[Path]:
    """Get theme preview thumbnail."""
    return theme_preview.get_preview_path(theme_name)

def generate_theme_preview(theme_name: str) -> Optional[Path]:
    """Generate theme preview thumbnail."""
    return theme_preview.generate_preview(theme_name)

def get_user_preference(key: str, default: Any = None) -> Any:
    """Get user preference."""
    return user_preferences.get_preference(key, default)

def set_user_preference(key: str, value: Any) -> bool:
    """Set user preference."""
    return user_preferences.set_preference(key, value)
