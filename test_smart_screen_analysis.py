#!/usr/bin/env python3
"""
Test script for smart screen analysis feature
"""

from modules.core.gemini_controller import parse_command

def test_smart_analyze_screen():
    """Test that AI can parse smart_analyze_screen commands"""
    
    test_commands = [
        "what is on screen right now",
        "analyze my current screen",
        "what's on my screen",
        "show me what's currently displayed",
        "analyze screen for errors",
        "check my screen for productivity",
    ]
    
    print("🧪 Testing Smart Screen Analysis Feature")
    print("=" * 60)
    
    for cmd in test_commands:
        print(f"\n📝 Command: '{cmd}'")
        result = parse_command(cmd)
        
        if result.get("action") == "smart_analyze_screen":
            print(f"✅ PASS: Correctly identified as smart_analyze_screen")
            print(f"   Focus: {result.get('parameters', {}).get('focus', 'general')}")
        elif result.get("action") == "error":
            print(f"⚠️  ERROR: {result.get('description')}")
        else:
            print(f"❌ FAIL: Got action '{result.get('action')}' instead of smart_analyze_screen")
            print(f"   Full result: {result}")
    
    print("\n" + "=" * 60)
    print("✅ Test complete!")

if __name__ == "__main__":
    test_smart_analyze_screen()
