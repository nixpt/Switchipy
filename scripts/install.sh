#!/bin/bash
# Switchipy Installation Script

echo "🚀 Switchipy Installation"
echo "=========================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Run the Python installer
python3 scripts/install.py
