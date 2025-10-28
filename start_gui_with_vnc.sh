#!/bin/bash

# Create .Xauthority file if it doesn't exist
touch ~/.Xauthority

# Start Xvfb (virtual framebuffer) if not already running
if ! pgrep -x "Xvfb" > /dev/null; then
    echo "Starting Xvfb..."
    Xvfb :0 -screen 0 1920x1080x24 &
    sleep 2
fi

# Set DISPLAY environment variable
export DISPLAY=:0

# Generate X11 authentication
xauth add $DISPLAY . $(xxd -l 16 -p /dev/urandom)

# Start the GUI application
echo "Starting GUI application..."
python gui_app.py
