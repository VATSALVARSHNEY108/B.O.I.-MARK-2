"""
Fullscreen App Automation
Opens applications in fullscreen mode and performs automation tasks
"""

import time
import subprocess
import platform
from typing import Optional, Dict, Any


class FullscreenAutomation:
    """Automates apps by opening them in fullscreen and performing actions"""
    
    def __init__(self):
        """Initialize fullscreen automation"""
        self.current_app = None
        self.is_fullscreen = False
        self.system = platform.system()
        
        # Try to import pyautogui for automation
        try:
            import pyautogui
            self.pyautogui = pyautogui
            self.automation_available = True
        except ImportError:
            self.pyautogui = None
            self.automation_available = False
            print("⚠️ PyAutoGUI not available - automation features limited")
    
    def open_app_fullscreen(self, app_name: str) -> Dict[str, Any]:
        """
        Open an application and maximize it to fullscreen
        
        Args:
            app_name: Name or path of the application
        
        Returns:
            Dict with success status and message
        """
        try:
            # Launch the application
            if self.system == "Windows":
                process = subprocess.Popen(app_name, shell=True)
            elif self.system == "Darwin":  # macOS
                process = subprocess.Popen(["open", "-a", app_name])
            else:  # Linux
                process = subprocess.Popen([app_name])
            
            # Wait for app to open
            time.sleep(2)
            
            # Make it fullscreen
            if self.automation_available:
                self._make_fullscreen()
            
            self.current_app = app_name
            self.is_fullscreen = True
            
            return {
                "success": True,
                "message": f"✅ Opened {app_name} in fullscreen mode",
                "app": app_name
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Failed to open {app_name}: {str(e)}",
                "app": app_name
            }
    
    def _make_fullscreen(self):
        """Make the current window fullscreen"""
        if not self.automation_available:
            return
        
        if self.system == "Windows":
            # Press F11 for fullscreen (works in most apps)
            self.pyautogui.press('f11')
            time.sleep(0.5)
            # Alternative: Alt+Enter
            # self.pyautogui.hotkey('alt', 'enter')
        
        elif self.system == "Darwin":  # macOS
            # Control+Command+F for fullscreen
            self.pyautogui.hotkey('ctrl', 'command', 'f')
            time.sleep(0.5)
        
        else:  # Linux
            # F11 works on most Linux apps
            self.pyautogui.press('f11')
            time.sleep(0.5)
    
    def maximize_window(self):
        """Maximize current window (not fullscreen, just maximized)"""
        if not self.automation_available:
            return {"success": False, "message": "Automation not available"}
        
        try:
            if self.system == "Windows":
                # Windows key + Up arrow to maximize
                self.pyautogui.hotkey('win', 'up')
            elif self.system == "Darwin":
                # Click the green button (needs precise positioning)
                # This is tricky, better to use F11
                self.pyautogui.press('f11')
            else:
                # Most Linux window managers support this
                self.pyautogui.hotkey('super', 'up')
            
            time.sleep(0.5)
            return {"success": True, "message": "Window maximized"}
        
        except Exception as e:
            return {"success": False, "message": f"Failed to maximize: {str(e)}"}
    
    def type_text(self, text: str, interval: float = 0.05):
        """Type text in the current application"""
        if not self.automation_available:
            return {"success": False, "message": "Automation not available"}
        
        try:
            self.pyautogui.write(text, interval=interval)
            return {"success": True, "message": f"Typed: {text[:50]}..."}
        except Exception as e:
            return {"success": False, "message": f"Failed to type: {str(e)}"}
    
    def press_key(self, key: str):
        """Press a specific key"""
        if not self.automation_available:
            return {"success": False, "message": "Automation not available"}
        
        try:
            self.pyautogui.press(key)
            return {"success": True, "message": f"Pressed key: {key}"}
        except Exception as e:
            return {"success": False, "message": f"Failed to press key: {str(e)}"}
    
    def hotkey(self, *keys):
        """Press a hotkey combination"""
        if not self.automation_available:
            return {"success": False, "message": "Automation not available"}
        
        try:
            self.pyautogui.hotkey(*keys)
            return {"success": True, "message": f"Pressed hotkey: {'+'.join(keys)}"}
        except Exception as e:
            return {"success": False, "message": f"Failed hotkey: {str(e)}"}
    
    def click_at(self, x: int, y: int):
        """Click at specific coordinates"""
        if not self.automation_available:
            return {"success": False, "message": "Automation not available"}
        
        try:
            self.pyautogui.click(x, y)
            return {"success": True, "message": f"Clicked at ({x}, {y})"}
        except Exception as e:
            return {"success": False, "message": f"Failed to click: {str(e)}"}
    
    def take_screenshot(self, filename: Optional[str] = None) -> Dict[str, Any]:
        """Take a screenshot of the current screen"""
        if not self.automation_available:
            return {"success": False, "message": "Automation not available"}
        
        try:
            if filename is None:
                filename = f"screenshot_{int(time.time())}.png"
            
            screenshot = self.pyautogui.screenshot()
            screenshot.save(filename)
            
            return {
                "success": True,
                "message": f"Screenshot saved: {filename}",
                "path": filename
            }
        except Exception as e:
            return {"success": False, "message": f"Failed screenshot: {str(e)}"}
    
    def exit_fullscreen(self):
        """Exit fullscreen mode"""
        if not self.automation_available:
            return {"success": False, "message": "Automation not available"}
        
        try:
            if self.system == "Windows" or self.system == "Linux":
                self.pyautogui.press('f11')
            elif self.system == "Darwin":
                self.pyautogui.hotkey('ctrl', 'command', 'f')
            
            self.is_fullscreen = False
            return {"success": True, "message": "Exited fullscreen"}
        except Exception as e:
            return {"success": False, "message": f"Failed to exit fullscreen: {str(e)}"}
    
    def workflow_example(self, app_name: str):
        """
        Example workflow: Open app in fullscreen and perform actions
        
        Args:
            app_name: Application to open
        """
        print(f"\n🚀 Starting fullscreen automation for: {app_name}")
        
        # Step 1: Open app in fullscreen
        result = self.open_app_fullscreen(app_name)
        print(result["message"])
        
        if not result["success"]:
            return result
        
        # Step 2: Wait for app to fully load
        print("⏳ Waiting for app to load...")
        time.sleep(3)
        
        # Step 3: Take a screenshot
        screenshot_result = self.take_screenshot()
        print(screenshot_result["message"])
        
        # Step 4: Example actions (customize based on your needs)
        # self.type_text("Hello from automation!")
        # self.press_key('enter')
        
        return {
            "success": True,
            "message": f"✅ Fullscreen automation completed for {app_name}",
            "screenshot": screenshot_result.get("path")
        }


def create_fullscreen_automation() -> FullscreenAutomation:
    """Factory function to create FullscreenAutomation instance"""
    return FullscreenAutomation()


if __name__ == "__main__":
    import sys
    
    automation = create_fullscreen_automation()
    
    if len(sys.argv) < 2:
        print("Usage: python fullscreen_automation.py <app_name>")
        print("Example: python fullscreen_automation.py notepad")
        sys.exit(1)
    
    app_name = sys.argv[1]
    result = automation.workflow_example(app_name)
    print(f"\n{result['message']}")
