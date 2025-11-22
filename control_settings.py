"""
Simple command-line interface to control Windows 11 settings
Usage: python control_settings.py <command>

Commands:
  wifi              - Toggle WiFi
  bluetooth         - Toggle Bluetooth
  airplane          - Toggle Airplane mode
  nightlight        - Toggle Night light
  hotspot           - Toggle Mobile hotspot
  volume up         - Increase volume
  volume down       - Decrease volume
  mute              - Toggle mute
  brightness up     - Increase brightness
  brightness down   - Decrease brightness
"""

import sys
import os

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules', 'system'))

from modules.system.settings_automator import SettingsAutomator

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = ' '.join(sys.argv[1:]).lower()
    
    automator = SettingsAutomator()
    
    # Map commands to functions
    commands = {
        'wifi': automator.toggle_wifi,
        'bluetooth': automator.toggle_bluetooth,
        'airplane': automator.toggle_airplane_mode,
        'nightlight': automator.toggle_night_light,
        'night light': automator.toggle_night_light,
        'hotspot': automator.toggle_mobile_hotspot,
        'mobile hotspot': automator.toggle_mobile_hotspot,
        'volume up': automator.volume_up,
        'volume down': automator.volume_down,
        'mute': automator.mute,
        'brightness up': automator.brightness_up,
        'brightness down': automator.brightness_down,
    }
    
    if command in commands:
        print(f"Executing: {command}...")
        result = commands[command]()
        
        if result.get('success'):
            print(f"✓ {result.get('message')}")
        else:
            print(f"✗ {result.get('error')}")
    else:
        print(f"Unknown command: {command}")
        print("\nAvailable commands:")
        print("  wifi, bluetooth, airplane, nightlight, hotspot")
        print("  volume up, volume down, mute")
        print("  brightness up, brightness down")
        sys.exit(1)

if __name__ == "__main__":
    main()
