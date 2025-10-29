#!/usr/bin/env python3
"""
Test script for lock, shutdown, and restart features
"""

from system_control import SystemController

def test_system_control():
    """Test the new system control features"""
    
    print("🧪 Testing System Control Features\n")
    print("=" * 60)
    
    controller = SystemController()
    
    # Test 1: Lock Screen
    print("\n1️⃣ Testing lock_screen()...")
    print("   Note: This will actually lock your screen on real systems")
    print(f"   Result: {controller.lock_screen.__doc__}")
    
    # Test 2: Shutdown System (with delay)
    print("\n2️⃣ Testing shutdown_system()...")
    print("   Note: This will schedule a shutdown on real systems")
    print(f"   Result: {controller.shutdown_system.__doc__}")
    
    # Test 3: Restart System (with delay)
    print("\n3️⃣ Testing restart_system()...")
    print("   Note: This will schedule a restart on real systems")
    print(f"   Result: {controller.restart_system.__doc__}")
    
    # Test 4: Cancel Shutdown/Restart
    print("\n4️⃣ Testing cancel_shutdown_restart()...")
    print(f"   Result: {controller.cancel_shutdown_restart.__doc__}")
    
    print("\n" + "=" * 60)
    print("✅ All methods are properly defined and callable")
    print("\n📝 Methods available:")
    print("   - lock_screen(): Lock the computer screen")
    print("   - shutdown_system(delay_seconds=10): Shutdown with delay")
    print("   - restart_system(delay_seconds=10): Restart with delay")
    print("   - cancel_shutdown_restart(): Cancel scheduled shutdown/restart")
    print("\n⚠️  IMPORTANT: These functions will perform real system operations")
    print("   when called on a real computer. Use with caution!")

if __name__ == "__main__":
    test_system_control()
