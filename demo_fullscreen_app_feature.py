"""
Demo: AI Screenshot Analysis with Fullscreen App Feature

This demo shows how to use the new fullscreen app feature that:
1. Takes a screenshot of the current screen
2. Uses AI to detect which app is visible
3. Opens that app in fullscreen mode
"""

from modules.ai_features.screenshot_analysis import (
    ScreenshotAnalyzer,
    detect_app_and_open_fullscreen,
    open_app_in_fullscreen,
    take_current_screenshot
)


def demo_basic_fullscreen():
    """Demo: Open a specific app in fullscreen"""
    print("=" * 60)
    print("DEMO 1: Open a specific app in fullscreen")
    print("=" * 60)
    
    print("\nOpening Chrome in fullscreen mode...")
    result = open_app_in_fullscreen("chrome")
    print(result)
    

def demo_auto_detect_and_open():
    """Demo: Auto-detect app from screenshot and open it"""
    print("\n" + "=" * 60)
    print("DEMO 2: Auto-detect app and open in fullscreen")
    print("=" * 60)
    
    analyzer = ScreenshotAnalyzer()
    
    print("\n📸 Taking screenshot of current screen...")
    screenshot_path = take_current_screenshot("screenshots/test_screen.png")
    print(f"Screenshot saved to: {screenshot_path}")
    
    print("\n🔍 Detecting app from screenshot and opening in fullscreen...")
    result = detect_app_and_open_fullscreen(screenshot_path)
    print(result)


def demo_manual_detection():
    """Demo: Manually detect app from screenshot"""
    print("\n" + "=" * 60)
    print("DEMO 3: Manual app detection from screenshot")
    print("=" * 60)
    
    analyzer = ScreenshotAnalyzer()
    
    print("\n📸 Taking screenshot...")
    screenshot_path = analyzer.take_screenshot("screenshots/manual_test.png")
    
    if screenshot_path:
        print(f"Screenshot saved to: {screenshot_path}")
        
        print("\n🔍 Detecting app...")
        app_info = analyzer.detect_app_from_screenshot(screenshot_path)
        
        print(f"\nDetection Results:")
        print(f"  App Name: {app_info.get('app_name', 'Unknown')}")
        print(f"  App Type: {app_info.get('app_type', 'unknown')}")
        print(f"  Is Fullscreen: {app_info.get('is_fullscreen', False)}")
        print(f"  Description: {app_info.get('description', 'N/A')[:100]}...")
        
        app_name = app_info.get('app_name', 'Unknown')
        if app_name != 'Unknown':
            print(f"\n✅ Opening {app_name} in fullscreen mode...")
            result = analyzer.open_app_fullscreen(app_name)
            print(result)


def demo_supported_apps():
    """Demo: Show all supported apps"""
    print("\n" + "=" * 60)
    print("DEMO 4: List of supported apps")
    print("=" * 60)
    
    supported_apps = [
        "chrome", "firefox", "edge", "safari",
        "notepad", "code", "calculator",
        "vlc", "spotify",
        "word", "excel", "powerpoint"
    ]
    
    print("\n📱 Supported Applications:")
    for i, app in enumerate(supported_apps, 1):
        print(f"  {i:2d}. {app.capitalize()}")
    
    print("\n💡 Usage Examples:")
    print("  - open_app_in_fullscreen('chrome')")
    print("  - open_app_in_fullscreen('notepad', force_fullscreen=True)")
    print("  - detect_app_and_open_fullscreen()  # Auto-detects from current screen")


if __name__ == "__main__":
    print("\n🚀 AI Fullscreen App Feature - Demo")
    print("=" * 60)
    print("\nThis feature uses AI to:")
    print("  1. Analyze screenshots to identify applications")
    print("  2. Open applications in fullscreen mode")
    print("  3. Detect if an app is already in fullscreen")
    print("=" * 60)
    
    import sys
    
    if len(sys.argv) > 1:
        demo_choice = sys.argv[1]
        
        if demo_choice == "1":
            demo_basic_fullscreen()
        elif demo_choice == "2":
            demo_auto_detect_and_open()
        elif demo_choice == "3":
            demo_manual_detection()
        elif demo_choice == "4":
            demo_supported_apps()
        else:
            print("\n❌ Invalid demo choice. Use: 1, 2, 3, or 4")
    else:
        print("\n📖 Available Demos:")
        print("\n  python demo_fullscreen_app_feature.py 1  - Open specific app")
        print("  python demo_fullscreen_app_feature.py 2  - Auto-detect and open")
        print("  python demo_fullscreen_app_feature.py 3  - Manual detection")
        print("  python demo_fullscreen_app_feature.py 4  - List supported apps")
        print("\nOr run all demos:")
        
        demo_supported_apps()
        
        print("\n" + "=" * 60)
        print("✅ Demo complete!")
        print("\n💡 Try running individual demos with the commands above")
