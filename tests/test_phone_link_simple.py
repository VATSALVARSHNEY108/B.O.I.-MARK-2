#!/usr/bin/env python3
"""
Simple Phone Link Dial Feature Test
"""

from modules.communication.phone_dialer import create_phone_dialer

print("=" * 70)
print("📱 PHONE LINK DIAL FEATURE - Simple Test")
print("=" * 70)

# Create phone dialer
phone_dialer = create_phone_dialer()

print("\n✅ Phone Dialer initialized successfully!")
print(f"   Windows platform: {phone_dialer.is_windows}")

print("\n1️⃣  TEST: Open Phone Link App")
print("-" * 70)
result = phone_dialer.open_phone_link()
print(f"   Success: {result['success']}")
print(f"   Message: {result['message']}")

print("\n2️⃣  TEST: Dial with Phone Link")
print("-" * 70)
test_number = "+1234567890"
result = phone_dialer.dial_with_phone_link(test_number)
print(f"   Success: {result['success']}")
print(f"   Message: {result['message']}")
print(f"   Phone: {result.get('phone', 'N/A')}")
print(f"   Method: {result.get('method', 'N/A')}")

print("\n3️⃣  TEST: Dial with different formats")
print("-" * 70)
test_numbers = [
    "123-456-7890",
    "(123) 456-7890",
    "+91 98765 43210",
    "9876543210"
]

for num in test_numbers:
    result = phone_dialer.dial_with_phone_link(num)
    print(f"   {num:20} → {result['message']}")

print("\n" + "=" * 70)
print("✅ ALL TESTS COMPLETE!")
print("=" * 70)

print("\n📋 HOW TO USE IN YOUR CODE:")
print("-" * 70)
print("""
# Method 1: Direct phone dialer usage
from modules.communication.phone_dialer import create_phone_dialer

phone_dialer = create_phone_dialer()
result = phone_dialer.dial_with_phone_link("+1234567890")

# Method 2: Via Command Executor
executor.execute_command({
    "action": "dial_phone_link",
    "parameters": {
        "phone": "+1234567890"
    }
})

# Method 3: Open Phone Link app
phone_dialer.open_phone_link()
# OR
executor.execute_command({"action": "open_phone_link"})
""")

print("\n🎯 FEATURES:")
print("-" * 70)
print("  ✅ Works without Twilio")
print("  ✅ Uses Windows Phone Link (Your Phone app)")
print("  ✅ Accepts any phone number format")
print("  ✅ Automatically opens Phone Link and dials")
print("  ✅ Uses tel: URI protocol")
print("=" * 70)
