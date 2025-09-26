#!/bin/bash
# Switchipy Autostart Manager - Shell Wrapper

echo "🚀 Switchipy Autostart Manager"
echo "=============================="

# Check if Python script exists
if [ ! -f "scripts/enable_autostart.py" ]; then
    echo "❌ Error: enable_autostart.py not found"
    exit 1
fi

# Run the Python autostart manager
python3 scripts/enable_autostart.py "$@"
