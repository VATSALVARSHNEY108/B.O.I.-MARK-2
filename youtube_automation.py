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
        Method 1: Open YouTube homepage, search, then click first video with mouse
        Most reliable across different browsers - uses mouse click instead of keyboard
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
        time.sleep(4)
        
        # Click on first video thumbnail using mouse
        print(f"  🎯 Clicking first video thumbnail...")
        # Typical position of first video thumbnail on YouTube search results
        # This is approximate and works for most screen resolutions
        self.gui.click_at_position(400, 400)
        
        return True
    
    def play_video_method_2(self, query):
        """
        Method 2: Direct search URL, then mouse click on first video
        Faster and more reliable - uses mouse instead of keyboard navigation
        """
        print(f"  🎬 Method 2: Using direct search URL...")
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        webbrowser.open(search_url)
        time.sleep(4)
        
        print(f"  🎯 Clicking first video...")
        # Click on the first video thumbnail
        self.gui.click_at_position(400, 400)
        
        return True
    
    def play_video_method_3(self, query):
        """
        Method 3: Search URL with mouse click at alternative position
        Opens search results and clicks at a different screen position
        """
        print(f"  🎬 Method 3: Using search with alternative click position...")
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        webbrowser.open(search_url)
        time.sleep(4)
        
        # Click at alternative position for first video
        print(f"  🎯 Clicking first video (alternative position)...")
        # Try clicking slightly to the right in case of different layouts
        self.gui.click_at_position(500, 350)
        
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
    
    def play_first_result(self, wait_time=3, use_mouse=True):
        """
        Play the first video from current YouTube search results page.
        This assumes you're already on a YouTube search results page.
        
        Args:
            wait_time: Seconds to wait for page to load (default: 3)
            use_mouse: Use mouse click instead of keyboard (default: True)
        
        Returns:
            Success status and message
        """
        try:
            print(f"  ⏳ Waiting {wait_time}s for page to load...")
            time.sleep(wait_time)
            
            if use_mouse:
                print(f"  🎯 Clicking first video with mouse...")
                # Click on first video thumbnail position
                self.gui.click_at_position(400, 400)
            else:
                print(f"  🎯 Navigating to first video with keyboard...")
                # Fallback: use keyboard navigation but skip voice search button
                # Usually voice search is one of the early tab stops, so we skip more
                for i in range(8):  # Increased from 6 to skip voice search
                    self.gui.press_key('tab')
                    time.sleep(0.3)
                
                # Play the video
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
    
    def search_and_play(self, query, wait_time=3, use_mouse=True):
        """
        Search YouTube and immediately play the first result.
        Combines search_only() and play_first_result().
        
        Args:
            query: Search query
            wait_time: Seconds to wait after search (default: 3)
            use_mouse: Use mouse click instead of keyboard (default: True)
        
        Returns:
            Success status and message
        """
        try:
            # First, perform the search
            print(f"  🔍 Searching YouTube for: {query}")
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            webbrowser.open(search_url)
            
            # Then play first result
            result = self.play_first_result(wait_time, use_mouse)
            
            if result["success"]:
                result["message"] = f"✅ Searched and playing: {query}"
                result["query"] = query
            
            return result
        
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
