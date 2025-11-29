"""
Complete Windows 11 Settings Automator
Controls all Windows settings through Quick Settings panel automation
No administrator privileges required!
"""

import pyautogui
import time
import platform
from typing import Dict, Optional, Tuple

# Configure PyAutoGUI
pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True


class SettingsAutomator:
    """Complete Windows 11 settings control via UI automation"""
    
    def __init__(self):
        if platform.system() != "Windows":
            raise RuntimeError("This controller only works on Windows 11")
        
        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Quick Settings button position (system tray)
        self.quick_settings_position = (self.screen_width - 200, self.screen_height - 35)
        
        # Toggle button positions (when panel is open)
        self.toggle_positions = {
            'night_light': (self.screen_width - 280, self.screen_height - 380),
            'bluetooth': (self.screen_width - 170, self.screen_height - 380),
            'wifi': (self.screen_width - 280, self.screen_height - 280),
            'airplane': (self.screen_width - 170, self.screen_height - 280),
            'mobile_hotspot': (self.screen_width - 280, self.screen_height - 180),
            'battery_saver': (self.screen_width - 170, self.screen_height - 180),
        }
    
    
    def open_quick_settings(self) -> bool:
        """Open the Quick Settings panel"""
        try:
            pyautogui.click(self.quick_settings_position[0], self.quick_settings_position[1])
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error opening Quick Settings: {e}")
            return False
    
    def close_quick_settings(self) -> bool:
        """Close Quick Settings panel"""
        try:
            pyautogui.press('escape')
            time.sleep(0.3)
            return True
        except Exception as e:
            print(f"Error closing Quick Settings: {e}")
            return False
    
    def click_toggle(self, toggle_name: str) -> Dict[str, any]:
        """Click a specific toggle in Quick Settings"""
        try:
            # Open Quick Settings
            if not self.open_quick_settings():
                return {"success": False, "error": "Failed to open Quick Settings"}
            
            # Get toggle position
            position = self.toggle_positions.get(toggle_name.lower())
            if not position:
                self.close_quick_settings()
                return {"success": False, "error": f"Unknown toggle: {toggle_name}"}
            
            # Click the toggle
            print(f"Clicking {toggle_name} at position: {position}")
            pyautogui.click(position[0], position[1])
            time.sleep(0.5)
            
            # Close Quick Settings
            self.close_quick_settings()
            
            return {"success": True, "message": f"{toggle_name.title()} toggled"}
        except Exception as e:
            self.close_quick_settings()
            return {"success": False, "error": str(e)}
    
    
    def toggle_wifi(self) -> Dict[str, any]:
        """Toggle WiFi on/off"""
        return self.click_toggle('wifi')
    
    def toggle_bluetooth(self) -> Dict[str, any]:
        """Toggle Bluetooth on/off"""
        return self.click_toggle('bluetooth')
    
    def toggle_airplane_mode(self) -> Dict[str, any]:
        """Toggle Airplane mode on/off"""
        return self.click_toggle('airplane')
    
    def toggle_mobile_hotspot(self) -> Dict[str, any]:
        """Toggle Mobile hotspot on/off"""
        return self.click_toggle('mobile_hotspot')
    
    
    def toggle_night_light(self) -> Dict[str, any]:
        """Toggle Night light on/off"""
        return self.click_toggle('night_light')
    
    
    def toggle_battery_saver(self) -> Dict[str, any]:
        """Toggle Battery saver on/off"""
        return self.click_toggle('battery_saver')
    
    
    def set_volume(self, level: int) -> Dict[str, any]:
        """Set system volume (0-100)"""
        try:
            if not 0 <= level <= 100:
                return {"success": False, "error": "Volume must be between 0 and 100"}
            
            # Calculate how many times to press volume key
            for _ in range(50):  # Reset to 0
                pyautogui.press('volumedown')
            
            # Press volume up to desired level
            presses = level // 2
            for _ in range(presses):
                pyautogui.press('volumeup')
            
            return {"success": True, "message": f"Volume set to {level}%"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def volume_up(self, steps: int = 2) -> Dict[str, any]:
        """Increase volume"""
        try:
            for _ in range(steps):
                pyautogui.press('volumeup')
            return {"success": True, "message": f"Volume increased by {steps * 2}%"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def volume_down(self, steps: int = 2) -> Dict[str, any]:
        """Decrease volume"""
        try:
            for _ in range(steps):
                pyautogui.press('volumedown')
            return {"success": True, "message": f"Volume decreased by {steps * 2}%"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def mute(self) -> Dict[str, any]:
        """Toggle mute"""
        try:
            pyautogui.press('volumemute')
            return {"success": True, "message": "Volume muted/unmuted"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    
    def brightness_up(self, steps: int = 1) -> Dict[str, any]:
        """Increase brightness"""
        try:
            for _ in range(steps):
                pyautogui.press('brightnessup')
            return {"success": True, "message": f"Brightness increased"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def brightness_down(self, steps: int = 1) -> Dict[str, any]:
        """Decrease brightness"""
        try:
            for _ in range(steps):
                pyautogui.press('brightnessdown')
            return {"success": True, "message": f"Brightness decreased"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    
    def get_available_toggles(self) -> Dict[str, any]:
        """Get list of available toggles"""
        return {
            "success": True,
            "toggles": list(self.toggle_positions.keys()),
            "screen_resolution": f"{self.screen_width}x{self.screen_height}",
            "quick_settings_position": self.quick_settings_position
        }
    
    def adjust_toggle_position(self, toggle_name: str, x_offset: int = 0, y_offset: int = 0) -> Dict[str, any]:
        """Adjust position of a toggle button"""
        if toggle_name.lower() not in self.toggle_positions:
            return {"success": False, "error": f"Unknown toggle: {toggle_name}"}
        
        current_x, current_y = self.toggle_positions[toggle_name.lower()]
        new_x = current_x + x_offset
        new_y = current_y + y_offset
        
        self.toggle_positions[toggle_name.lower()] = (new_x, new_y)
        
        return {
            "success": True,
            "message": f"{toggle_name} position adjusted to ({new_x}, {new_y})"
        }
