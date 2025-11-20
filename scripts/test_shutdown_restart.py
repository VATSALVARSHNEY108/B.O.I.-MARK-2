#!/usr/bin/env python3
"""
Test script for shutdown and restart functionality
This will help diagnose issues without actually shutting down
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.system.system_control import SystemController
import platform

def main():
    print("=" * 60)
    print("SHUTDOWN & RESTART DIAGNOSTIC TEST")
    print("=" * 60)
    print(f"\nOperating System: {platform.system()}")
    print(f"Platform: {platform.platform()}")
    
    controller = SystemController()
    
    print(f"\nDetected OS in controller: {controller.os}")
    
    print("\n" + "=" * 60)
    print("TEST 1: Lock Screen (Safe Test)")
    print("=" * 60)
    result = controller.lock_screen()
    print(f"Result: {result}")
    
    print("\n" + "=" * 60)
    print("TEST 2: Cancel Shutdown/Restart (Safe)")
    print("=" * 60)
    result = controller.cancel_shutdown_restart()
    print(f"Result: {result}")
    
    print("\n" + "=" * 60)
    print("TEST 3: Shutdown with 300 second delay (5 minutes)")
    print("=" * 60)
    print("This gives you time to cancel it...")
    result = controller.shutdown_system(300)
    print(f"Result: {result}")
    
    print("\n" + "=" * 60)
    print("TEST 4: Check if shutdown was scheduled")
    print("=" * 60)
    
    if controller.os == "Windows":
        import subprocess
        check_result = subprocess.run(
            "shutdown /a",
            shell=True,
            capture_output=True,
            text=True
        )
        if check_result.returncode == 0:
            print("✅ Shutdown was scheduled and has been cancelled!")
        else:
            print(f"Result: {check_result.stderr}")
    else:
        print("ℹ️ Cancellation check is Windows-specific")
    
    print("\n" + "=" * 60)
    print("TEST 5: Restart with 300 second delay (5 minutes)")
    print("=" * 60)
    print("This gives you time to cancel it...")
    result = controller.restart_system(300)
    print(f"Result: {result}")
    
    print("\n" + "=" * 60)
    print("TEST 6: Cancel the restart")
    print("=" * 60)
    result = controller.cancel_shutdown_restart()
    print(f"Result: {result}")
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 60)
    print("\nIf you saw error messages above, that's your issue!")
    print("If commands succeeded, shutdown/restart is working correctly.")
    print("\nNOTE: These commands only work on your local computer,")
    print("NOT in cloud environments like Replit.")
    print("=" * 60)

if __name__ == "__main__":
    main()
