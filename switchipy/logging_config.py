"""
Logging configuration for Switchipy.

This module provides structured logging with different levels,
log rotation, and user-friendly error messages.
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from datetime import datetime

# Logging configuration
LOG_CONFIG = {
    'level': logging.INFO,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S',
    'max_bytes': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5,
    'log_dir': Path.home() / '.local' / 'share' / 'switchipy' / 'logs'
}

class SwitchipyLogger:
    """Enhanced logger for Switchipy with structured logging."""
    
    def __init__(self, name='switchipy', level=None):
        self.name = name
        self.level = level or LOG_CONFIG['level']
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Set up the logger with file and console handlers."""
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Create log directory
        LOG_CONFIG['log_dir'].mkdir(parents=True, exist_ok=True)
        
        # File handler with rotation
        log_file = LOG_CONFIG['log_dir'] / f'{self.name}.log'
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=LOG_CONFIG['max_bytes'],
            backupCount=LOG_CONFIG['backup_count']
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            LOG_CONFIG['format'],
            datefmt=LOG_CONFIG['date_format']
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def debug(self, message, **kwargs):
        """Log debug message with optional context."""
        self._log_with_context(logging.DEBUG, message, **kwargs)
    
    def info(self, message, **kwargs):
        """Log info message with optional context."""
        self._log_with_context(logging.INFO, message, **kwargs)
    
    def warning(self, message, **kwargs):
        """Log warning message with optional context."""
        self._log_with_context(logging.WARNING, message, **kwargs)
    
    def error(self, message, **kwargs):
        """Log error message with optional context."""
        self._log_with_context(logging.ERROR, message, **kwargs)
    
    def critical(self, message, **kwargs):
        """Log critical message with optional context."""
        self._log_with_context(logging.CRITICAL, message, **kwargs)
    
    def _log_with_context(self, level, message, **kwargs):
        """Log message with additional context."""
        if kwargs:
            context = ' | '.join([f"{k}={v}" for k, v in kwargs.items()])
            message = f"{message} | {context}"
        self.logger.log(level, message)
    
    def set_level(self, level):
        """Set logging level."""
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
    
    def enable_debug(self):
        """Enable debug logging."""
        self.set_level(logging.DEBUG)
        self.info("Debug logging enabled")
    
    def disable_debug(self):
        """Disable debug logging."""
        self.set_level(logging.INFO)
        self.info("Debug logging disabled")

# Global logger instance
logger = SwitchipyLogger()

# Convenience functions
def debug(message, **kwargs):
    """Log debug message."""
    logger.debug(message, **kwargs)

def info(message, **kwargs):
    """Log info message."""
    logger.info(message, **kwargs)

def warning(message, **kwargs):
    """Log warning message."""
    logger.warning(message, **kwargs)

def error(message, **kwargs):
    """Log error message."""
    logger.error(message, **kwargs)

def critical(message, **kwargs):
    """Log critical message."""
    logger.critical(message, **kwargs)

def enable_debug():
    """Enable debug logging."""
    logger.enable_debug()

def disable_debug():
    """Disable debug logging."""
    logger.disable_debug()

def get_log_file():
    """Get the path to the current log file."""
    return LOG_CONFIG['log_dir'] / f'{logger.name}.log'

def clear_logs():
    """Clear all log files."""
    try:
        for log_file in LOG_CONFIG['log_dir'].glob('*.log*'):
            log_file.unlink()
        info("Log files cleared")
    except Exception as e:
        error(f"Failed to clear logs: {e}")

def get_log_stats():
    """Get logging statistics."""
    log_file = get_log_file()
    if log_file.exists():
        size = log_file.stat().st_size
        return {
            'log_file': str(log_file),
            'size_bytes': size,
            'size_mb': round(size / (1024 * 1024), 2),
            'exists': True
        }
    return {
        'log_file': str(log_file),
        'size_bytes': 0,
        'size_mb': 0,
        'exists': False
    }
