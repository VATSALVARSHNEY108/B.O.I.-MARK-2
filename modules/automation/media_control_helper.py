"""
Media Control Helper for Gesture Actions
Provides cross-platform media playback control
"""

import platform
import pyautogui


class MediaControlHelper:
    """Helper class for media control operations"""
    
    def __init__(self):
        self.os = platform.system()
    
    def play_pause(self):
        """Toggle play/pause for media"""
        try:
            pyautogui.press('playpause')
            return {"success": True, "message": "Play/Pause toggled"}
        except Exception as e:
            return {"success": False, "message": f"Failed to toggle play/pause: {e}"}
    
    def next_track(self):
        """Skip to next track"""
        try:
            pyautogui.press('nexttrack')
            return {"success": True, "message": "Next track"}
        except Exception as e:
            return {"success": False, "message": f"Failed to skip track: {e}"}
    
    def previous_track(self):
        """Go to previous track"""
        try:
            pyautogui.press('prevtrack')
            return {"success": True, "message": "Previous track"}
        except Exception as e:
            return {"success": False, "message": f"Failed to go to previous track: {e}"}
    
    def stop(self):
        """Stop media playback"""
        try:
            pyautogui.press('stop')
            return {"success": True, "message": "Media stopped"}
        except Exception as e:
            return {"success": False, "message": f"Failed to stop: {e}"}
    
    def volume_up(self, steps=1):
        """Increase volume"""
        try:
            for _ in range(steps):
                pyautogui.press('volumeup')
            return {"success": True, "message": f"Volume increased"}
        except Exception as e:
            return {"success": False, "message": f"Failed to increase volume: {e}"}
    
    def volume_down(self, steps=1):
        """Decrease volume"""
        try:
            for _ in range(steps):
                pyautogui.press('volumedown')
            return {"success": True, "message": f"Volume decreased"}
        except Exception as e:
            return {"success": False, "message": f"Failed to decrease volume: {e}"}
    
    def mute(self):
        """Mute/unmute volume"""
        try:
            pyautogui.press('volumemute')
            return {"success": True, "message": "Volume muted/unmuted"}
        except Exception as e:
            return {"success": False, "message": f"Failed to mute: {e}"}
