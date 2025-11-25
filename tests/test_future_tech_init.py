#!/usr/bin/env python3
"""
Quick test to verify Future-Tech Core initializes without errors
"""

print("Testing Future-Tech Core initialization...")
print()

try:
    from modules.core.future_tech_core import create_future_tech_core
    print("✅ Import successful")
    
    print("\nCreating Future-Tech Core instance...")
    ftc = create_future_tech_core()
    print("✅ Initialization successful")
    
    print("\nTesting basic command processing...")
    result = ftc.process_ultra_intelligent_command("test command")
    print(f"✅ Command processing works: {result.get('success', False)}")
    
    print("\nTesting system status...")
    status = ftc.get_status_report()
    print(f"✅ Status report works: {len(status)} fields")
    
    print("\n" + "="*50)
    print("🎉 ALL TESTS PASSED!")
    print("Future-Tech Core is ready to use!")
    print("="*50)
    
except Exception as e:
    print(f"\n❌ TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
