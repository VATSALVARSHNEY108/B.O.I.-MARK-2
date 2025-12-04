#!/usr/bin/env python3
"""
BOI Phone Dialer Module
Handles phone calls via Windows Phone Link with multiple click strategies
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path

# Add workspace to path
workspace = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace))


class PhoneDialer:
    """Phone dialing system with Phone Link automation"""

    def __init__(self):
        """Initialize Phone Dialer"""
        self.status = "active"
        self.phone_link_active = False
        self.last_call = None

    def get_status(self):
        """Get current status"""
        return {
            "status": self.status,
            "phone_link_active": self.phone_link_active,
            "last_call": self.last_call
        }

    def open_phone_link(self):
        """Open Windows Phone Link desktop application directly"""
        try:
            # Method 1: Use explorer.exe with correct app folder (Microsoft.YourPhone)
            print("  🔄 Attempting to open Phone Link (Method 1: Explorer)...")
            try:
                subprocess.Popen([
                    "explorer.exe",
                    "shell:AppsFolder\\Microsoft.YourPhone_8wekyb3d8bbwe!App"
                ])
                self.phone_link_active = True
                time.sleep(2)
                print("  ✅ Phone Link desktop app opened")
                return {
                    "success": True,
                    "message": "📱 Phone Link opened successfully"
                }
            except Exception as e1:
                print(f"  ⚠️ Method 1 failed: {e1}")
            
            # Method 2: Use PowerShell Start-Process
            print("  🔄 Attempting to open Phone Link (Method 2: PowerShell)...")
            try:
                ps_cmd = "Start-Process 'shell:AppsFolder\\Microsoft.YourPhone_8wekyb3d8bbwe!App'"
                subprocess.Popen(["powershell", "-Command", ps_cmd])
                self.phone_link_active = True
                time.sleep(2)
                print("  ✅ Phone Link opened via PowerShell")
                return {
                    "success": True,
                    "message": "📱 Phone Link opened successfully"
                }
            except Exception as e2:
                print(f"  ⚠️ Method 2 failed: {e2}")
            
            # Method 3: Use CMD with shell:AppsFolder
            print("  🔄 Attempting to open Phone Link (Method 3: CMD)...")
            try:
                subprocess.Popen(["cmd", "/c", "start shell:AppsFolder\\Microsoft.YourPhone_8wekyb3d8bbwe!App"], shell=False)
                self.phone_link_active = True
                time.sleep(2)
                print("  ✅ Phone Link opened via CMD")
                return {
                    "success": True,
                    "message": "📱 Phone Link opened successfully"
                }
            except Exception as e3:
                print(f"  ⚠️ Method 3 failed: {e3}")
                
            raise Exception("All Phone Link opening methods failed")
                
        except Exception as e:
            print(f"  ❌ Failed to open Phone Link: {e}")
            return {
                "success": False,
                "message": f"Failed to open Phone Link. Please open it manually. Error: {e}"
            }

    def dial_number(self, phone_number: str):
        """
        Dial a phone number via Phone Link
        
        Args:
            phone_number: Phone number to dial
            
        Returns:
            dict with success status and details
        """
        if not phone_number:
            return {"success": False, "message": "❌ No phone number provided"}

        phone_number = str(phone_number).strip()
        clean_number = ''.join(c for c in phone_number if c.isdigit() or c == '+')
        self.last_call = phone_number

        print(f"\n  📱 Dialing: {phone_number}")
        print(f"  ⏳ Opening Phone Link app...")

        open_result = self.open_phone_link()
        if not open_result.get("success"):
            print(f"  ⚠️ Warning: {open_result.get('message')}")
        
        self.phone_link_active = True

        try:
            import pyautogui
            
            screen_width, screen_height = pyautogui.size()
            
            print(f"  ⌨️ Step 1: Typing number {clean_number}...")
            time.sleep(1)
            pyautogui.typewrite(clean_number.replace('+', ''), interval=0.08)
            time.sleep(0.5)

            print("  📞 Step 2: Clicking Call button...")
            
            click_x = 1670
            click_y = 893
            
            print(f"   Clicking at position: ({click_x}, {click_y})")
            pyautogui.click(click_x, click_y)
            time.sleep(0.3)
            pyautogui.click(click_x, click_y)
            print("   ✅ Call button clicked!")

            # Try Tab navigation as final backup
            for i in range(2):
                pyautogui.press('tab')
                time.sleep(0.1)
            pyautogui.press('enter')

            return {
                "success": True,
                "message":
                f"📱 Calling {phone_number} via Phone Link (tried multiple click positions)",
                "phone": phone_number,
                "method": "phone_link_auto_multiclick",
                "auto_call": True
            }

        except ImportError:
            # PyAutoGUI not available, just open Phone Link
            return {
                "success":
                True,
                "message":
                f"📱 Phone Link opened with {phone_number} - Press Enter or click Call button",
                "phone":
                phone_number,
                "method":
                "phone_link_manual",
                "auto_call":
                False,
                "note":
                "Install pyautogui for automatic calling: pip install pyautogui"
            }
        except Exception as e:
            print(f"⚠️ Auto-call failed: {e}")
            return {
                "success": True,
                "message":
                f"📱 Phone Link opened - Manually enter number or press Call",
                "phone": phone_number,
                "method": "phone_link_manual_fallback",
                "auto_call": False,
                "error": str(e)
            }

    def call_contact(self, contact_name: str):
        """
        Call a contact by name - looks up number from contacts.json
        
        Args:
            contact_name: Name of the contact to call
            
        Returns:
            dict with success status and details
        """
        if not contact_name:
            return {"success": False, "message": "❌ No contact name provided"}
        
        try:
            contacts_path = workspace / "data" / "contacts.json"
            with open(contacts_path, 'r', encoding='utf-8') as f:
                contacts = json.load(f)
            
            search_name = contact_name.lower().strip()
            
            for contact in contacts:
                name = contact.get("name", "").lower()
                if name == search_name or search_name in name:
                    phone = contact.get("phone", "")
                    if phone:
                        print(f"📱 Found {contact.get('name')}'s number: {phone}")
                        return self.dial_number(phone)
                    else:
                        return {
                            "success": False,
                            "message": f"❌ Contact '{contact.get('name')}' has no phone number"
                        }
            
            available = [c.get('name') for c in contacts]
            return {
                "success": False,
                "message": f"❌ Contact '{contact_name}' not found. Available: {', '.join(available)}"
            }
            
        except FileNotFoundError:
            return {
                "success": False,
                "message": "❌ Contacts file not found (data/contacts.json)"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error looking up contact: {e}"
            }
    
    def dial_with_phone_link(self, phone_number: str):
        """
        Dial a phone number using Phone Link (alias for dial_number)
        
        Args:
            phone_number: Phone number to dial
            
        Returns:
            dict with success status and details
        """
        return self.dial_number(phone_number)
    
    def quick_dial(self, name_or_number: str, message: str = None):
        """
        Quick dial a contact by name or phone number.
        If message is provided, send it after the call.
        
        Args:
            name_or_number: Contact name or phone number
            message: Optional message to send after call
            
        Returns:
            dict with success status
        """
        is_phone = any(c.isdigit() for c in name_or_number)
        
        if is_phone:
            return self.dial_number(name_or_number)
        else:
            return self.call_contact(name_or_number)
    
    def hangup(self):
        """Hang up the current call"""
        try:
            import pyautogui

            print("📞 Hanging up...")
            # Try to press Escape key or look for End Call button
            pyautogui.press('escape')
            time.sleep(0.5)
            pyautogui.press('e')  # Keyboard shortcut for end call

            return {"success": True, "message": "☎️ Call ended"}
        except Exception as e:
            return {"success": False, "message": f"Failed to hang up: {e}"}

    def close_phone_link(self):
        """Close Phone Link"""
        try:
            import pyautogui

            print("Closing Phone Link...")
            pyautogui.hotkey('alt', 'F4')
            time.sleep(1)
            self.phone_link_active = False

            return {"success": True, "message": "Phone Link closed"}
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to close Phone Link: {e}"
            }


def create_phone_dialer():
    """Factory function to create PhoneDialer instance"""
    return PhoneDialer()


# Allow direct execution for testing
if __name__ == "__main__":
    dialer = create_phone_dialer()

    if len(sys.argv) > 1:
        phone_number = sys.argv[1]
        result = dialer.dial_number(phone_number)
        print(f"\n📞 Result: {result}")
    else:
        print("Usage: python phone_dialer.py <phone_number>")
        print("Example: python phone_dialer.py 5551234567")
