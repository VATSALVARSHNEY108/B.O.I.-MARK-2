"""
Test script for WiFi toggle via Quick Settings
This will open Quick Settings and click on WiFi
"""

import sys
import os
import time

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules', 'system'))

from modules.system.quick_settings_controller import QuickSettingsController

print("=" * 60)
print("WIFI TOGGLE TEST - QUICK SETTINGS")
print("=" * 60)
print()
print("⚠️  IMPORTANT: Don't move your mouse during the test.")
print()
print("This test will:")
print("  1. Open Quick Settings panel")
print("  2. Click on WiFi toggle")
print()
print("Starting in 3 seconds...")
time.sleep(3)

try:
    # Initialize controller
    print("1. Initializing QuickSettingsController...")
    controller = QuickSettingsController()
    print(f"   ✓ Screen resolution: {controller.screen_width}x{controller.screen_height}")
    print()
    
    # Test WiFi toggle
    print("2. Opening Quick Settings and toggling WiFi...")
    print()
    
    result = controller.toggle_wifi()
    
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
    print("💡 Did it click the right button?")
    print("   If not, let me know which direction to adjust!")
    
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
