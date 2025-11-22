"""
Test script for Bluetooth control functionality
Run this to diagnose Bluetooth issues
"""

import sys
import os

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules', 'system'))

try:
    from modules.system.windows11_settings_controller import Windows11SettingsController
    
    print("=" * 60)
    print("BLUETOOTH CONTROL TEST")
    print("=" * 60)
    print()
    
    # Initialize controller
    print("1. Initializing Windows11SettingsController...")
    try:
        controller = Windows11SettingsController()
        print("   ✓ Controller initialized successfully")
    except Exception as e:
        print(f"   ✗ Failed to initialize: {e}")
        sys.exit(1)
    
    print()
    print("2. Attempting to turn Bluetooth OFF...")
    print("-" * 60)
    
    # Test turning Bluetooth off
    result = controller.set_bluetooth_state(enabled=False)
    
    print(f"   Result: {result}")
    print()
    
    if result.get("success"):
        print(f"   ✓ SUCCESS: {result.get('message')}")
    else:
        print(f"   ✗ FAILED: {result.get('error', 'Unknown error')}")
        print()
        print("   Detailed error information:")
        for key, value in result.items():
            print(f"     - {key}: {value}")
    
    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print()
    print("Make sure you're running this on Windows with all dependencies installed.")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
