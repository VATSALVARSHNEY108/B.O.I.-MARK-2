#!/usr/bin/env python3
"""
Test Phone Link Auto-Call Fix
Verifies that the Call button is now clicked properly
"""

from modules.communication.phone_dialer import create_phone_dialer
import time

print("=" * 70)
print("📞 PHONE LINK AUTO-CALL FIX - VERIFICATION TEST")
print("=" * 70)
print()
print("This test verifies the improved auto-call functionality.")
print()
print("✨ NEW IMPROVEMENTS:")
print("   1. Longer wait time (4 seconds instead of 3)")
print("   2. Visual button detection (finds green call button)")
print("   3. OCR text detection (finds 'Call' text on screen)")
print("   4. Tab navigation fallback (most reliable method)")
print()
print("⚠️  IMPORTANT:")
print("   • Make sure Phone Link is installed and connected to your phone")
print("   • Keep the Phone Link window visible (don't minimize)")
print("   • The call should start automatically after Phone Link opens")
print()

# Ask for test number
test_number = input("Enter phone number to test (or press Enter for demo): ").strip()

if not test_number:
    test_number = "+1234567890"
    print(f"Using demo number: {test_number}")

print()
input("Press Enter to start the test...")

# Create phone dialer
phone_dialer = create_phone_dialer()

print("\n" + "=" * 70)
print("🚀 STARTING AUTO-CALL TEST")
print("=" * 70)
print()
print(f"📱 Number to dial: {test_number}")
print()
print("Watch carefully:")
print("  1. Phone Link will open")
print("  2. Number will appear in the dial field")
print("  3. System will wait 4 seconds")
print("  4. ✨ One of these will happen:")
print("      • Visual detection finds and clicks Call button")
print("      • OCR finds 'Call' text and clicks it")
print("      • Tab navigation moves to Call button and presses Enter")
print("  5. 📞 Call should start automatically!")
print()
print("Starting in 3 seconds...")
time.sleep(3)

# Execute the call with auto-call enabled
result = phone_dialer.dial_with_phone_link(test_number, auto_call=True)

print("\n" + "=" * 70)
print("📊 TEST RESULTS")
print("=" * 70)
print()
print(f"✅ Success: {result['success']}")
print(f"📱 Phone: {result.get('phone', 'N/A')}")
print(f"🔧 Method Used: {result.get('method', 'N/A')}")
print(f"🤖 Auto-call: {result.get('auto_call', 'N/A')}")
print(f"💬 Message: {result['message']}")

if result.get('note'):
    print(f"📝 Note: {result['note']}")

print()
print("=" * 70)
print("DID THE CALL START?")
print("=" * 70)
print()
answer = input("Did the call start automatically? (yes/no): ").lower()

if answer in ['yes', 'y']:
    print()
    print("✅ SUCCESS! The fix is working correctly!")
    print()
    print("The auto-call feature is now functioning properly.")
    print("Phone Link opened and the Call button was clicked automatically.")
else:
    print()
    print("⚠️  If the call didn't start, please check:")
    print()
    print("   1. Is Phone Link installed and connected to your phone?")
    print("   2. Did Phone Link window open?")
    print("   3. Did you see the number in the dial field?")
    print("   4. Was the Phone Link window in focus (not minimized)?")
    print()
    print("   💡 Troubleshooting tips:")
    print("      • Try increasing wait time in phone_dialer.py (line 403)")
    print("      • Make sure pyautogui is installed: pip install pyautogui")
    print("      • Keep Phone Link window visible during the test")
    print("      • Check if Phone Link requires permissions")
    print()
    print("   📋 Method used: " + result.get('method', 'unknown'))
    print("      • 'phone_link_auto_visual' = Found button visually")
    print("      • 'phone_link_auto_ocr' = Found button via text")
    print("      • 'phone_link_auto_tab' = Used Tab navigation")

print()
print("=" * 70)
print("✅ TEST COMPLETE")
print("=" * 70)
