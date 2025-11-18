#!/usr/bin/env python3
"""
Test Phone Link Dial Feature
Demonstrates calling via Phone Link without Twilio
"""

from modules.communication.phone_dialer import create_phone_dialer
from modules.core.command_executor import CommandExecutor

print("=" * 70)
print("📱 PHONE LINK DIAL FEATURE TEST")
print("=" * 70)

# Create instances
phone_dialer = create_phone_dialer()
executor = CommandExecutor()

print("\n1️⃣  TEST: Open Phone Link App")
print("-" * 70)
result = phone_dialer.open_phone_link()
print(f"✅ Result: {result['message']}")

print("\n2️⃣  TEST: Dial with Phone Link (Direct Method)")
print("-" * 70)
test_number = "+1234567890"
result = phone_dialer.dial_with_phone_link(test_number)
print(f"✅ Result: {result['message']}")
print(f"   Phone: {result.get('phone', 'N/A')}")
print(f"   Method: {result.get('method', 'N/A')}")

print("\n3️⃣  TEST: Dial via Command Executor")
print("-" * 70)
result = executor.execute_command({
    "action": "dial_phone_link",
    "parameters": {
        "phone": "+9876543210"
    }
})
print(f"✅ Result: {result['message']}")

print("\n4️⃣  TEST: Open Phone Link via Command Executor")
print("-" * 70)
result = executor.execute_command({
    "action": "open_phone_link"
})
print(f"✅ Result: {result['message']}")

print("\n" + "=" * 70)
print("✅ ALL TESTS COMPLETE!")
print("=" * 70)

print("\n📋 AVAILABLE COMMANDS:")
print("-" * 70)
print("  Action: 'dial_phone_link' or 'phone_link_dial'")
print("    Parameters: {'phone': '+1234567890'}")
print("    Opens Phone Link and dials the number")
print()
print("  Action: 'open_phone_link'")
print("    Opens the Phone Link app")
print()
print("🎯 HOW IT WORKS:")
print("-" * 70)
print("  • Uses tel: URI protocol")
print("  • Works with Windows Phone Link (Your Phone)")
print("  • No Twilio needed!")
print("  • Automatically opens Phone Link and dials")
print("=" * 70)
