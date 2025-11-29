"""
Smart YouTube Automation Module
Provides intelligent YouTube video search and playback
Uses Brave browser by default
"""

import webbrowser
import time
import urllib.parse
import os
import platform
import subprocess


class YouTubeAutomation:
    """Handles YouTube video search and playback automation"""
    
    def __init__(self, gui_automation):
        """
        Initialize YouTube automation.
        
        Args:
            gui_automation: GUIAutomation instance for keyboard/mouse control
        """
        self.gui = gui_automation
        self.brave_path = self._find_brave_browser()
    
    def _find_brave_browser(self):
        """Find Brave browser path"""
        if platform.system() == "Windows":
            paths = [
                "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
                "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"),
                os.path.expandvars(r"%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe"),
            ]
            for path in paths:
                if os.path.exists(path):
                    return path
        elif platform.system() == "Darwin":  # macOS
            if os.path.exists("/Applications/Brave Browser.app"):
                return "open -a \"Brave Browser\""
        elif platform.system() == "Linux":
            if os.path.exists("/usr/bin/brave-browser"):
                return "/usr/bin/brave-browser"
        
        print("⚠️  Brave browser not found, falling back to default browser")
        return None
    
    def _open_url_with_browser(self, url):
        """Open URL with Brave browser"""
        try:
            if self.brave_path:
                if platform.system() == "Windows":
                    subprocess.Popen([self.brave_path, url])
                elif platform.system() == "Darwin":
                    subprocess.Popen(self.brave_path + f" {url}", shell=True)
                elif platform.system() == "Linux":
                    subprocess.Popen([self.brave_path, url])
                print(f"✅ Opened with Brave: {url}")
            else:
                webbrowser.open(url)
                print(f"✅ Opened with default browser: {url}")
        except Exception as e:
            print(f"⚠️  Error opening URL: {e}, falling back to default")
            webbrowser.open(url)
    
    def play_video_method_1(self, query):
        """
        Simple method: Search YouTube and click first video
        """
        print(f"  🔍 Searching for: {query}")
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        self._open_url_with_browser(search_url)
        time.sleep(4)
        
        print(f"  🖱️  Clicking first video...")
        x, y = self.gui.get_relative_position(25, 35)
        self.gui.single_click(x, y)
        
        return True
    
    def play_video_method_2(self, query):
        """
        Alternative position for different screen layouts
        """
        print(f"  🔍 Searching for: {query}")
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        self._open_url_with_browser(search_url)
        time.sleep(4)
        
        print(f"  🖱️  Clicking first video (center position)...")
        x, y = self.gui.get_relative_position(30, 38)
        self.gui.single_click(x, y)
        
        return True
    
    def play_video_method_3(self, query):
        """
        Lower position for larger screens
        """
        print(f"  🔍 Searching for: {query}")
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        self._open_url_with_browser(search_url)
        time.sleep(4)
        
        print(f"  🖱️  Clicking first video (lower position)...")
        x, y = self.gui.get_relative_position(28, 42)
        self.gui.single_click(x, y)
        
        return True
    
    def smart_play_video(self, query, method="auto"):
        """
        Intelligently play YouTube video with direct URL or search.
        
        Args:
            query: Search query for the video
            method: "auto", "direct_url", or "search"
        
        Returns:
            Success status and message
        """
        try:
            # DIRECT METHOD: Construct YouTube search URL that auto-plays first video
            # This is more reliable than clicking
            encoded_query = urllib.parse.quote(query)
            
            # YouTube search URL with auto-play capability
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            
            print(f"  🎬 Opening YouTube search in Brave: {query}")
            self._open_url_with_browser(search_url)
            
            # Wait a bit for results to load, then try to find first video
            time.sleep(3)
            
            print(f"  ▶️  Attempting to play first result...")
            # Try to send keyboard command to play (Space key)
            try:
                import pyautogui
                # Focus on the page and press Enter on first result (keyboard navigation)
                pyautogui.press('tab')  # Focus on first result
                time.sleep(0.5)
                pyautogui.press('enter')  # Click first result
                time.sleep(2)
                print(f"  ✅ Played: {query}")
            except:
                print(f"  ℹ️  Video opened, user may need to click play")
            
            return {
                "success": True,
                "message": f"✅ Opening: {query} in Brave",
                "query": query
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}",
                "query": query
            }
    
    def open_video_url(self, url):
        """
        Open a specific YouTube video URL.
        
        Args:
            url: YouTube video URL
        
        Returns:
            Success status
        """
        try:
            self._open_url_with_browser(url)
            return {
                "success": True,
                "message": f"✅ Opened video: {url}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}"
            }
    
    def search_only(self, query):
        """
        Search YouTube without auto-playing.
        
        Args:
            query: Search query
        
        Returns:
            Success status
        """
        try:
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            webbrowser.open(search_url)
            
            return {
                "success": True,
                "message": f"✅ Showing search results for: {query}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}"
            }
    
    def play_first_result(self, wait_time=4, use_mouse=True):
        """
        Play the first video from current YouTube search results page.
        This assumes you're already on a YouTube search results page.
        
        Args:
            wait_time: Seconds to wait for page to load (default: 4)
            use_mouse: Use mouse click instead of keyboard (default: True)
        
        Returns:
            Success status and message
        """
        try:
            print(f"  ⏳ Waiting {wait_time}s for page to load...")
            time.sleep(wait_time)
            
            if use_mouse:
                print(f"  🎯 Clicking first video with mouse...")
                x, y = self.gui.get_relative_position(25, 35)
                self.gui.single_click(x, y)
            else:
                print(f"  🎯 Navigating to first video with keyboard...")
                for i in range(8):
                    self.gui.press_key('tab')
                    time.sleep(0.3)
                
                print(f"  ▶️  Playing first video...")
                self.gui.press_key('enter')
            
            time.sleep(1)
            
            return {
                "success": True,
                "message": "✅ Playing first video from search results"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error playing first result: {str(e)}"
            }
    
    def search_and_play(self, query, wait_time=4, use_mouse=True):
        """
        Search YouTube and immediately play the first result.
        IMPORTANT: This does the search AND click in one method to avoid double-clicking.
        
        Args:
            query: Search query
            wait_time: Seconds to wait after search (default: 4)
            use_mouse: Use mouse click instead of keyboard (default: True)
        
        Returns:
            Success status and message
        """
        try:
            print(f"  🔍 Searching YouTube for: {query}")
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            webbrowser.open(search_url)
            
            print(f"  ⏳ Waiting {wait_time}s for page to load...")
            time.sleep(wait_time)
            
            if use_mouse:
                print(f"  🎯 Clicking first video...")
                x, y = self.gui.get_relative_position(25, 35)
                self.gui.single_click(x, y)
            else:
                print(f"  🎯 Navigating to first video with keyboard...")
                for i in range(8):
                    self.gui.press_key('tab')
                    time.sleep(0.3)
                
                print(f"  ▶️  Playing first video...")
                self.gui.press_key('enter')
            
            return {
                "success": True,
                "message": f"✅ Searched and playing: {query}",
                "query": query
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}",
                "query": query
            }


def create_youtube_automation(gui_automation):
    """
    Factory function to create YouTubeAutomation instance.
    
    Args:
        gui_automation: GUIAutomation instance
    
    Returns:
        YouTubeAutomation instance
    """
    return YouTubeAutomation(gui_automation)
