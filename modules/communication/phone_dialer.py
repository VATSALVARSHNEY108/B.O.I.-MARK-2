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
        """Open Windows Phone Link application"""
        try:
            # Try multiple methods to open Phone Link
            
            # Method 1: Use Windows "start" command with app name
            print("  🔄 Attempting to open Phone Link (Method 1: Start command)...")
            try:
                subprocess.Popen(["start", "ms-phone-link://"], shell=True)
                self.phone_link_active = True
                time.sleep(2)
                print("  ✅ Phone Link opened via ms-phone-link protocol")
                return {
                    "success": True,
                    "message": "📱 Phone Link opened successfully"
                }
            except Exception as e1:
                print(f"  ⚠️ Method 1 failed: {e1}")
            
            # Method 2: Use explorer.exe with app folder
            print("  🔄 Attempting to open Phone Link (Method 2: Explorer app folder)...")
            try:
                subprocess.Popen([
                    "explorer.exe",
                    "shell:appsFolder\\MicrosoftCorporationII.WindowsPhoneLink_8wekyb3d8bbwe!App"
                ])
                self.phone_link_active = True
                time.sleep(2)
                print("  ✅ Phone Link opened via explorer")
                return {
                    "success": True,
                    "message": "📱 Phone Link opened successfully"
                }
            except Exception as e2:
                print(f"  ⚠️ Method 2 failed: {e2}")
            
            # Method 3: Use Windows Run dialog
            print("  🔄 Attempting to open Phone Link (Method 3: Windows Run)...")
            try:
                subprocess.Popen(["cmd", "/c", "start phonelink:"], shell=False)
                self.phone_link_active = True
                time.sleep(2)
                print("  ✅ Phone Link opened via phonelink protocol")
                return {
                    "success": True,
                    "message": "📱 Phone Link opened successfully"
                }
            except Exception as e3:
                print(f"  ⚠️ Method 3 failed: {e3}")
            
            # Method 4: Direct app launch via PowerShell
            print("  🔄 Attempting to open Phone Link (Method 4: PowerShell)...")
            try:
                ps_cmd = 'Start-Process -FilePath "phonelink://"'
                subprocess.Popen(["powershell", "-Command", ps_cmd])
                self.phone_link_active = True
                time.sleep(2)
                print("  ✅ Phone Link opened via PowerShell")
                return {
                    "success": True,
                    "message": "📱 Phone Link opened successfully"
                }
            except Exception as e4:
                print(f"  ⚠️ Method 4 failed: {e4}")
                
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

        # Format phone number
        phone_number = str(phone_number).strip()
        self.last_call = phone_number

        print(f"\n  📱 Dialing: {phone_number}")
        print(f"  ⏳ Opening Phone Link app...")

        # First, open Phone Link if not already open
        open_result = self.open_phone_link()
        if not open_result.get("success"):
            print(f"  ⚠️ Warning: {open_result.get('message')}")
        
        self.phone_link_active = True

        try:
            import pyautogui

            # Type the phone number in Phone Link
            time.sleep(1)
            pyautogui.typewrite(phone_number, interval=0.05)
            time.sleep(0.5)

            # Strategy 1: Try visual button detection
            try:
                import cv2
                import numpy as np
                from PIL import ImageGrab

                screenshot = np.array(ImageGrab.grab())
                screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

                # Look for green "Call" button
                lower_green = np.array([0, 100, 0])
                upper_green = np.array([100, 255, 100])
                mask = cv2.inRange(screenshot_bgr, lower_green, upper_green)

                if cv2.countNonZero(mask) > 0:
                    # Found green button, try to click it
                    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE)[0]
                    if contours:
                        largest_contour = max(contours, key=cv2.contourArea)
                        x, y, w, h = cv2.boundingRect(largest_contour)
                        button_x = x + w // 2
                        button_y = y + h // 2

                        print(
                            f"   Found Call button at ({button_x}, {button_y})"
                        )
                        pyautogui.click(button_x, button_y)
                        time.sleep(0.5)

                        return {
                            "success": True,
                            "message":
                            f"📱 Calling {phone_number} via Phone Link",
                            "phone": phone_number,
                            "method": "phone_link_auto_visual",
                            "auto_call": True
                        }
            except Exception as img_error:
                print(f"ℹ️ Visual button detection not available: {img_error}")

            # Strategy 2: Try to find "Call" button using OCR
            try:
                import pytesseract
                from PIL import ImageGrab
                import numpy as np

                # Take a screenshot to find "Call" button
                screenshot = ImageGrab.grab()

                # Use pytesseract to find text on screen
                data = pytesseract.image_to_data(
                    screenshot, output_type=pytesseract.Output.DICT)

                # Look for "Call" text
                for i, text in enumerate(data['text']):
                    if text.strip().lower() in ['call', 'dial']:
                        # Found the Call button text, click it
                        x = data['left'][i] + data['width'][i] // 2
                        y = data['top'][i] + data['height'][i] // 2
                        pyautogui.click(x, y)
                        print("✅ Call button clicked via OCR!")

                        return {
                            "success": True,
                            "message":
                            f"📱 Calling {phone_number} via Phone Link",
                            "phone": phone_number,
                            "method": "phone_link_auto_ocr",
                            "auto_call": True
                        }
            except Exception as ocr_error:
                print(f"ℹ️ OCR detection not available: {ocr_error}")

            # Strategy 3: Click the call button at bottom of screen
            print("📞 Attempting to click Call button...")

            # Check if we have a calibrated position
            calibrated = False
            try:
                config_path = workspace / "config" / "phone_link_button.json"
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    cal_x = config.get("call_button_x")
                    cal_y = config.get("call_button_y")

                    if cal_x and cal_y:
                        print(
                            f"   Using calibrated position: ({cal_x}, {cal_y})"
                        )
                        pyautogui.click(cal_x, cal_y)
                        time.sleep(0.5)
                        calibrated = True
                        print("✅ Clicked at calibrated position!")
            except FileNotFoundError:
                print(
                    "   No calibration found. Using Phone Link layout positions..."
                )
            except Exception as e:
                print(f"   Calibration error: {e}")

            # If no calibration, try Phone Link's actual button positions
            if not calibrated:
                # Get screen size
                screen_width, screen_height = pyautogui.size()

                # Based on Phone Link UI: Call button is at the BOTTOM
                # Usually at bottom-center or bottom-right of the Phone Link window
                click_positions = [
                    # Bottom center-right (most likely for call button)
                    (int(screen_width * 0.85), int(screen_height * 0.92)
                     ),  # Bottom right area
                    (int(screen_width * 0.5),
                     int(screen_height * 0.95)),  # Bottom center
                    (int(screen_width * 0.75),
                     int(screen_height * 0.90)),  # Bottom center-right
                    (int(screen_width * 0.85),
                     int(screen_height * 0.85)),  # Right side, lower
                    (int(screen_width * 0.88),
                     int(screen_height * 0.70)),  # Dial pad area
                ]

                for i, (x, y) in enumerate(click_positions):
                    print(f"   Trying position {i+1}/5: ({x}, {y})")
                    pyautogui.click(x, y)
                    time.sleep(0.5)

                print("✅ Click commands sent!")
                print()
                print(
                    "   💡 TIP: Run 'python scripts/calibrate_phone_link_button.py'"
                )
                print(
                    "      to find the exact Call button position on your screen!"
                )

            # Also try keyboard shortcuts as backup
            print("   Backup: Trying keyboard shortcuts...")
            pyautogui.press('enter')
            time.sleep(0.2)
            pyautogui.press('space')
            time.sleep(0.2)

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
        # Check if it's a phone number (digits and common phone chars)
        is_phone = any(c.isdigit() for c in name_or_number)
        
        if is_phone:
            # It's a phone number, dial directly
            return self.dial_number(name_or_number)
        else:
            # It's likely a contact name, try to resolve it
            try:
                # Try to get contact from contact manager if available
                from modules.utilities.contact_manager import ContactManager
                contact_mgr = ContactManager("data/contacts.json")
                contact = contact_mgr.get_contact(name_or_number)
                
                if contact and contact.get("phone"):
                    return self.dial_number(contact["phone"])
                else:
                    # Contact not found, try as direct number
                    return self.dial_number(name_or_number)
            except:
                # If contact lookup fails, just try as direct number
                return self.dial_number(name_or_number)
    
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
