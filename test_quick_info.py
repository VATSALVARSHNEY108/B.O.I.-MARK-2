#!/usr/bin/env python3
"""
Test Quick Info Feature
Tests the new weather/date/time commands
"""

import sys
import os
from pathlib import Path

# Add modules to path
workspace_dir = Path(__file__).parent
modules_dir = workspace_dir / 'modules'
sys.path.insert(0, str(workspace_dir))
sys.path.insert(0, str(modules_dir))
sys.path.insert(0, str(modules_dir / 'core'))

from modules.core.gemini_controller import parse_command
from modules.core.command_executor import CommandExecutor

def test_quick_info():
    """Test quick info commands"""
    print("=" * 70)
    print("TESTING QUICK INFO FEATURE")
    print("=" * 70)
    
    # Initialize executor
    print("\n✅ Initializing CommandExecutor...")
    executor = CommandExecutor()
    print("✅ CommandExecutor initialized successfully!")
    
    # Test cases
    test_commands = [
        "what time is it",
        "what's the date today",
        "what day is it",
        "tell me the weather",
        "get weather for London"
    ]
    
    print("\n" + "=" * 70)
    print("TESTING COMMAND PARSING")
    print("=" * 70)
    
    for user_input in test_commands:
        print(f"\n📝 User: \"{user_input}\"")
        print("-" * 70)
        
        try:
            # Parse command
            command_dict = parse_command(user_input)
            action = command_dict.get("action", "")
            parameters = command_dict.get("parameters", {})
            
            print(f"✅ Parsed Action: {action}")
            print(f"   Parameters: {parameters}")
            
            # Check if it's a quick info action (not search_web)
            if action in ["get_time", "get_date", "get_day_info", "get_quick_weather", "get_forecast"]:
                print(f"✅ CORRECT: Using quick info action (NOT web search)")
            elif action == "search_web":
                print(f"⚠️  WARNING: Using search_web instead of quick info")
            
            # Execute command
            print(f"\n🔄 Executing command...")
            result = executor.execute(command_dict)
            
            if result["success"]:
                print(f"\n✅ SUCCESS!")
                print(result["message"])
            else:
                print(f"\n❌ FAILED: {result['message']}")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "=" * 70)
    
    print("\n🎉 Test Complete!")

if __name__ == "__main__":
    # Check if API key is set (needed for parse_command)
    if not os.environ.get("GEMINI_API_KEY"):
        print("⚠️  WARNING: GEMINI_API_KEY not set")
        print("   Command parsing will fail, but we can test QuickInfo directly")
        print()
        
        # Direct test of QuickInfo
        from modules.utilities.quick_info import create_quick_info
        quick_info = create_quick_info()
        
        print("=" * 70)
        print("DIRECT QUICK INFO TESTS (No API key needed)")
        print("=" * 70)
        
        print("\n📅 Testing get_current_time():")
        print(quick_info.get_current_time())
        
        print("\n📅 Testing get_current_date():")
        print(quick_info.get_current_date())
        
        print("\n📅 Testing get_day_info():")
        print(quick_info.get_day_info())
        
        print("\n✅ Direct tests passed!")
    else:
        test_quick_info()
