#!/usr/bin/env python3
"""
Test Phone Link with Exact Call Button Coordinates
Uses the calibrated position: X=1670, Y=893
"""

from modules.communication.phone_dialer import create_phone_dialer
import time

print("=" * 70)
print("📞 PHONE LINK - EXACT COORDINATE TEST")
print("=" * 70)
print()
print("Using calibrated call button position:")
print("   X = 1670")
print("   Y = 893")
print()

# Get test number
test_number = input("Enter phone number to test (or press Enter for demo): ").strip()

if not test_number:
    test_number = "+1234567890"
    print(f"Using demo number: {test_number}")

print()
print("⚠️  IMPORTANT:")
print("   • Keep Phone Link window visible")
print("   • Don't click anywhere during the test")
print("   • The call should start automatically!")
print()
input("Press Enter to start the test...")

# Create phone dialer
print()
print("=" * 70)
print("🚀 STARTING AUTO-CALL TEST")
print("=" * 70)
print()

dialer = create_phone_dialer()

# Execute the call
result = dialer.dial_with_phone_link(test_number, auto_call=True)

print()
print("=" * 70)
print("📊 RESULT")
print("=" * 70)
print()
print(f"✅ Success: {result['success']}")
print(f"📱 Phone: {result.get('phone', 'N/A')}")
print(f"🔧 Method: {result.get('method', 'N/A')}")
print(f"💬 Message: {result['message']}")
print()

if result.get('method') == 'phone_link_auto_visual' or 'calibrated' in str(result.get('message', '')).lower():
    print("✅ Used calibrated position (X=1670, Y=893)")
else:
    print("ℹ️  Used fallback positions")

print()
print("=" * 70)
answer = input("Did the call start successfully? (yes/no): ").lower()

if answer in ['yes', 'y']:
    print()
    print("🎉 SUCCESS! Phone Link auto-call is now working!")
    print()
    print("Your call button position is saved in:")
    print("   config/phone_link_button.json")
    print()
else:
    print()
    print("⚠️  If the call didn't start, you can recalibrate:")
    print("   python scripts/calibrate_phone_link_button.py")
    print()
    print("Or manually update the coordinates in:")
    print("   config/phone_link_button.json")
    print()

print("=" * 70)
print("✅ TEST COMPLETE")
print("=" * 70)
