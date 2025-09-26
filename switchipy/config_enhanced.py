"""
Enhanced configuration management for Switchipy.

This module provides:
- Configuration validation with JSON Schema
- Configuration migration system
- Automatic backup creation
- Configuration repair
- User-friendly configuration editor
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from .logging_config import logger

# Configuration schema for validation
CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "auto_switch_enabled": {"type": "boolean"},
        "dark_start": {"type": "string", "pattern": r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"},
        "dark_end": {"type": "string", "pattern": r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"},
        "hotkey": {"type": "string"},
        "last_theme": {"type": "string"},
        "icon_theme": {"type": "string", "enum": ["default", "modern", "minimal"]},
        "icon_size": {"type": "integer", "minimum": 16, "maximum": 256},
        "icon_animated": {"type": "boolean"},
        "log_level": {"type": "string", "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]},
        "notifications": {"type": "boolean"},
        "backup_enabled": {"type": "boolean"},
        "backup_count": {"type": "integer", "minimum": 1, "maximum": 10}
    },
    "required": ["auto_switch_enabled", "dark_start", "dark_end", "hotkey"],
    "additionalProperties": False
}

# Default configuration with all options
DEFAULT_CONFIG = {
    "auto_switch_enabled": False,
    "dark_start": "19:00",
    "dark_end": "05:00",
    "hotkey": "<ctrl>+<alt>+t",
    "last_theme": "",
    "icon_theme": "default",
    "icon_size": 64,
    "icon_animated": False,
    "log_level": "INFO",
    "notifications": True,
    "backup_enabled": True,
    "backup_count": 5
}

# Configuration file paths
CONFIG_PATH = Path.home() / ".switchipy_config.json"
BACKUP_DIR = Path.home() / ".local" / "share" / "switchipy" / "backups"

class ConfigManager:
    """Enhanced configuration manager with validation and backup."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or CONFIG_PATH
        self.backup_dir = BACKUP_DIR
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self._config = None
        self._schema = CONFIG_SCHEMA
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration with validation and repair."""
        try:
            if not self.config_path.exists():
                logger.info("Configuration file not found, creating default")
                return self._create_default_config()
            
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            # Validate configuration
            if not self._validate_config(config):
                logger.warning("Configuration validation failed, attempting repair")
                config = self._repair_config(config)
            
            # Migrate old configuration format
            config = self._migrate_config(config)
            
            # Create backup before saving
            if config.get('backup_enabled', True):
                self._create_backup()
            
            self._config = config
            logger.info("Configuration loaded successfully", config_version=config.get('version', 'unknown'))
            return config
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return self._create_default_config()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration with validation and backup."""
        try:
            # Validate configuration before saving
            if not self._validate_config(config):
                logger.error("Configuration validation failed, not saving")
                return False
            
            # Create backup before saving
            if config.get('backup_enabled', True):
                self._create_backup()
            
            # Add metadata
            config['version'] = '1.0.0'
            config['last_modified'] = datetime.now().isoformat()
            
            # Save configuration
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2, sort_keys=True)
            
            self._config = config
            logger.info("Configuration saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False
    
    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration against schema."""
        try:
            # Basic type checking
            for key, value in config.items():
                if key not in self._schema['properties']:
                    logger.warning(f"Unknown configuration key: {key}")
                    continue
                
                prop_schema = self._schema['properties'][key]
                if not self._validate_property(key, value, prop_schema):
                    return False
            
            # Check required fields
            for required_field in self._schema['required']:
                if required_field not in config:
                    logger.error(f"Missing required field: {required_field}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation error: {e}")
            return False
    
    def _validate_property(self, key: str, value: Any, schema: Dict[str, Any]) -> bool:
        """Validate a single property against its schema."""
        try:
            # Type validation
            if schema.get('type') == 'boolean' and not isinstance(value, bool):
                logger.error(f"Invalid type for {key}: expected boolean, got {type(value)}")
                return False
            
            if schema.get('type') == 'string' and not isinstance(value, str):
                logger.error(f"Invalid type for {key}: expected string, got {type(value)}")
                return False
            
            if schema.get('type') == 'integer' and not isinstance(value, int):
                logger.error(f"Invalid type for {key}: expected integer, got {type(value)}")
                return False
            
            # Pattern validation for strings
            if 'pattern' in schema and isinstance(value, str):
                import re
                if not re.match(schema['pattern'], value):
                    logger.error(f"Invalid format for {key}: {value}")
                    return False
            
            # Enum validation
            if 'enum' in schema and value not in schema['enum']:
                logger.error(f"Invalid value for {key}: {value}, must be one of {schema['enum']}")
                return False
            
            # Range validation
            if 'minimum' in schema and value < schema['minimum']:
                logger.error(f"Value too small for {key}: {value} < {schema['minimum']}")
                return False
            
            if 'maximum' in schema and value > schema['maximum']:
                logger.error(f"Value too large for {key}: {value} > {schema['maximum']}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Property validation error for {key}: {e}")
            return False
    
    def _repair_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Repair invalid configuration by fixing common issues."""
        logger.info("Attempting to repair configuration")
        
        # Fix missing required fields
        for required_field in self._schema['required']:
            if required_field not in config:
                config[required_field] = DEFAULT_CONFIG[required_field]
                logger.info(f"Added missing required field: {required_field}")
        
        # Fix invalid values
        for key, value in config.items():
            if key in DEFAULT_CONFIG:
                default_value = DEFAULT_CONFIG[key]
                if not self._validate_property(key, value, self._schema['properties'][key]):
                    config[key] = default_value
                    logger.info(f"Fixed invalid value for {key}: {value} -> {default_value}")
        
        # Remove unknown fields
        valid_keys = set(self._schema['properties'].keys())
        invalid_keys = [key for key in config.keys() if key not in valid_keys]
        for key in invalid_keys:
            del config[key]
            logger.info(f"Removed unknown field: {key}")
        
        return config
    
    def _migrate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate configuration from older versions."""
        # Add new fields with default values
        for key, default_value in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = default_value
                logger.info(f"Added new configuration field: {key}")
        
        return config
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration."""
        config = DEFAULT_CONFIG.copy()
        self.save_config(config)
        logger.info("Created default configuration")
        return config
    
    def _create_backup(self) -> Optional[Path]:
        """Create backup of current configuration."""
        try:
            if not self.config_path.exists():
                return None
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"config_backup_{timestamp}.json"
            
            shutil.copy2(self.config_path, backup_path)
            logger.debug(f"Configuration backup created: {backup_path}")
            
            # Clean up old backups
            self._cleanup_old_backups()
            
            return backup_path
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None
    
    def _cleanup_old_backups(self):
        """Clean up old backup files."""
        try:
            backup_count = self._config.get('backup_count', 5) if self._config else 5
            backup_files = sorted(self.backup_dir.glob("config_backup_*.json"))
            
            if len(backup_files) > backup_count:
                for old_backup in backup_files[:-backup_count]:
                    old_backup.unlink()
                    logger.debug(f"Removed old backup: {old_backup}")
                    
        except Exception as e:
            logger.error(f"Failed to cleanup old backups: {e}")
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a configuration value with fallback."""
        if self._config is None:
            self._config = self.load_config()
        
        return self._config.get(key, default)
    
    def set_config_value(self, key: str, value: Any) -> bool:
        """Set a configuration value and save."""
        if self._config is None:
            self._config = self.load_config()
        
        self._config[key] = value
        return self.save_config(self._config)
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to defaults."""
        try:
            config = DEFAULT_CONFIG.copy()
            return self.save_config(config)
        except Exception as e:
            logger.error(f"Failed to reset configuration: {e}")
            return False
    
    def get_backup_list(self) -> List[Dict[str, Any]]:
        """Get list of available backups."""
        backups = []
        try:
            for backup_file in sorted(self.backup_dir.glob("config_backup_*.json")):
                stat = backup_file.stat()
                backups.append({
                    'path': backup_file,
                    'name': backup_file.name,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime),
                    'size_mb': round(stat.st_size / (1024 * 1024), 2)
                })
        except Exception as e:
            logger.error(f"Failed to get backup list: {e}")
        
        return backups
    
    def restore_backup(self, backup_path: Path) -> bool:
        """Restore configuration from backup."""
        try:
            if not backup_path.exists():
                logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Create backup of current config
            self._create_backup()
            
            # Restore from backup
            shutil.copy2(backup_path, self.config_path)
            self._config = None  # Force reload
            
            logger.info(f"Configuration restored from backup: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restore backup: {e}")
            return False

# Global configuration manager instance
config_manager = ConfigManager()

# Convenience functions
def load_config() -> Dict[str, Any]:
    """Load configuration with enhanced features."""
    return config_manager.load_config()

def save_config(config: Dict[str, Any]) -> bool:
    """Save configuration with validation."""
    return config_manager.save_config(config)

def get_config_value(key: str, default: Any = None) -> Any:
    """Get a configuration value."""
    return config_manager.get_config_value(key, default)

def set_config_value(key: str, value: Any) -> bool:
    """Set a configuration value."""
    return config_manager.set_config_value(key, value)

def reset_to_defaults() -> bool:
    """Reset configuration to defaults."""
    return config_manager.reset_to_defaults()

def get_backup_list() -> List[Dict[str, Any]]:
    """Get list of configuration backups."""
    return config_manager.get_backup_list()

def restore_backup(backup_path: Path) -> bool:
    """Restore configuration from backup."""
    return config_manager.restore_backup(backup_path)
