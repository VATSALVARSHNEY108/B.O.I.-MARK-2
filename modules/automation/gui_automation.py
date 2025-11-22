"""
GUI Automation Module
Handles all GUI automation tasks including mouse, keyboard, and desktop control
"""

import os
import time
import subprocess
from pathlib import Path

# Try to import pyautogui, but make it optional for cloud environments
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception:
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None

# Try to import pyperclip for clipboard operations
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except Exception:
    PYPERCLIP_AVAILABLE = False
    pyperclip = None


class GUIAutomation:
    """Handles GUI automation tasks"""
    
    def __init__(self):
        self.last_folder_suggestions = []
        self.available = PYAUTOGUI_AVAILABLE
    
    def open_application(self, app_name):
        """Open an application by name"""
        try:
            if not app_name:
                return False
            
            # Common application mappings
            app_mappings = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "paint": "mspaint.exe",
                "explorer": "explorer.exe",
                "chrome": "chrome.exe",
                "firefox": "firefox.exe",
                "edge": "msedge.exe",
                "vscode": "code.exe",
                "vs code": "code.exe",
                "spotify": "spotify.exe",
                "discord": "discord.exe",
                "cmd": "cmd.exe",
                "terminal": "cmd.exe",
                "powershell": "powershell.exe",
            }
            
            # Get the executable name
            executable = app_mappings.get(app_name.lower(), app_name)
            
            # Try to launch the application
            if os.name == 'nt':  # Windows
                subprocess.Popen(executable, shell=True)
            else:  # Linux/Mac
                subprocess.Popen([executable])
            
            return True
        except Exception as e:
            print(f"Failed to open application: {e}")
            return False
    
    def type_text(self, text, interval=0.0):
        """Type text using keyboard"""
        if not PYAUTOGUI_AVAILABLE:
            print("PyAutoGUI not available in this environment")
            return False
        
        try:
            pyautogui.write(text, interval=interval)
            return True
        except Exception as e:
            print(f"Failed to type text: {e}")
            return False
    
    def click(self, x=None, y=None, button='left'):
        """Click mouse at position or current position"""
        if not PYAUTOGUI_AVAILABLE:
            print("PyAutoGUI not available in this environment")
            return False
        
        try:
            if x is not None and y is not None:
                pyautogui.click(x, y, button=button)
            else:
                pyautogui.click(button=button)
            return True
        except Exception as e:
            print(f"Failed to click: {e}")
            return False
    
    def move_mouse(self, x, y):
        """Move mouse to position"""
        if not PYAUTOGUI_AVAILABLE:
            print("PyAutoGUI not available in this environment")
            return False
        
        try:
            pyautogui.moveTo(x, y)
            return True
        except Exception as e:
            print(f"Failed to move mouse: {e}")
            return False
    
    def press_key(self, key):
        """Press a keyboard key"""
        if not PYAUTOGUI_AVAILABLE:
            print("PyAutoGUI not available in this environment")
            return False
        
        try:
            pyautogui.press(key)
            return True
        except Exception as e:
            print(f"Failed to press key: {e}")
            return False
    
    def hotkey(self, *keys):
        """Press multiple keys as hotkey combination"""
        if not PYAUTOGUI_AVAILABLE:
            print("PyAutoGUI not available in this environment")
            return False
        
        try:
            pyautogui.hotkey(*keys)
            return True
        except Exception as e:
            print(f"Failed to press hotkey: {e}")
            return False
    
    def screenshot(self, filename="screenshot.png"):
        """Take a screenshot"""
        if not PYAUTOGUI_AVAILABLE:
            print("PyAutoGUI not available in this environment")
            return False
        
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            return True
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
            return False
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        if not PYPERCLIP_AVAILABLE:
            print("Pyperclip not available in this environment")
            return False
        
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"Failed to copy to clipboard: {e}")
            return False
    
    def paste_from_clipboard(self):
        """Paste from clipboard"""
        if not PYAUTOGUI_AVAILABLE:
            print("PyAutoGUI not available in this environment")
            return False
        
        try:
            pyautogui.hotkey('ctrl', 'v')
            return True
        except Exception as e:
            print(f"Failed to paste from clipboard: {e}")
            return False
    
    def wait(self, seconds):
        """Wait for specified seconds"""
        try:
            time.sleep(seconds)
            return True
        except Exception as e:
            print(f"Failed to wait: {e}")
            return False
    
    def open_folder(self, folder_path=None, folder_name=None):
        """Open a folder in file explorer"""
        try:
            # Get user directories
            home = Path.home()
            
            # Check for OneDrive synced folders
            onedrive_desktop = home / "OneDrive" / "Desktop"
            desktop = onedrive_desktop if onedrive_desktop.exists() else home / "Desktop"
            
            onedrive_documents = home / "OneDrive" / "Documents"
            documents = onedrive_documents if onedrive_documents.exists() else home / "Documents"
            
            downloads = home / "Downloads"
            
            onedrive_pictures = home / "OneDrive" / "Pictures"
            pictures = onedrive_pictures if onedrive_pictures.exists() else home / "Pictures"
            
            # If folder_path is provided, use it directly
            if folder_path:
                target_path = folder_path
            # If folder_name is provided, search in common locations
            elif folder_name:
                # Search in Desktop first
                desktop_folder = desktop / folder_name
                if desktop_folder.exists():
                    target_path = str(desktop_folder)
                else:
                    # Search in Documents
                    docs_folder = documents / folder_name
                    if docs_folder.exists():
                        target_path = str(docs_folder)
                    else:
                        # Search in Downloads
                        downloads_folder = downloads / folder_name
                        if downloads_folder.exists():
                            target_path = str(downloads_folder)
                        else:
                            # Search in Home
                            home_folder = home / folder_name
                            if home_folder.exists():
                                target_path = str(home_folder)
                            else:
                                # Folder not found, provide suggestions
                                self._generate_folder_suggestions(folder_name)
                                return False
            else:
                # No folder specified, open home directory
                target_path = str(home)
            
            # Open the folder
            if os.name == 'nt':  # Windows
                subprocess.Popen('explorer "' + target_path + '"')
            elif os.name == 'posix':  # Linux/Mac
                if os.uname().sysname == 'Darwin':  # Mac
                    subprocess.Popen(['open', target_path])
                else:  # Linux
                    subprocess.Popen(['xdg-open', target_path])
            
            return True
        except Exception as e:
            print(f"Failed to open folder: {e}")
            return False
    
    def open_desktop_folder(self, folder_name=None):
        """Open Desktop or a folder on Desktop"""
        try:
            home = Path.home()
            # Check for OneDrive Desktop
            onedrive_desktop = home / "OneDrive" / "Desktop"
            desktop = onedrive_desktop if onedrive_desktop.exists() else home / "Desktop"
            
            # If no folder name, open Desktop itself
            if not folder_name:
                target_path = str(desktop)
            else:
                # Open folder on Desktop
                target_folder = desktop / folder_name
                if target_folder.exists():
                    target_path = str(target_folder)
                else:
                    # Folder not found on Desktop
                    self._generate_folder_suggestions(folder_name, desktop_only=True)
                    return False
            
            # Open the folder
            if os.name == 'nt':  # Windows
                subprocess.Popen('explorer "' + target_path + '"')
            elif os.name == 'posix':  # Linux/Mac
                if os.uname().sysname == 'Darwin':  # Mac
                    subprocess.Popen(['open', target_path])
                else:  # Linux
                    subprocess.Popen(['xdg-open', target_path])
            
            return True
        except Exception as e:
            print(f"Failed to open desktop folder: {e}")
            return False
    
    def _generate_folder_suggestions(self, search_name, desktop_only=False):
        """Generate folder name suggestions"""
        self.last_folder_suggestions = []
        
        try:
            home = Path.home()
            
            # Check for OneDrive folders
            onedrive_desktop = home / "OneDrive" / "Desktop"
            desktop = onedrive_desktop if onedrive_desktop.exists() else home / "Desktop"
            
            onedrive_documents = home / "OneDrive" / "Documents"
            documents = onedrive_documents if onedrive_documents.exists() else home / "Documents"
            
            # Define search locations
            if desktop_only:
                search_locations = [desktop]
            else:
                search_locations = [
                    desktop,
                    documents,
                    home / "Downloads",
                    home
                ]
            
            # Search for similar folder names
            for location in search_locations:
                if location.exists():
                    for item in location.iterdir():
                        if item.is_dir():
                            # Check if folder name is similar
                            if search_name.lower() in item.name.lower():
                                self.last_folder_suggestions.append(str(item))
            
            # Limit to 5 suggestions
            self.last_folder_suggestions = self.last_folder_suggestions[:5]
        except Exception as e:
            print(f"Failed to generate suggestions: {e}")


if __name__ == "__main__":
    # Test the GUI automation
    gui = GUIAutomation()
    print("GUI Automation Module - Testing")
    print(f"PyAutoGUI Available: {PYAUTOGUI_AVAILABLE}")
    print(f"Pyperclip Available: {PYPERCLIP_AVAILABLE}")
