#!/usr/bin/env python3
"""
Volume & Brightness Controller
Standalone utility for controlling system volume and brightness
Works cross-platform (Windows, macOS, Linux)
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.system.system_control import SystemController


def print_help():
    """Display help information"""
    print("\n🎛️ VOLUME & BRIGHTNESS CONTROLLER")
    print("=" * 70)
    print("Usage: python volume_brightness_controller.py <category> <command> [value]")
    print("\n📢 VOLUME COMMANDS:")
    print("  volume set <0-100>    - Set volume to specific percentage")
    print("  volume up [amount]    - Increase volume (default 10)")
    print("  volume down [amount]  - Decrease volume (default 10)")
    print("  volume mute           - Toggle mute/unmute")
    print("  volume get            - Show current volume level")
    print("  volume menu           - Open interactive menu (Windows only)")
    print("\n🔆 BRIGHTNESS COMMANDS:")
    print("  brightness set <0-100>  - Set brightness to specific percentage")
    print("  brightness up [amount]  - Increase brightness (default 10)")
    print("  brightness down [amount]- Decrease brightness (default 10)")
    print("  brightness get          - Show current brightness level")
    print("\n💡 EXAMPLES:")
    print("  python volume_brightness_controller.py volume set 80")
    print("  python volume_brightness_controller.py volume up 5")
    print("  python volume_brightness_controller.py volume mute")
    print("  python volume_brightness_controller.py brightness set 50")
    print("  python volume_brightness_controller.py brightness down 20")
    print("  python volume_brightness_controller.py volume menu")
    print()


def main():
    """Main entry point"""
    controller = SystemController()
    
    # Check if enough arguments
    if len(sys.argv) < 3:
        print_help()
        return
    
    category = sys.argv[1].lower()
    command = sys.argv[2].lower()
    
    # VOLUME COMMANDS
    if category == "volume" or category == "vol":
        if command == "set":
            if len(sys.argv) < 4:
                print("❌ Error: Please specify volume level (0-100)")
                print("Example: python volume_brightness_controller.py volume set 80")
                return
            try:
                level = int(sys.argv[3])
                print(controller.set_volume(level))
            except ValueError:
                print("❌ Error: Volume level must be a number (0-100)")
        
        elif command == "up":
            amount = 10
            if len(sys.argv) > 3:
                try:
                    amount = int(sys.argv[3])
                except ValueError:
                    print("⚠️ Warning: Invalid amount, using default (10)")
            print(controller.increase_volume(amount))
        
        elif command == "down":
            amount = 10
            if len(sys.argv) > 3:
                try:
                    amount = int(sys.argv[3])
                except ValueError:
                    print("⚠️ Warning: Invalid amount, using default (10)")
            print(controller.decrease_volume(amount))
        
        elif command == "mute":
            print(controller.toggle_mute())
        
        elif command == "get":
            print(controller.get_volume_info())
        
        elif command == "menu":
            print(controller.open_volume_brightness_menu())
        
        else:
            print(f"❌ Unknown volume command: {command}")
            print("Run without arguments to see available commands")
    
    # BRIGHTNESS COMMANDS
    elif category == "brightness" or category == "bright":
        if command == "set":
            if len(sys.argv) < 4:
                print("❌ Error: Please specify brightness level (0-100)")
                print("Example: python volume_brightness_controller.py brightness set 75")
                return
            try:
                level = int(sys.argv[3])
                print(controller.set_brightness(level))
            except ValueError:
                print("❌ Error: Brightness level must be a number (0-100)")
        
        elif command == "up":
            amount = 10
            if len(sys.argv) > 3:
                try:
                    amount = int(sys.argv[3])
                except ValueError:
                    print("⚠️ Warning: Invalid amount, using default (10)")
            print(controller.increase_brightness(amount))
        
        elif command == "down":
            amount = 10
            if len(sys.argv) > 3:
                try:
                    amount = int(sys.argv[3])
                except ValueError:
                    print("⚠️ Warning: Invalid amount, using default (10)")
            print(controller.decrease_brightness(amount))
        
        elif command == "get":
            level = controller.get_brightness()
            if level is not None:
                print(f"🔆 Current Brightness: {level}%")
            else:
                print("ℹ️ Unable to retrieve brightness level")
        
        else:
            print(f"❌ Unknown brightness command: {command}")
            print("Run without arguments to see available commands")
    
    else:
        print(f"❌ Unknown category: {category}")
        print("Available categories: volume, brightness")
        print("Run without arguments to see help")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Run without arguments for help")
