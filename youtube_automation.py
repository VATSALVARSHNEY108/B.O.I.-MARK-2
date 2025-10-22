"""
Smart YouTube Automation Module
Provides intelligent YouTube video search and playback
"""

import webbrowser
import time
import urllib.parse


class YouTubeAutomation:
    """Handles YouTube video search and playback automation"""
    
    def __init__(self, gui_automation):
        """
        Initialize YouTube automation.
        
        Args:
            gui_automation: GUIAutomation instance for keyboard/mouse control
        """
        self.gui = gui_automation
    
    def play_video_method_1(self, query):
        """
        Method 1: Open YouTube homepage, search, then navigate to first video
        Most reliable across different browsers
        """
        print(f"  🎬 Method 1: Opening YouTube homepage...")
        webbrowser.open("https://www.youtube.com")
        time.sleep(3)
        
        print(f"  🔍 Searching for: {query}")
        # Press / to focus search box
        self.gui.press_key('/')
        time.sleep(0.5)
        
        # Type search query
        self.gui.type_text(query, interval=0.1)
        time.sleep(0.5)
        
        # Press Enter to search
        print(f"  🔎 Executing search...")
        self.gui.press_key('enter')
        time.sleep(3)
        
        # Navigate to first video
        print(f"  🎯 Navigating to first video...")
        for i in range(6):
            self.gui.press_key('tab')
            time.sleep(0.3)
        
        # Play video
        print(f"  ▶️  Playing video...")
        self.gui.press_key('enter')
        
        return True
    
    def play_video_method_2(self, query):
        """
        Method 2: Direct search URL, then keyboard navigation
        Faster but may need adjustment based on browser
        """
        print(f"  🎬 Method 2: Using direct search URL...")
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        webbrowser.open(search_url)
        time.sleep(3)
        
        print(f"  🎯 Navigating to first video...")
        # Tab through to first video (may vary by browser)
        for i in range(4):
            self.gui.press_key('tab')
            time.sleep(0.3)
        
        # Play video
        print(f"  ▶️  Playing video...")
        self.gui.press_key('enter')
        
        return True
    
    def play_video_method_3(self, query):
        """
        Method 3: Search URL with auto-play trick
        Opens search results and uses keyboard shortcut
        """
        print(f"  🎬 Method 3: Using search with keyboard shortcuts...")
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        webbrowser.open(search_url)
        time.sleep(3)
        
        # Try using keyboard navigation
        print(f"  🎯 Using smart navigation...")
        # Press Tab a few times to get to first video
        self.gui.press_key('tab')
        time.sleep(0.2)
        self.gui.press_key('tab')
        time.sleep(0.2)
        self.gui.press_key('tab')
        time.sleep(0.2)
        
        # Press Enter
        self.gui.press_key('enter')
        
        return True
    
    def smart_play_video(self, query, method="auto"):
        """
        Intelligently play YouTube video with fallback methods.
        
        Args:
            query: Search query for the video
            method: "auto", "method1", "method2", or "method3"
        
        Returns:
            Success status and message
        """
        try:
            if method == "method1":
                self.play_video_method_1(query)
            elif method == "method2":
                self.play_video_method_2(query)
            elif method == "method3":
                self.play_video_method_3(query)
            else:
                # Auto mode: Use method 1 (most reliable)
                self.play_video_method_1(query)
            
            return {
                "success": True,
                "message": f"✅ Now playing: {query}",
                "query": query
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error playing video: {str(e)}",
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
            webbrowser.open(url)
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


def create_youtube_automation(gui_automation):
    """
    Factory function to create YouTubeAutomation instance.
    
    Args:
        gui_automation: GUIAutomation instance
    
    Returns:
        YouTubeAutomation instance
    """
    return YouTubeAutomation(gui_automation)
