#!/bin/bash
# Hand Gesture Mouse Controller Launcher
# This script ensures the correct Python version and X11 display are configured

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     HAND GESTURE MOUSE CONTROLLER                           ║"
echo "║     Control your mouse with hand gestures via webcam        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Set up X11 display environment
export DISPLAY=${DISPLAY:-:0}
export XAUTHORITY=${XAUTHORITY:-$HOME/.Xauthority}

# Create .Xauthority if it doesn't exist
if [ ! -f "$XAUTHORITY" ]; then
    touch "$XAUTHORITY"
    chmod 600 "$XAUTHORITY"
    echo "Created .Xauthority file"
fi

# Use Python 3.11 explicitly
PYTHON_BIN="/home/runner/workspace/.pythonlibs/bin/python3.11"

# Check if Python 3.11 is available
if [ ! -f "$PYTHON_BIN" ]; then
    echo "Trying default python3.11..."
    PYTHON_BIN="python3.11"
fi

echo "Starting Hand Gesture Controller..."
echo "Python: $PYTHON_BIN"
echo "Display: $DISPLAY"
echo ""

# Run the demo with Python 3.11
exec $PYTHON_BIN demo_hand_gesture_controller.py "$@"
