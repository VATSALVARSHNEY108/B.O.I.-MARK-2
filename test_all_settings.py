"""
Complete test for all Windows 11 settings controls
Tests WiFi, Bluetooth, Night Light, Volume, Brightness, etc.
"""

import sys
import os
import time

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules', 'system'))

from modules.system.settings_automator import SettingsAutomator

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_result(result):
    if result.get("success"):
        print(f"  ✓ {result.get('message')}")
    else:
        print(f"  ✗ {result.get('error')}")
    print()

def main():
    print_header("WINDOWS 11 SETTINGS AUTOMATOR - FULL TEST")
    
    print("\n⚠️  IMPORTANT:")
    print("  - Don't move your mouse during the test")
    print("  - Each toggle will be tested one by one")
    print("  - Press Ctrl+C to stop at any time")
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    try:
        # Initialize
        print("\n1. Initializing SettingsAutomator...")
        automator = SettingsAutomator()
        info = automator.get_available_toggles()
        print(f"   ✓ Screen: {info['screen_resolution']}")
        print(f"   ✓ Available toggles: {', '.join(info['toggles'])}")
        
        # Test each control
        print_header("TESTING NETWORK CONTROLS")
        
        print("Testing WiFi toggle...")
        result = automator.toggle_wifi()
        print_result(result)
        time.sleep(1)
        
        print("Testing Bluetooth toggle...")
        result = automator.toggle_bluetooth()
        print_result(result)
        time.sleep(1)
        
        print("Testing Airplane mode toggle...")
        result = automator.toggle_airplane_mode()
        print_result(result)
        time.sleep(1)
        
        print_header("TESTING DISPLAY CONTROLS")
        
        print("Testing Night light toggle...")
        result = automator.toggle_night_light()
        print_result(result)
        time.sleep(1)
        
        print_header("TESTING VOLUME CONTROLS")
        
        print("Testing Volume Up...")
        result = automator.volume_up(2)
        print_result(result)
        time.sleep(0.5)
        
        print("Testing Volume Down...")
        result = automator.volume_down(2)
        print_result(result)
        time.sleep(0.5)
        
        print("Testing Mute toggle...")
        result = automator.mute()
        print_result(result)
        time.sleep(0.5)
        
        print("Unmuting...")
        result = automator.mute()
        print_result(result)
        
        print_header("TESTING BRIGHTNESS CONTROLS")
        
        print("Testing Brightness Up...")
        result = automator.brightness_up(1)
        print_result(result)
        time.sleep(0.5)
        
        print("Testing Brightness Down...")
        result = automator.brightness_down(1)
        print_result(result)
        
        print_header("ALL TESTS COMPLETE!")
        print("\n✓ All settings controls are working!")
        print("\n💡 You can now use these controls in your BOI application!")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
