#!/usr/bin/env python3
"""
VATSAL AI Desktop Automation - GUI Launcher
Launch the main GUI application with all features
"""

import sys
import os

# Add the modules directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

def main():
    """Launch the VATSAL AI GUI Application"""
    try:
        print("🚀 Starting VATSAL AI Desktop Automation GUI...")
        print("=" * 60)
        
        # Import and run the GUI app
        from core.gui_app import main as gui_main
        
        gui_main()
        
    except ImportError as e:
        print(f"❌ Error: Could not import GUI app - {e}")
        print("\nMake sure all dependencies are installed:")
        print("  • google-genai")
        print("  • pyautogui")
        print("  • psutil")
        print("  • pyperclip")
        print("  • python-dotenv")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
