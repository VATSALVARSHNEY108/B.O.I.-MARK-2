#!/usr/bin/env python3
"""
Phone Link Automator - Call Vatsal
Reads Vatsal's mobile number from contacts.json and dials via Phone Link app
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


def find_vatsal_number():
    """Find Vatsal's mobile number from contacts"""
    contacts = load_contacts()
    
    for contact in contacts:
        name = contact.get("name", "").lower()
        if name == "vatsal":
            phone = contact.get("phone", "")
            if phone:
                print(f"Found Vatsal's number: {phone}")
                return phone
    
    print("Error: Vatsal's contact not found in contacts.json")
    return None


def open_phone_link():
    """Open Windows Phone Link application"""
    print("Opening Phone Link app...")
    
    methods = [
        (["start", "ms-phone-link://"], True, "ms-phone-link protocol"),
        (["explorer.exe", "shell:appsFolder\\MicrosoftCorporationII.WindowsPhoneLink_8wekyb3d8bbwe!App"], False, "Explorer app folder"),
        (["cmd", "/c", "start phonelink:"], False, "phonelink protocol"),
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
    
    time.sleep(1)
    
    pyautogui.typewrite(clean_number.replace('+', ''), interval=0.05)
    time.sleep(0.5)
    
    calibrated_pos = get_calibrated_button_position()
    
    if calibrated_pos:
        x, y = calibrated_pos
        print(f"Using calibrated position: ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(0.5)
    else:
        screen_width, screen_height = pyautogui.size()
        
        click_positions = [
            (int(screen_width * 0.85), int(screen_height * 0.92)),
            (int(screen_width * 0.5), int(screen_height * 0.95)),
            (int(screen_width * 0.75), int(screen_height * 0.90)),
            (int(screen_width * 0.85), int(screen_height * 0.85)),
        ]
        
        for i, (x, y) in enumerate(click_positions):
            print(f"Trying click position {i+1}: ({x}, {y})")
            pyautogui.click(x, y)
            time.sleep(0.3)
    
    pyautogui.press('enter')
    time.sleep(0.2)
    pyautogui.press('space')
    
    print("Call initiated!")
    return True


def call_vatsal():
    """Main function to call Vatsal"""
    print("=" * 50)
    print("  PHONE LINK AUTOMATOR - CALL VATSAL")
    print("=" * 50)
    print()
    
    phone_number = find_vatsal_number()
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
        print(f"  Calling Vatsal at {phone_number}")
        print("=" * 50)
        return True
    
    return False


if __name__ == "__main__":
    success = call_vatsal()
    sys.exit(0 if success else 1)
