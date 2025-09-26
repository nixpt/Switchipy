#!/bin/bash
# Switchipy Cron Theme Switcher
# 
# This script can be used with cron to automatically switch themes
# based on time of day.

# Configuration
LIGHT_THEME="Adwaita"
DARK_THEME="Adwaita-dark"
DARK_START="19:00"
DARK_END="05:00"

# Get current time in HH:MM format
CURRENT_TIME=$(date +"%H:%M")

# Function to check if current time is within dark hours
is_dark_time() {
    local current_time="$1"
    local dark_start="$2"
    local dark_end="$3"
    
    # Convert times to minutes since midnight for comparison
    current_minutes=$((10#${current_time:0:2} * 60 + 10#${current_time:3:2}))
    start_minutes=$((10#${dark_start:0:2} * 60 + 10#${dark_start:3:2}))
    end_minutes=$((10#${dark_end:0:2} * 60 + 10#${dark_end:3:2}))
    
    if [ $start_minutes -lt $end_minutes ]; then
        # Same day (e.g., 19:00 to 23:59)
        [ $current_minutes -ge $start_minutes ] && [ $current_minutes -lt $end_minutes ]
    else
        # Overnight (e.g., 19:00 to 05:00)
        [ $current_minutes -ge $start_minutes ] || [ $current_minutes -lt $end_minutes ]
    fi
}

# Check if it's dark time and switch theme accordingly
if is_dark_time "$CURRENT_TIME" "$DARK_START" "$DARK_END"; then
    echo "$(date): Switching to dark theme ($DARK_THEME)"
    switchipy-cli set "$DARK_THEME"
else
    echo "$(date): Switching to light theme ($LIGHT_THEME)"
    switchipy-cli set "$LIGHT_THEME"
fi
