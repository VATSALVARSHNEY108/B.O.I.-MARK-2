#!/usr/bin/env python3
"""
Phone Link Automator - Call Any Contact
Reads mobile number from contacts.json and dials via Phone Link app
Usage: python call_vatsal.py <contact_name>
Example: python call_vatsal.py vatsal
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
CONTACTS_FILE = WORKSPACE / "data" / "contacts.json"
CONFIG_FILE = WORKSPACE / "config" / "phone_link_button.json"


def load_contacts():
    """Load contacts from JSON file"""
    try:
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Contacts file not found at {CONTACTS_FILE}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in contacts file: {e}")
        return []


def find_contact_number(name):
    """Find contact's mobile number from contacts by name"""
    contacts = load_contacts()
    search_name = name.lower().strip()
    
    for contact in contacts:
        contact_name = contact.get("name", "").lower()
        if contact_name == search_name or search_name in contact_name:
            phone = contact.get("phone", "")
            if phone:
                print(f"Found {contact.get('name')}'s number: {phone}")
                return phone, contact.get('name')
    
    print(f"Error: Contact '{name}' not found in contacts.json")
    print("\nAvailable contacts:")
    for contact in contacts:
        print(f"  - {contact.get('name')}: {contact.get('phone', 'No number')}")
    return None, None


def open_phone_link():
    """Open Windows Phone Link desktop application directly"""
    print("Opening Phone Link app...")
    
    methods = [
        (["explorer.exe", "shell:AppsFolder\\Microsoft.YourPhone_8wekyb3d8bbwe!App"], False, "Phone Link desktop app"),
        (["powershell", "-Command", "Start-Process 'shell:AppsFolder\\Microsoft.YourPhone_8wekyb3d8bbwe!App'"], False, "PowerShell"),
        (["cmd", "/c", "start shell:AppsFolder\\Microsoft.YourPhone_8wekyb3d8bbwe!App"], False, "CMD shell"),
    ]
    
    for cmd, use_shell, description in methods:
        try:
            subprocess.Popen(cmd, shell=use_shell)
            print(f"Phone Link opened via {description}")
            time.sleep(3)
            return True
        except Exception as e:
            print(f"Method '{description}' failed: {e}")
            continue
    
    print("Failed to open Phone Link. Please open it manually.")
    return False


def get_calibrated_button_position():
    """Get calibrated call button position from config"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            x = config.get("call_button_x")
            y = config.get("call_button_y")
            if x and y:
                return (x, y)
    except:
        pass
    return None


def dial_number(phone_number):
    """Dial phone number using Phone Link automation"""
    try:
        import pyautogui
        pyautogui.FAILSAFE = True
    except ImportError:
        print("Warning: pyautogui not installed. Cannot automate dialing.")
        print("Install with: pip install pyautogui")
        return False
    
    clean_number = ''.join(c for c in phone_number if c.isdigit() or c == '+')
    
    print(f"Dialing: {clean_number}")
    
    print("Step 1: Typing phone number...")
    pyautogui.typewrite(clean_number.replace('+', ''), interval=0.08)
    time.sleep(0.5)
    
    print("Step 2: Clicking Call button...")
    
    screen_width, screen_height = pyautogui.size()
    click_x = screen_width - 1970
    click_y = 975
    
    print(f"Clicking at position: ({click_x}, {click_y})")
    pyautogui.click(click_x, click_y)
    time.sleep(0.3)
    pyautogui.click(click_x, click_y)
    
    print("Call initiated!")
    return True


def call_contact(contact_name):
    """Main function to call a contact by name"""
    print("=" * 50)
    print(f"  PHONE LINK AUTOMATOR - CALL {contact_name.upper()}")
    print("=" * 50)
    print()
    
    phone_number, actual_name = find_contact_number(contact_name)
    if not phone_number:
        return False
    
    if not open_phone_link():
        print("Please open Phone Link manually and try again.")
        return False
    
    print("Waiting for Phone Link to fully load...")
    time.sleep(2)
    
    if dial_number(phone_number):
        print()
        print("=" * 50)
        print(f"  Calling {actual_name} at {phone_number}")
        print("=" * 50)
        return True
    
    return False


def show_usage():
    """Show usage information"""
    print("=" * 50)
    print("  PHONE LINK AUTOMATOR")
    print("=" * 50)
    print()
    print("Usage: python call_vatsal.py <contact_name>")
    print()
    print("Examples:")
    print("  python call_vatsal.py vatsal")
    print("  python call_vatsal.py mata")
    print("  python call_vatsal.py pita")
    print()
    
    contacts = load_contacts()
    if contacts:
        print("Available contacts:")
        for contact in contacts:
            print(f"  - {contact.get('name')}: {contact.get('phone', 'No number')}")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)
    
    contact_name = " ".join(sys.argv[1:])
    success = call_contact(contact_name)
    sys.exit(0 if success else 1)
