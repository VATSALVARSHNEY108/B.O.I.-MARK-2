#!/usr/bin/env python3
"""
BOI (Barely Obeys Instructions) - Main Entry Point
Launches the application with proper module path configuration
"""

import sys
import os

# Get workspace directory
workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, workspace_dir)

def main():
    """Launch BOI application"""
    try:
        from modules.core.gui_app import main as gui_main
        gui_main()
    except Exception as e:
        print(f"❌ Error starting BOI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
