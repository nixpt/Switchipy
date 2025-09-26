"""
Performance monitoring and optimization for Switchipy.

This module provides:
- Performance metrics collection
- Memory usage monitoring
- Execution time tracking
- Performance optimization suggestions
- Resource usage reporting
"""

import time
import psutil
import threading
from functools import wraps
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime, timedelta
from .logging_config import logger

class PerformanceMonitor:
    """Monitor and track performance metrics."""
    
    def __init__(self):
        self.metrics = {}
        self.start_time = time.time()
        self.thread = None
        self.monitoring = False
        self.memory_samples = []
        self.cpu_samples = []
        self.max_samples = 100
    
    def start_monitoring(self, interval: float = 5.0):
        """Start background performance monitoring."""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self.thread.start()
        logger.info("Performance monitoring started", interval=interval)
    
    def stop_monitoring(self):
        """Stop background performance monitoring."""
        self.monitoring = False
        if self.thread:
            self.thread.join(timeout=1.0)
        logger.info("Performance monitoring stopped")
    
    def _monitor_loop(self, interval: float):
        """Background monitoring loop."""
        while self.monitoring:
            try:
                # Collect system metrics
                memory_info = psutil.virtual_memory()
                cpu_percent = psutil.cpu_percent()
                
                # Store samples
                self.memory_samples.append({
                    'timestamp': datetime.now(),
                    'used_mb': memory_info.used / (1024 * 1024),
                    'percent': memory_info.percent
                })
                
                self.cpu_samples.append({
                    'timestamp': datetime.now(),
                    'percent': cpu_percent
                })
                
                # Keep only recent samples
                if len(self.memory_samples) > self.max_samples:
                    self.memory_samples = self.memory_samples[-self.max_samples:]
                if len(self.cpu_samples) > self.max_samples:
                    self.cpu_samples = self.cpu_samples[-self.max_samples:]
                
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
                time.sleep(interval)
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage."""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            system_memory = psutil.virtual_memory()
            
            return {
                'process_mb': round(memory_info.rss / (1024 * 1024), 2),
                'process_percent': round(process.memory_percent(), 2),
                'system_used_mb': round(system_memory.used / (1024 * 1024), 2),
                'system_available_mb': round(system_memory.available / (1024 * 1024), 2),
                'system_percent': system_memory.percent
            }
        except Exception as e:
            logger.error(f"Failed to get memory usage: {e}")
            return {}
    
    def get_cpu_usage(self) -> Dict[str, Any]:
        """Get current CPU usage."""
        try:
            process = psutil.Process()
            return {
                'process_percent': process.cpu_percent(),
                'system_percent': psutil.cpu_percent(),
                'cpu_count': psutil.cpu_count()
            }
        except Exception as e:
            logger.error(f"Failed to get CPU usage: {e}")
            return {}
    
    def get_uptime(self) -> Dict[str, Any]:
        """Get application uptime."""
        uptime_seconds = time.time() - self.start_time
        return {
            'uptime_seconds': uptime_seconds,
            'uptime_formatted': str(timedelta(seconds=int(uptime_seconds))),
            'start_time': datetime.fromtimestamp(self.start_time).isoformat()
        }
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        return {
            'memory': self.get_memory_usage(),
            'cpu': self.get_cpu_usage(),
            'uptime': self.get_uptime(),
            'monitoring_active': self.monitoring,
            'samples_collected': len(self.memory_samples)
        }
    
    def get_memory_trend(self) -> Dict[str, Any]:
        """Get memory usage trend over time."""
        if not self.memory_samples:
            return {'trend': 'no_data', 'samples': 0}
        
        recent_samples = self.memory_samples[-10:]  # Last 10 samples
        if len(recent_samples) < 2:
            return {'trend': 'insufficient_data', 'samples': len(recent_samples)}
        
        # Calculate trend
        first_usage = recent_samples[0]['used_mb']
        last_usage = recent_samples[-1]['used_mb']
        trend_direction = 'increasing' if last_usage > first_usage else 'decreasing'
        trend_percent = abs((last_usage - first_usage) / first_usage * 100)
        
        return {
            'trend': trend_direction,
            'trend_percent': round(trend_percent, 2),
            'first_usage_mb': first_usage,
            'last_usage_mb': last_usage,
            'samples': len(recent_samples)
        }
    
    def get_optimization_suggestions(self) -> List[str]:
        """Get performance optimization suggestions."""
        suggestions = []
        
        # Check memory usage
        memory_info = self.get_memory_usage()
        if memory_info.get('process_percent', 0) > 5.0:
            suggestions.append("High memory usage detected - consider optimizing icon caching")
        
        # Check CPU usage
        cpu_info = self.get_cpu_usage()
        if cpu_info.get('process_percent', 0) > 10.0:
            suggestions.append("High CPU usage detected - consider reducing auto-switch frequency")
        
        # Check memory trend
        memory_trend = self.get_memory_trend()
        if memory_trend.get('trend') == 'increasing' and memory_trend.get('trend_percent', 0) > 20:
            suggestions.append("Memory usage is increasing - consider clearing caches")
        
        # Check uptime
        uptime_info = self.get_uptime()
        if uptime_info.get('uptime_seconds', 0) > 86400:  # 24 hours
            suggestions.append("Long uptime detected - consider restarting for optimal performance")
        
        return suggestions

def performance_timer(func_name: Optional[str] = None):
    """Decorator to time function execution."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            name = func_name or func.__name__
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.debug(f"Function {name} executed", 
                           execution_time=round(execution_time, 3))
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"Function {name} failed", 
                           execution_time=round(execution_time, 3), 
                           error=str(e))
                raise
        
        return wrapper
    return decorator

def memory_usage_tracker(func_name: Optional[str] = None):
    """Decorator to track memory usage of functions."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            name = func_name or func.__name__
            
            try:
                # Get memory before
                process = psutil.Process()
                memory_before = process.memory_info().rss / (1024 * 1024)
                
                result = func(*args, **kwargs)
                
                # Get memory after
                memory_after = process.memory_info().rss / (1024 * 1024)
                memory_delta = memory_after - memory_before
                
                logger.debug(f"Function {name} memory usage", 
                           memory_before=round(memory_before, 2),
                           memory_after=round(memory_after, 2),
                           memory_delta=round(memory_delta, 2))
                
                return result
            except Exception as e:
                logger.error(f"Function {name} memory tracking failed", error=str(e))
                raise
        
        return wrapper
    return decorator

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

# Convenience functions
def start_performance_monitoring(interval: float = 5.0):
    """Start performance monitoring."""
    performance_monitor.start_monitoring(interval)

def stop_performance_monitoring():
    """Stop performance monitoring."""
    performance_monitor.stop_monitoring()

def get_performance_summary() -> Dict[str, Any]:
    """Get performance summary."""
    return performance_monitor.get_performance_summary()

def get_optimization_suggestions() -> List[str]:
    """Get optimization suggestions."""
    return performance_monitor.get_optimization_suggestions()

def log_performance_summary():
    """Log current performance summary."""
    summary = get_performance_summary()
    logger.info("Performance summary", **summary)
    
    suggestions = get_optimization_suggestions()
    if suggestions:
        logger.warning("Performance optimization suggestions", suggestions=suggestions)
