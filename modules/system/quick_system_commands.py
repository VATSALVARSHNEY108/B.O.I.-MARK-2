"""
Quick System Commands - Direct execution without API calls
Use this for instant system control without relying on Gemini API
"""

import sys
from system_control import SystemController

def main():
    controller = SystemController()
    
    if len(sys.argv) < 2:
        print("\n🎮 QUICK SYSTEM COMMANDS")
        print("=" * 60)
        print("Usage: python quick_system_commands.py <command> [value]")
        print("\nSystem Control:")
        print("  lock           - Lock screen")
        print("  shutdown       - Shutdown computer (10 sec delay)")
        print("  shutdown-now   - Shutdown immediately")
        print("  restart        - Restart computer (10 sec delay)")
        print("  restart-now    - Restart immediately")
        print("  cancel         - Cancel shutdown/restart")
        print("\nVolume Control:")
        print("  vol-set <0-100>    - Set volume to specific level")
        print("  vol-up [amount]    - Increase volume (default 10)")
        print("  vol-down [amount]  - Decrease volume (default 10)")
        print("  vol-mute           - Toggle mute")
        print("  vol-get            - Get current volume")
        print("  vol-menu           - Open interactive menu (Windows)")
        print("\nBrightness Control:")
        print("  bright-set <0-100> - Set brightness to specific level")
        print("\nExamples:")
        print("  python quick_system_commands.py lock")
        print("  python quick_system_commands.py vol-set 80")
        print("  python quick_system_commands.py vol-up 5")
        print("  python quick_system_commands.py bright-set 75")
        return
    
    command = sys.argv[1].lower()
    
    if command == "lock":
        print(controller.lock_screen())
    
    elif command == "shutdown":
        print(controller.shutdown_system(10))
    
    elif command == "shutdown-now":
        print(controller.shutdown_system(0))
    
    elif command == "restart":
        print(controller.restart_system(10))
    
    elif command == "restart-now":
        print(controller.restart_system(0))
    
    elif command == "cancel":
        print(controller.cancel_shutdown_restart())
    
    # Volume commands
    elif command == "vol-set":
        if len(sys.argv) < 3:
            print("❌ Please specify volume level (0-100)")
        else:
            level = int(sys.argv[2])
            print(controller.set_volume(level))
    
    elif command == "vol-up":
        amount = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        print(controller.increase_volume(amount))
    
    elif command == "vol-down":
        amount = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        print(controller.decrease_volume(amount))
    
    elif command == "vol-mute":
        print(controller.toggle_mute())
    
    elif command == "vol-get":
        print(controller.get_volume_info())
    
    elif command == "vol-menu":
        print(controller.open_volume_brightness_menu())
    
    # Brightness commands
    elif command == "bright-set":
        if len(sys.argv) < 3:
            print("❌ Please specify brightness level (0-100)")
        else:
            level = int(sys.argv[2])
            print(controller.set_brightness(level))
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run without arguments to see available commands")

if __name__ == "__main__":
    main()
