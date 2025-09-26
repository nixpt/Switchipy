#!/usr/bin/env python3
"""
Switchipy CLI Entry Point

This is a standalone CLI script that can be run directly.
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from switchipy.cli import main

if __name__ == '__main__':
    main()
