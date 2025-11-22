"""
Test script for Quick Settings automation
This will click on your Quick Settings panel to toggle Bluetooth
"""

import sys
import os
import time

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules', 'system'))

from modules.system.quick_settings_controller import QuickSettingsController

print("=" * 60)
print("QUICK SETTINGS AUTOMATION TEST")
print("=" * 60)
print()
print("⚠️  IMPORTANT: Make sure your Quick Settings panel is accessible!")
print("   Don't move your mouse during the test.")
print()
print("Starting in 3 seconds...")
time.sleep(3)

try:
    # Initialize controller
    print("1. Initializing QuickSettingsController...")
    controller = QuickSettingsController()
    print(f"   ✓ Screen resolution: {controller.screen_width}x{controller.screen_height}")
    print()
    
    # Get info
    print("2. Available toggles:")
    info = controller.get_quick_settings_info()
    for toggle in info['available_toggles']:
        print(f"   - {toggle}")
    print()
    
    # Test Bluetooth toggle
    print("3. Testing Bluetooth toggle...")
    print("   Opening Quick Settings and clicking Bluetooth...")
    print()
    
    result = controller.toggle_bluetooth()
    
    print(f"   Result: {result}")
    print()
    
    if result.get("success"):
        print(f"   ✓ SUCCESS: {result.get('message')}")
    else:
        print(f"   ✗ FAILED: {result.get('error', 'Unknown error')}")
    
    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print()
    print("💡 TIPS:")
    print("   - If the wrong button was clicked, the positions may need adjustment")
    print("   - Check your screen resolution and scaling settings")
    print("   - Make sure Quick Settings is not already open before running")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print()
    print("Make sure you're running this on Windows with PyAutoGUI installed.")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
