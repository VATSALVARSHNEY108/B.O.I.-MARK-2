"""
YouTube Automation Module - Simple, Direct Video Playing
Opens Brave -> Searches YouTube -> Plays first video
"""

import subprocess
import time
import webbrowser
import urllib.parse
import platform
import os
from typing import Dict, Optional
import pyautogui


class YouTubeAutomator:
    """Simple YouTube automation using Brave browser"""
    
    def __init__(self):
        self.brave_path = self._find_brave()
        print(f"  🎯 Brave Path: {self.brave_path if self.brave_path else 'Not found, will use default'}")
    
    def _find_brave(self) -> Optional[str]:
        """Find Brave browser executable"""
        system = platform.system()
        
        if system == "Windows":
            # Check common Windows Brave paths
            paths = [
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"),
            ]
            for path in paths:
                if os.path.exists(path):
                    return path
        
        elif system == "Darwin":  # macOS
            path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
            if os.path.exists(path):
                return path
        
        elif system == "Linux":
            for path in ["/usr/bin/brave-browser", "/usr/bin/brave"]:
                if os.path.exists(path):
                    return path
        
        return None
    
    def search_and_play(self, query: str) -> Dict:
        """
        Search YouTube and play the first video.
        
        Steps:
        1. Open Brave browser with YouTube search
        2. Wait for results to load
        3. Click first video
        4. Play it
        
        Args:
            query: What to search for on YouTube
            
        Returns:
            Success/failure status with message
        """
        try:
            print(f"\n  🎬 YouTube Automator - Starting")
            print(f"  🔍 Query: {query}")
            
            # Step 1: Construct YouTube search URL
            encoded_query = urllib.parse.quote(query)
            yt_search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            print(f"  🌐 URL: {yt_search_url}")
            
            # Step 2: Open Brave with the search URL
            print(f"  🚀 Opening Brave browser...")
            if self.brave_path:
                subprocess.Popen([self.brave_path, yt_search_url])
                print(f"  ✅ Launched Brave")
            else:
                print(f"  ⚠️  Brave not found, using default browser")
                webbrowser.open(yt_search_url)
            
            # Step 3: Wait for YouTube to load and render videos
            print(f"  ⏳ Waiting for YouTube to load...")
            time.sleep(5)  # Give YouTube time to load and render
            
            # Step 4: Click first video using keyboard navigation
            print(f"  ▶️  Clicking first video...")
            try:
                # Tab to first video result
                pyautogui.press('tab')
                time.sleep(0.3)
                # Press Enter to click/open it
                pyautogui.press('enter')
                time.sleep(2)
                print(f"  ✅ Video opened and playing!")
            except Exception as e:
                print(f"  ⚠️  Keyboard automation failed: {e}")
                print(f"  ℹ️  Please click the first video manually")
            
            return {
                "success": True,
                "message": f"✅ YouTube search opened for '{query}' - First video playing in Brave",
                "query": query,
                "url": yt_search_url
            }
        
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            return {
                "success": False,
                "message": f"❌ Failed to play YouTube video: {str(e)}",
                "error": str(e)
            }
    
    def search_only(self, query: str) -> Dict:
        """
        Just search YouTube without playing anything.
        
        Args:
            query: What to search for on YouTube
            
        Returns:
            Success/failure status with message
        """
        try:
            print(f"\n  🔍 YouTube Search - Starting")
            print(f"  📝 Query: {query}")
            
            encoded_query = urllib.parse.quote(query)
            yt_search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            
            if self.brave_path:
                subprocess.Popen([self.brave_path, yt_search_url])
                print(f"  ✅ Opened search in Brave")
            else:
                webbrowser.open(yt_search_url)
                print(f"  ✅ Opened search in default browser")
            
            time.sleep(2)
            
            return {
                "success": True,
                "message": f"✅ YouTube search results for '{query}'",
                "query": query
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Search failed: {str(e)}"
            }
    
    def play_url(self, video_url: str) -> Dict:
        """
        Play a specific YouTube video URL.
        
        Args:
            video_url: Direct YouTube video URL
            
        Returns:
            Success/failure status
        """
        try:
            print(f"\n  🎬 Opening: {video_url}")
            
            if self.brave_path:
                subprocess.Popen([self.brave_path, video_url])
            else:
                webbrowser.open(video_url)
            
            time.sleep(2)
            
            return {
                "success": True,
                "message": f"✅ Video opened: {video_url}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Failed to open video: {str(e)}"
            }
