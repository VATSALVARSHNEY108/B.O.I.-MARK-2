#!/usr/bin/env python3
"""
Test script for close all windows functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.system.system_control import SystemController
import platform
import time

def main():
    print("=" * 60)
    print("CLOSE ALL WINDOWS TEST")
    print("=" * 60)
    print(f"\nOperating System: {platform.system()}")
    
    controller = SystemController()
    
    print(f"Detected OS in controller: {controller.os}")
    
    print("\n" + "=" * 60)
    print("WARNING: This will close all open windows!")
    print("=" * 60)
    print("\nThis test will:")
    print("  1. List all currently open windows")
    print("  2. Wait 5 seconds for you to cancel (Ctrl+C)")
    print("  3. Close all windows and tabs")
    print("\nSave your work before continuing!")
    print("\n" + "=" * 60)
    
    try:
        # List open windows first
        print("\nStep 1: Listing open windows...")
        result = controller.list_open_windows()
        print(result)
        
        # Countdown
        print("\nStep 2: Starting countdown...")
        for i in range(5, 0, -1):
            print(f"Closing all windows in {i}... (Press Ctrl+C to cancel)")
            time.sleep(1)
        
        # Close all windows
        print("\nStep 3: Closing all windows...")
        result = controller.close_all_windows()
        print(result)
        
        print("\n" + "=" * 60)
        print("TEST COMPLETE")
        print("=" * 60)
        print("\nAll windows should now be closed.")
        print("Check if browsers and applications were closed successfully.")
        
    except KeyboardInterrupt:
        print("\n\n❌ Test cancelled by user")
        print("No windows were closed.")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")

if __name__ == "__main__":
    main()
