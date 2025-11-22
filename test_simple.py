"""Simple test to debug"""
import sys
import os

print("Script started!")

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules', 'system'))

print("Paths added!")

try:
    from modules.system.quick_settings_controller import QuickSettingsController
    print("Import successful!")
    
    controller = QuickSettingsController()
    print(f"Controller created! Screen: {controller.screen_width}x{controller.screen_height}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("Script finished!")
