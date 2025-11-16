"""
Window Control Helper for Gesture Actions
Provides cross-platform window management functionality
"""

import platform
import subprocess
from typing import Any

pyautogui: Any = None
PYAUTOGUI_AVAILABLE = False

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception as e:
    PYAUTOGUI_AVAILABLE = False
    print(f"⚠️  PyAutoGUI not available (no display): {e}")


class WindowControlHelper:
    """Helper class for window management operations"""
    
    def __init__(self):
        self.os = platform.system()
    
    def minimize_active_window(self):
        """Minimize the currently active window"""
        if not PYAUTOGUI_AVAILABLE:
            return {"success": False, "message": "PyAutoGUI not available in this environment"}
        try:
            if self.os == "Windows":
                pyautogui.hotkey('win', 'down')
                return {"success": True, "message": "Window minimized"}
            elif self.os == "Darwin":
                pyautogui.hotkey('command', 'm')
                return {"success": True, "message": "Window minimized"}
            elif self.os == "Linux":
                pyautogui.hotkey('super', 'h')
                return {"success": True, "message": "Window minimized"}
        except Exception as e:
            return {"success": False, "message": f"Failed to minimize: {e}"}
    
    def maximize_active_window(self):
        """Maximize the currently active window"""
        if not PYAUTOGUI_AVAILABLE:
            return {"success": False, "message": "PyAutoGUI not available in this environment"}
        try:
            if self.os == "Windows":
                pyautogui.hotkey('win', 'up')
                return {"success": True, "message": "Window maximized"}
            elif self.os == "Darwin":
                # macOS doesn't have a standard maximize hotkey
                # Use green button simulation
                pyautogui.hotkey('ctrl', 'command', 'f')
                return {"success": True, "message": "Window fullscreen"}
            elif self.os == "Linux":
                pyautogui.hotkey('super', 'up')
                return {"success": True, "message": "Window maximized"}
        except Exception as e:
            return {"success": False, "message": f"Failed to maximize: {e}"}
    
    def close_active_window(self):
        """Close the currently active window"""
        if not PYAUTOGUI_AVAILABLE:
            return {"success": False, "message": "PyAutoGUI not available in this environment"}
        try:
            if self.os == "Windows":
                pyautogui.hotkey('alt', 'f4')
                return {"success": True, "message": "Window closed"}
            elif self.os == "Darwin":
                pyautogui.hotkey('command', 'w')
                return {"success": True, "message": "Window closed"}
            elif self.os == "Linux":
                pyautogui.hotkey('alt', 'f4')
                return {"success": True, "message": "Window closed"}
        except Exception as e:
            return {"success": False, "message": f"Failed to close window: {e}"}
    
    def switch_desktop(self, direction="right"):
        """Switch to next/previous virtual desktop"""
        if not PYAUTOGUI_AVAILABLE:
            return {"success": False, "message": "PyAutoGUI not available in this environment"}
        try:
            if self.os == "Windows":
                if direction == "right":
                    pyautogui.hotkey('ctrl', 'win', 'right')
                else:
                    pyautogui.hotkey('ctrl', 'win', 'left')
                return {"success": True, "message": f"Switched desktop {direction}"}
            elif self.os == "Darwin":
                if direction == "right":
                    pyautogui.hotkey('ctrl', 'right')
                else:
                    pyautogui.hotkey('ctrl', 'left')
                return {"success": True, "message": f"Switched desktop {direction}"}
            elif self.os == "Linux":
                if direction == "right":
                    pyautogui.hotkey('ctrl', 'alt', 'right')
                else:
                    pyautogui.hotkey('ctrl', 'alt', 'left')
                return {"success": True, "message": f"Switched desktop {direction}"}
        except Exception as e:
            return {"success": False, "message": f"Failed to switch desktop: {e}"}
    
    def show_desktop(self):
        """Show desktop / minimize all windows"""
        if not PYAUTOGUI_AVAILABLE:
            return {"success": False, "message": "PyAutoGUI not available in this environment"}
        try:
            if self.os == "Windows":
                pyautogui.hotkey('win', 'd')
            elif self.os == "Darwin":
                pyautogui.hotkey('f11')
            elif self.os == "Linux":
                pyautogui.hotkey('ctrl', 'alt', 'd')
            return {"success": True, "message": "Desktop shown"}
        except Exception as e:
            return {"success": False, "message": f"Failed to show desktop: {e}"}
