"""
Test script for folder opening functionality
"""

from gui_automation import GUIAutomation
from command_executor import CommandExecutor

def test_folder_opening():
    """Test the new folder opening features"""
    
    print("=" * 60)
    print("🧪 TESTING FOLDER OPENING FEATURES")
    print("=" * 60)
    
    gui = GUIAutomation()
    executor = CommandExecutor()
    
    # Test 1: Get desktop path
    print("\n1️⃣ Testing get_desktop_path()...")
    desktop_path = gui.get_desktop_path()
    print(f"   Desktop path: {desktop_path}")
    
    # Test 2: Open Desktop itself
    print("\n2️⃣ Testing open_desktop()...")
    result = executor.execute_single_action("open_desktop", {})
    print(f"   Result: {result['message']}")
    print(f"   Success: {result['success']}")
    
    # Test 3: Open folder by name (search in common locations)
    print("\n3️⃣ Testing open_folder() with folder_name...")
    result = executor.execute_single_action("open_folder", {"folder_name": "Documents"})
    print(f"   Result: {result['message']}")
    print(f"   Success: {result['success']}")
    
    # Test 4: Open folder by full path
    print("\n4️⃣ Testing open_folder() with folder_path...")
    import os
    home = os.path.expanduser("~")
    result = executor.execute_single_action("open_folder", {"folder_path": home})
    print(f"   Result: {result['message']}")
    print(f"   Success: {result['success']}")
    
    # Test 5: Open Desktop folder specifically
    print("\n5️⃣ Testing open_desktop_folder() with no params...")
    result = executor.execute_single_action("open_desktop_folder", {})
    print(f"   Result: {result['message']}")
    print(f"   Success: {result['success']}")
    
    # Test 6: Try to open a folder on Desktop
    print("\n6️⃣ Testing open_desktop_folder() with folder name...")
    result = executor.execute_single_action("open_desktop_folder", {"folder_name": "TestFolder"})
    print(f"   Result: {result['message']}")
    print(f"   Success: {result['success']}")
    
    print("\n" + "=" * 60)
    print("✅ FOLDER OPENING TESTS COMPLETE")
    print("=" * 60)
    
    # Display available actions
    print("\n📋 New Actions Available:")
    print("   • open_folder - Open any folder by path or name")
    print("   • open_desktop_folder - Open folder on Desktop")
    print("   • open_desktop - Open Desktop itself")
    print("\n💡 Example Commands:")
    print('   • "Open my Desktop"')
    print('   • "Open Documents folder"')
    print('   • "Open TestFolder on Desktop"')
    print('   • "Open the Projects folder"')

if __name__ == "__main__":
    test_folder_opening()
