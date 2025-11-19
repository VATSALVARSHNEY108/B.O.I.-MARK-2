#!/usr/bin/env python3
"""
Demo: AI Phone Link Controller
Shows all the ways to use AI-powered phone control
"""

from ai_phone_link_controller import AIPhoneLinkController
import time

print("=" * 70)
print("🤖 AI PHONE LINK CONTROLLER - DEMO")
print("=" * 70)
print()

# Initialize controller
controller = AIPhoneLinkController()

print("✅ Controller initialized!")
print(f"   AI Engine: {'Active ✓' if controller.ai_enabled else 'Basic mode (no API key)'}")
print(f"   Phone Link: {'Available ✓' if controller.phone_dialer.is_windows else 'Windows only'}")
print()

# Demo 1: Natural language commands
print("\n" + "=" * 70)
print("DEMO 1: Natural Language Commands (With AI)")
print("=" * 70)

demo_commands = [
    "Call +1234567890",
    "Dial my friend at 9876543210",
    "Open Phone Link",
]

for cmd in demo_commands:
    print(f"\n💬 Command: '{cmd}'")
    result = controller.process_command(cmd)
    print(f"📱 Result: {result['message']}")
    time.sleep(1)

# Demo 2: Quick dial (no AI parsing)
print("\n" + "=" * 70)
print("DEMO 2: Quick Dial (Direct, No AI)")
print("=" * 70)

print("\n📞 Quick dialing +1234567890...")
result = controller.quick_dial("+1234567890")
print(f"✅ {result['message']}")

# Demo 3: Command history
print("\n" + "=" * 70)
print("DEMO 3: Command History")
print("=" * 70)

history = controller.get_history(limit=5)
print(f"\n📜 Recent {len(history)} commands:")
for i, entry in enumerate(history, 1):
    print(f"\n{i}. {entry['input']}")
    print(f"   Action: {entry['command'].get('action', 'unknown')}")
    print(f"   Time: {entry['timestamp']}")

# Demo 4: Integration example
print("\n" + "=" * 70)
print("DEMO 4: Integration Example")
print("=" * 70)

print("""
# How to integrate with your code:

from ai_phone_link_controller import AIPhoneLinkController

controller = AIPhoneLinkController()

# Method 1: Natural language
result = controller.process_command("Call mom at +1234567890")

# Method 2: Quick dial
result = controller.quick_dial("+1234567890")

# Method 3: Open Phone Link
result = controller.phone_dialer.open_phone_link()

# Method 4: Via command executor (existing VATSAL method)
result = controller.executor.execute_command({
    "action": "dial_phone_link",
    "parameters": {"phone": "+1234567890"}
})
""")

# Demo 5: Batch file examples
print("\n" + "=" * 70)
print("DEMO 5: Batch File Launchers")
print("=" * 70)

print("""
✅ Available batch files in 'launchers/' folder:

1. ai_phone_controller.bat
   → Interactive AI mode with chat interface
   Usage: Double-click the file

2. quick_dial.bat
   → One-click dial your favorite number
   Usage: Edit number in file, then double-click

3. ai_phone_with_number.bat
   → Dial any number with AI
   Usage: Double-click and enter number when prompted
   Or: ai_phone_with_number.bat "+1234567890"

4. ai_phone_controller.ps1
   → PowerShell version (alternative)
   Usage: Right-click → Run with PowerShell
""")

print("\n" + "=" * 70)
print("✅ DEMO COMPLETE!")
print("=" * 70)
print()
print("📚 For more info, read: AI_PHONE_LINK_CONTROLLER_GUIDE.md")
print()
print("🚀 Try interactive mode:")
print("   python ai_phone_link_controller.py")
print()
print("=" * 70)
