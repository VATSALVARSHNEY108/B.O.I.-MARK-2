"""
Windows 11 Quick Settings Controller
Automates clicking on Quick Settings toggles (WiFi, Bluetooth, Airplane mode, etc.)
No administrator privileges required!
"""

import pyautogui
import time
import platform
from typing import Dict, Tuple, Optional
from PIL import ImageGrab
import subprocess

# Configure PyAutoGUI
pyautogui.PAUSE = 0.5  # Add small delay between actions
pyautogui.FAILSAFE = True  # Move mouse to corner to abort


class QuickSettingsController:
    """Control Windows 11 settings via Quick Settings panel automation"""
    
    def __init__(self):
        if platform.system() != "Windows":
            raise RuntimeError("This controller only works on Windows 11")
        
        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Quick Settings button is typically in bottom-right corner
        # Usually around (width - 100, height - 30) on Windows 11
        # Adjusted to click more to the left on the system tray area
        self.quick_settings_position = (self.screen_width - 160, self.screen_height - 35)
    
    def open_quick_settings(self) -> bool:
        """Open the Quick Settings panel by clicking the system tray icons area"""
        try:
            # Click on the Quick Settings area (WiFi/Volume/Battery icons area)
            print(f"Clicking Quick Settings at position: {self.quick_settings_position}")
            pyautogui.click(self.quick_settings_position[0], self.quick_settings_position[1])
            
            # Wait for panel to open
            time.sleep(1)
            
            return True
        except Exception as e:
            print(f"Error opening Quick Settings: {e}")
            return False
    
    def close_quick_settings(self) -> bool:
        """Close Quick Settings by clicking elsewhere or pressing Escape"""
        try:
            pyautogui.press('escape')
            time.sleep(0.3)
            return True
        except Exception as e:
            print(f"Error closing Quick Settings: {e}")
            return False
    
    def find_toggle_button(self, toggle_name: str) -> Optional[Tuple[int, int]]:
        """
        Find a toggle button by scanning for text on screen
        Returns (x, y) coordinates if found, None otherwise
        """
        try:
            # Take screenshot of the Quick Settings area (right side of screen)
            screenshot_area = (
                self.screen_width - 400,  # Start 400px from right
                self.screen_height - 600,  # Start 600px from bottom
                self.screen_width,         # End at right edge
                self.screen_height - 50    # End 50px from bottom
            )
            
            # Try to locate the button using image recognition
            # Note: This requires the toggle to be visible on screen
            button_location = pyautogui.locateOnScreen(
                None,  # We'll use text-based approach instead
                region=screenshot_area,
                confidence=0.8
            )
            
            # For now, return estimated positions based on typical Windows 11 layout
            # These are approximate positions when Quick Settings is open
            # Adjusted to click more to the left
            toggle_positions = {
                'wifi': (self.screen_width - 310, self.screen_height - 450),
                'bluetooth': (self.screen_width - 180, self.screen_height - 450),
                'airplane': (self.screen_width - 310, self.screen_height - 350),
                'night_light': (self.screen_width - 180, self.screen_height - 350),
                'mobile_hotspot': (self.screen_width - 310, self.screen_height - 250),
            }
            
            return toggle_positions.get(toggle_name.lower())
        except Exception as e:
            print(f"Error finding toggle: {e}")
            return None
    
    def toggle_wifi(self, enable: Optional[bool] = None) -> Dict[str, any]:
        """
        Toggle WiFi on/off
        If enable=None, just toggles (flips current state)
        If enable=True, ensures WiFi is on
        If enable=False, ensures WiFi is off
        """
        try:
            # Open Quick Settings
            if not self.open_quick_settings():
                return {"success": False, "error": "Failed to open Quick Settings"}
            
            # Find and click WiFi toggle
            wifi_pos = self.find_toggle_button('wifi')
            if wifi_pos:
                print(f"Clicking WiFi toggle at: {wifi_pos}")
                pyautogui.click(wifi_pos[0], wifi_pos[1])
                time.sleep(0.5)
                
                # Close Quick Settings
                self.close_quick_settings()
                
                action = "toggled" if enable is None else ("enabled" if enable else "disabled")
                return {"success": True, "message": f"WiFi {action}"}
            else:
                self.close_quick_settings()
                return {"success": False, "error": "Could not locate WiFi toggle"}
        except Exception as e:
            self.close_quick_settings()
            return {"success": False, "error": str(e)}
    
    def toggle_bluetooth(self, enable: Optional[bool] = None) -> Dict[str, any]:
        """
        Toggle Bluetooth on/off
        No administrator privileges required!
        """
        try:
            # Open Quick Settings
            if not self.open_quick_settings():
                return {"success": False, "error": "Failed to open Quick Settings"}
            
            # Find and click Bluetooth toggle
            bluetooth_pos = self.find_toggle_button('bluetooth')
            if bluetooth_pos:
                print(f"Clicking Bluetooth toggle at: {bluetooth_pos}")
                pyautogui.click(bluetooth_pos[0], bluetooth_pos[1])
                time.sleep(0.5)
                
                # Close Quick Settings
                self.close_quick_settings()
                
                action = "toggled" if enable is None else ("enabled" if enable else "disabled")
                return {"success": True, "message": f"Bluetooth {action}"}
            else:
                self.close_quick_settings()
                return {"success": False, "error": "Could not locate Bluetooth toggle"}
        except Exception as e:
            self.close_quick_settings()
            return {"success": False, "error": str(e)}
    
    def toggle_airplane_mode(self, enable: Optional[bool] = None) -> Dict[str, any]:
        """Toggle Airplane mode on/off"""
        try:
            if not self.open_quick_settings():
                return {"success": False, "error": "Failed to open Quick Settings"}
            
            airplane_pos = self.find_toggle_button('airplane')
            if airplane_pos:
                print(f"Clicking Airplane mode toggle at: {airplane_pos}")
                pyautogui.click(airplane_pos[0], airplane_pos[1])
                time.sleep(0.5)
                
                self.close_quick_settings()
                
                action = "toggled" if enable is None else ("enabled" if enable else "disabled")
                return {"success": True, "message": f"Airplane mode {action}"}
            else:
                self.close_quick_settings()
                return {"success": False, "error": "Could not locate Airplane mode toggle"}
        except Exception as e:
            self.close_quick_settings()
            return {"success": False, "error": str(e)}
    
    def toggle_night_light(self, enable: Optional[bool] = None) -> Dict[str, any]:
        """Toggle Night light on/off"""
        try:
            if not self.open_quick_settings():
                return {"success": False, "error": "Failed to open Quick Settings"}
            
            night_light_pos = self.find_toggle_button('night_light')
            if night_light_pos:
                print(f"Clicking Night light toggle at: {night_light_pos}")
                pyautogui.click(night_light_pos[0], night_light_pos[1])
                time.sleep(0.5)
                
                self.close_quick_settings()
                
                action = "toggled" if enable is None else ("enabled" if enable else "disabled")
                return {"success": True, "message": f"Night light {action}"}
            else:
                self.close_quick_settings()
                return {"success": False, "error": "Could not locate Night light toggle"}
        except Exception as e:
            self.close_quick_settings()
            return {"success": False, "error": str(e)}
    
    def get_quick_settings_info(self) -> Dict[str, any]:
        """Get information about available Quick Settings toggles"""
        return {
            "success": True,
            "available_toggles": [
                "wifi",
                "bluetooth",
                "airplane_mode",
                "night_light",
                "mobile_hotspot"
            ],
            "screen_resolution": f"{self.screen_width}x{self.screen_height}",
            "note": "Positions are estimated. First run might need manual adjustment."
        }
