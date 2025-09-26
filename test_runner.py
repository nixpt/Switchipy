#!/usr/bin/env python3
"""
Test runner for Switchipy
"""
import sys
import os
import unittest
import subprocess

def run_tests():
    """Run all tests and return exit code"""
    print("🧪 Running Switchipy Test Suite")
    print("=" * 50)
    
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Test modules
    test_modules = [
        'tests.test_themes',
        'tests.test_config', 
        'tests.test_icons',
        'tests.test_hotkey'
    ]
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    for module in test_modules:
        try:
            tests = loader.loadTestsFromName(module)
            suite.addTests(tests)
            print(f"✓ Loaded {module}")
        except Exception as e:
            print(f"✗ Failed to load {module}: {e}")
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"❌ {len(result.failures)} failures, {len(result.errors)} errors")
        return 1

def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    # Check system dependencies
    system_deps = ['xfconf-query', 'zenity']
    for dep in system_deps:
        try:
            subprocess.run(['which', dep], check=True, capture_output=True)
            print(f"✓ {dep} available")
        except subprocess.CalledProcessError:
            print(f"✗ {dep} not found")
    
    # Check Python dependencies
    python_deps = ['gi', 'PIL']
    for dep in python_deps:
        try:
            __import__(dep)
            print(f"✓ {dep} available")
        except ImportError:
            print(f"✗ {dep} not found")
    
    # Check optional dependencies
    try:
        import pynput
        print("✓ pynput available (hotkey support enabled)")
    except ImportError:
        print("⚠ pynput not available (hotkey support disabled)")

if __name__ == '__main__':
    print("Switchipy Test Runner")
    print("=" * 50)
    
    # Check dependencies first
    check_dependencies()
    print()
    
    # Run tests
    exit_code = run_tests()
    sys.exit(exit_code)
