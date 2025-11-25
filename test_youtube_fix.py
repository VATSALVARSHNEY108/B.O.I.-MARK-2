#!/usr/bin/env python3
"""
Quick test for YouTube video clicking fix
"""

from modules.web.selenium_web_automator import SeleniumWebAutomator

def test_youtube_playing():
    print("=" * 60)
    print("Testing YouTube Video Click Fix")
    print("=" * 60)
    
    automator = SeleniumWebAutomator(headless=False)
    
    query = "python tutorial"
    print(f"\n🔍 Testing search and play for: '{query}'")
    
    result = automator.youtube_play_video(query)
    
    if result.get("success"):
        print(f"\n✅ SUCCESS: {result.get('message')}")
        print("\n🎉 The YouTube clicking fix is working!")
        input("\nPress Enter to close the browser...")
    else:
        print(f"\n❌ FAILED: {result.get('error')}")
    
    automator.close_browser()
    print("\n✅ Browser closed")

if __name__ == "__main__":
    test_youtube_playing()
