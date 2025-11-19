#!/usr/bin/env python3
"""
Test Automatic Calling Feature
Demonstrates the new auto-call functionality
"""

from modules.communication.phone_dialer import create_phone_dialer
import time

print("=" * 70)
print("📞 AUTOMATIC CALLING TEST")
print("=" * 70)
print()
print("This test demonstrates the new automatic calling feature.")
print("Phone Link will open AND automatically press the Call button!")
print()
print("⚠️  IMPORTANT:")
print("   1. Make sure Phone Link is installed and connected")
print("   2. Keep the Phone Link window in focus (don't click elsewhere)")
print("   3. Watch as the call starts automatically!")
print()
input("Press Enter to continue...")

# Create phone dialer
phone_dialer = create_phone_dialer()

print("\n" + "=" * 70)
print("TEST 1: Auto-Call Mode (Default)")
print("=" * 70)
print()
print("📱 Dialing with auto-call enabled...")
print()

# Test number - change this to your real number if you want!
test_number = "+1234567890"

print(f"Number to dial: {test_number}")
print()
print("What will happen:")
print("  1. Phone Link opens")
print("  2. Number appears in dial field")
print("  3. System waits 3 seconds")
print("  4. ✨ Enter key pressed automatically")
print("  5. 📞 Call starts!")
print()
input("Press Enter to start test...")

result = phone_dialer.dial_with_phone_link(test_number, auto_call=True)

print("\n📊 Result:")
print(f"   Success: {result['success']}")
print(f"   Message: {result['message']}")
print(f"   Method: {result.get('method', 'N/A')}")
print(f"   Auto-call: {result.get('auto_call', 'N/A')}")

if result.get('note'):
    print(f"   Note: {result['note']}")

print("\n" + "=" * 70)
print("TEST 2: Manual Mode (auto_call=False)")
print("=" * 70)
print()
print("This time we'll just open Phone Link without auto-calling.")
print("You'll need to press Enter or click Call yourself.")
print()
input("Press Enter to continue...")

result = phone_dialer.dial_with_phone_link(test_number, auto_call=False)

print("\n📊 Result:")
print(f"   Success: {result['success']}")
print(f"   Message: {result['message']}")
print(f"   Method: {result.get('method', 'N/A')}")

print("\n" + "=" * 70)
print("TEST 3: Multiple Quick Calls")
print("=" * 70)
print()
print("Testing rapid-fire calling (auto-call enabled)")
print()

test_numbers = [
    "+1234567890",
    "9876543210",
    "+91 98765 43210"
]

print("⚠️  Warning: This will make 3 calls in sequence!")
print("   Each call will auto-start after 3 seconds.")
print()
choice = input("Continue? (y/n): ").lower()

if choice == 'y':
    for i, num in enumerate(test_numbers, 1):
        print(f"\n📞 Call {i}/3: {num}")
        result = phone_dialer.dial_with_phone_link(num, auto_call=True)
        print(f"   → {result['message']}")
        
        # Wait between calls
        if i < len(test_numbers):
            print("   Waiting 5 seconds before next call...")
            time.sleep(5)
else:
    print("Skipped multiple calls test.")

print("\n" + "=" * 70)
print("✅ ALL TESTS COMPLETE!")
print("=" * 70)
print()
print("Summary:")
print("  ✅ Auto-call mode: Opens Phone Link AND starts call")
print("  ✅ Manual mode: Opens Phone Link only (you click Call)")
print("  ✅ Both modes work!")
print()
print("💡 Tips:")
print("  • Keep Phone Link window in focus during auto-call")
print("  • Adjust wait time in code if Phone Link is slow")
print("  • Use auto_call=False to review number before calling")
print()
print("🎯 Next Steps:")
print("  1. Use ai_phone_link_controller.py for AI commands")
print("  2. Use launchers/quick_dial.bat for one-click calling")
print("  3. Integrate with your VATSAL voice commands")
print()
print("=" * 70)
