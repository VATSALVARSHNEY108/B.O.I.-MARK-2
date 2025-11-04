#!/usr/bin/env python3
"""
Test Volume Control Without nircmd
This script tests the new pycaw-based volume control
"""

from modules.system.system_control import SystemController

def test_volume_control():
    """Test all volume control functions"""
    print("=" * 60)
    print("Testing Volume Control (WITHOUT nircmd)")
    print("=" * 60)
    
    controller = SystemController()
    
    print("\n1. Getting current volume...")
    print(controller.get_volume_info())
    
    print("\n2. Setting volume to 50%...")
    print(controller.set_volume(50))
    
    print("\n3. Getting volume again...")
    print(controller.get_volume_info())
    
    print("\n4. Increasing volume by 10...")
    print(controller.increase_volume(10))
    
    print("\n5. Getting volume...")
    print(controller.get_volume_info())
    
    print("\n6. Decreasing volume by 5...")
    print(controller.decrease_volume(5))
    
    print("\n7. Getting volume...")
    print(controller.get_volume_info())
    
    print("\n8. Testing mute...")
    print(controller.mute_volume())
    
    print("\n9. Testing unmute...")
    print(controller.unmute_volume())
    
    print("\n10. Testing toggle mute...")
    print(controller.toggle_mute())
    
    print("\n11. Testing toggle mute again...")
    print(controller.toggle_mute())
    
    print("\n" + "=" * 60)
    print("✅ Volume control test completed!")
    print("✅ No nircmd.exe required!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_volume_control()
    except Exception as e:
        print(f"\n❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
