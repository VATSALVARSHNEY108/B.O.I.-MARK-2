import time
import os
import platform
from typing import Any

pyautogui: Any = None
pyperclip: Any = None
GUI_AVAILABLE = False

try:
    import pyautogui
    import pyperclip
    GUI_AVAILABLE = True
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
except Exception as e:
    GUI_AVAILABLE = False
    print(f"⚠️  GUI automation not available in this environment: {e}")
    print("Running in DEMO MODE - commands will be simulated")

class GUIAutomation:
    """Handles all GUI automation tasks using PyAutoGUI"""
    
    def __init__(self):
        self.demo_mode = not GUI_AVAILABLE
        if GUI_AVAILABLE:
            self.screen_width, self.screen_height = pyautogui.size()
        else:
            self.screen_width, self.screen_height = 1920, 1080
            print(f"📺 Simulated screen size: {self.screen_width}x{self.screen_height}")
    
    def _log_demo(self, action: str):
        """Log demo mode actions"""
        if self.demo_mode:
            print(f"  [DEMO] {action}")
    
    def open_application(self, app_name: str) -> bool:
        """Open an application based on the operating system"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would open application: {app_name}")
                return True
            
            system = platform.system()
            
            if system == "Windows":
                pyautogui.press('win')
                time.sleep(0.5)
                pyautogui.write(app_name, interval=0.1)
                time.sleep(0.5)
                pyautogui.press('enter')
            elif system == "Darwin":
                pyautogui.hotkey('command', 'space')
                time.sleep(0.5)
                pyautogui.write(app_name, interval=0.1)
                time.sleep(0.5)
                pyautogui.press('enter')
            elif system == "Linux":
                pyautogui.hotkey('alt', 'f2')
                time.sleep(0.5)
                pyautogui.write(app_name, interval=0.1)
                time.sleep(0.5)
                pyautogui.press('enter')
            else:
                return False
            
            return True
        except Exception as e:
            print(f"Error opening application: {e}")
            return False
    
    def type_text(self, text: str, interval: float = 0.05) -> bool:
        """Type text with specified interval between keystrokes"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would type: '{text}'")
                return True
            
            pyautogui.write(text, interval=interval)
            return True
        except Exception as e:
            print(f"Error typing text: {e}")
            return False
    
    def click(self, x: int | None = None, y: int | None = None, button: str = 'left', clicks: int = 1) -> bool:
        """Click at specified position or current position"""
        try:
            if self.demo_mode:
                if x is not None and y is not None:
                    self._log_demo(f"Would click {button} button at ({x}, {y})")
                else:
                    self._log_demo(f"Would click {button} button at current position")
                return True
            
            if x is not None and y is not None:
                pyautogui.click(x, y, button=button, clicks=clicks)
            else:
                pyautogui.click(button=button, clicks=clicks)
            return True
        except Exception as e:
            print(f"Error clicking: {e}")
            return False
    
    def click_at_position(self, x: int, y: int, button: str = 'left') -> bool:
        """Click at a specific screen position with a single click"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would single click at position ({x}, {y})")
                return True
            
            print(f"  🖱️  Single clicking at position ({x}, {y})")
            # Move to position first, then do a single left-click
            pyautogui.moveTo(x, y, duration=0.2)
            time.sleep(0.1)
            # Explicitly set clicks=1 for single click only
            pyautogui.click(x, y, button='left', clicks=1)
            return True
        except Exception as e:
            print(f"Error clicking at position: {e}")
            return False
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> bool:
        """Move mouse to specified position"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would move mouse to ({x}, {y})")
                return True
            
            pyautogui.moveTo(x, y, duration=duration)
            return True
        except Exception as e:
            print(f"Error moving mouse: {e}")
            return False
    
    def press_key(self, key: str, presses: int = 1) -> bool:
        """Press a keyboard key"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would press key: {key} ({presses} time(s))")
                return True
            
            pyautogui.press(key, presses=presses)
            return True
        except Exception as e:
            print(f"Error pressing key: {e}")
            return False
    
    def hotkey(self, *keys) -> bool:
        """Press a combination of keys"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would press hotkey: {'+'.join(keys)}")
                return True
            
            pyautogui.hotkey(*keys)
            return True
        except Exception as e:
            print(f"Error with hotkey: {e}")
            return False
    
    def screenshot(self, filename: str = "screenshot.png") -> bool:
        """Take a screenshot and save it"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would take screenshot and save as: {filename}")
                return True
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            print(f"Screenshot saved as {filename}")
            return True
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return False
    
    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would copy to clipboard: '{text[:50]}...'")
                return True
            
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            return False
    
    def paste_from_clipboard(self) -> bool:
        """Paste from clipboard"""
        try:
            if self.demo_mode:
                self._log_demo("Would paste from clipboard")
                return True
            
            system = platform.system()
            if system == "Darwin":
                pyautogui.hotkey('command', 'v')
            else:
                pyautogui.hotkey('ctrl', 'v')
            return True
        except Exception as e:
            print(f"Error pasting: {e}")
            return False
    
    def get_mouse_position(self) -> tuple:
        """Get current mouse position"""
        if self.demo_mode:
            return (0, 0)
        return pyautogui.position()
    
    def wait(self, seconds: float) -> bool:
        """Wait for specified seconds"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would wait {seconds} seconds")
                time.sleep(0.1)
                return True
            
            time.sleep(seconds)
            return True
        except Exception as e:
            print(f"Error waiting: {e}")
            return False
