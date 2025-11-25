#!/usr/bin/env python3
"""
Phone Link Call Button Calibration Tool
Helps you find the exact position of the Call button on your screen
"""

import pyautogui
import time
import json
import os

print("=" * 70)
print("📞 PHONE LINK CALL BUTTON CALIBRATION")
print("=" * 70)
print()
print("This tool will help you find the exact position of the")
print("Call button on your screen so auto-calling works perfectly!")
print()
print("=" * 70)
print()

# Step 1: Open Phone Link with a test number
print("STEP 1: Opening Phone Link with test number...")
print()

from modules.communication.phone_dialer import create_phone_dialer

dialer = create_phone_dialer()

# Open Phone Link with a test number (won't actually call)
import webbrowser
webbrowser.open("tel:1234567890")

print("⏳ Waiting 4 seconds for Phone Link to open...")
time.sleep(4)

print()
print("=" * 70)
print("STEP 2: Find the Call Button Position")
print("=" * 70)
print()
print("Instructions:")
print("  1. Look at your Phone Link window")
print("  2. Move your mouse OVER the green Call button")
print("  3. Hold your mouse there for 3 seconds")
print("  4. The tool will capture that position")
print()
print("Starting in 5 seconds...")
print()

for i in range(5, 0, -1):
    print(f"   {i}...")
    time.sleep(1)

print()
print("🖱️  HOVER OVER THE CALL BUTTON NOW!")
print()

# Record mouse positions over 3 seconds
positions = []
for i in range(30):  # 30 samples over 3 seconds
    x, y = pyautogui.position()
    positions.append((x, y))
    print(f"\rPosition: X={x:4d}, Y={y:4d}  [{i+1}/30]", end="")
    time.sleep(0.1)

print()
print()

# Calculate average position
avg_x = sum(p[0] for p in positions) // len(positions)
avg_y = sum(p[1] for p in positions) // len(positions)

print("=" * 70)
print("STEP 3: Verify the Position")
print("=" * 70)
print()
print(f"📍 Detected Call Button Position: X={avg_x}, Y={avg_y}")
print()
print("The mouse will click at this position in 3 seconds.")
print("Watch to see if it clicks the Call button correctly!")
print()

for i in range(3, 0, -1):
    print(f"   Clicking in {i}...")
    time.sleep(1)

# Click the detected position
pyautogui.click(avg_x, avg_y)

print()
print("✅ Click executed!")
print()
print("=" * 70)
print("STEP 4: Save Configuration")
print("=" * 70)
print()

response = input("Did it click the Call button correctly? (yes/no): ").lower()

if response in ['yes', 'y']:
    # Save the position to config
    config = {
        "call_button_x": avg_x,
        "call_button_y": avg_y,
        "screen_width": pyautogui.size()[0],
        "screen_height": pyautogui.size()[1]
    }
    
    config_file = "config/phone_link_button.json"
    os.makedirs("config", exist_ok=True)
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print()
    print("✅ SUCCESS! Configuration saved!")
    print()
    print(f"   Config file: {config_file}")
    print(f"   Button position: ({avg_x}, {avg_y})")
    print()
    print("=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print()
    print("1. The phone_dialer module will now use this exact position")
    print("2. Test it with: python tests/test_phone_link_fix.py")
    print("3. Auto-calling should now work perfectly!")
    print()
else:
    print()
    print("⚠️  Position not accurate. Let's try again!")
    print()
    print("Tips:")
    print("  • Make sure Phone Link window is open")
    print("  • Hover your mouse DIRECTLY over the Call button")
    print("  • Keep your mouse very still during the 3-second capture")
    print("  • Run this script again: python scripts/calibrate_phone_link_button.py")
    print()

print("=" * 70)
print("✅ CALIBRATION COMPLETE")
print("=" * 70)
