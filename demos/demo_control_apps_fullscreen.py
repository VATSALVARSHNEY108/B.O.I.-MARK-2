"""
Demo: Control Apps in Fullscreen Mode

This demo shows how to ensure apps are opened in fullscreen 
BEFORE controlling them (Notepad, Browser, YouTube, etc.)
"""

from modules.ai_features.screenshot_analysis import (
    control_notepad_fullscreen,
    control_browser_fullscreen,
    control_youtube_fullscreen,
    ensure_app_fullscreen
)
import time


def demo_control_notepad():
    """Demo: Open Notepad in fullscreen before controlling it"""
    print("=" * 60)
    print("DEMO 1: Control Notepad in Fullscreen")
    print("=" * 60)
    
    print("\n📝 Opening Notepad in fullscreen mode...")
    result = control_notepad_fullscreen()
    print(result)
    
    print("\n✅ Now you can control Notepad (type, save, etc.)")
    print("   The app is already open and in fullscreen mode!")
    
    # Example: Now you could use pyautogui to type in Notepad
    time.sleep(1)
    print("\n💡 You can now use automation to:")
    print("   - Type text with pyautogui.write()")
    print("   - Save files with Ctrl+S")
    print("   - Do other Notepad operations")


def demo_control_browser():
    """Demo: Open browser in fullscreen before controlling it"""
    print("\n" + "=" * 60)
    print("DEMO 2: Control Browser in Fullscreen")
    print("=" * 60)
    
    browser = input("\nWhich browser? (chrome/firefox/edge/safari) [chrome]: ").strip() or "chrome"
    
    print(f"\n🌐 Opening {browser} in fullscreen mode...")
    result = control_browser_fullscreen(browser)
    print(result)
    
    print("\n✅ Now you can control the browser")
    print("   The browser is ready for automation!")
    
    time.sleep(1)
    print("\n💡 You can now:")
    print("   - Navigate to URLs")
    print("   - Fill forms")
    print("   - Click buttons")
    print("   - Scrape data")


def demo_control_youtube():
    """Demo: Open YouTube in fullscreen browser"""
    print("\n" + "=" * 60)
    print("DEMO 3: Open YouTube in Fullscreen Browser")
    print("=" * 60)
    
    browser = input("\nWhich browser? (chrome/firefox/edge) [chrome]: ").strip() or "chrome"
    youtube_url = input("YouTube URL [https://youtube.com]: ").strip() or "https://youtube.com"
    
    print(f"\n📺 Opening YouTube in {browser} fullscreen...")
    result = control_youtube_fullscreen(browser, youtube_url)
    print(result)
    
    print("\n✅ YouTube is now open in fullscreen!")
    print("   Ready for video automation!")
    
    time.sleep(1)
    print("\n💡 You can now:")
    print("   - Search for videos")
    print("   - Play videos")
    print("   - Control playback")
    print("   - Navigate YouTube")


def demo_control_any_app():
    """Demo: Control any supported app in fullscreen"""
    print("\n" + "=" * 60)
    print("DEMO 4: Control Any App in Fullscreen")
    print("=" * 60)
    
    print("\n📱 Supported apps:")
    apps = [
        "notepad", "chrome", "firefox", "edge",
        "calculator", "code", "spotify", "vlc"
    ]
    
    for i, app in enumerate(apps, 1):
        print(f"   {i}. {app}")
    
    app_name = input("\nEnter app name: ").strip().lower()
    
    if not app_name:
        print("❌ No app specified")
        return
    
    print(f"\n🚀 Opening {app_name} in fullscreen...")
    result = ensure_app_fullscreen(app_name)
    print(result)
    
    print(f"\n✅ {app_name} is ready for automation!")


def demo_workflow_example():
    """Demo: Complete workflow with fullscreen control"""
    print("\n" + "=" * 60)
    print("DEMO 5: Complete Automation Workflow")
    print("=" * 60)
    
    print("\n📋 Workflow Example: Write a note in Notepad")
    print("\nStep 1: Ensure Notepad is fullscreen...")
    result = control_notepad_fullscreen()
    print(f"   {result}")
    
    time.sleep(2)
    
    print("\nStep 2: Now you can type in Notepad...")
    print("   (In real automation, you'd use pyautogui.write() here)")
    
    print("\nStep 3: Save the file...")
    print("   (In real automation, you'd use pyautogui.hotkey('ctrl', 's'))")
    
    print("\n✅ Workflow complete!")
    print("   The app was fullscreen throughout the entire process")


def show_usage_examples():
    """Show code usage examples"""
    print("\n" + "=" * 60)
    print("CODE USAGE EXAMPLES")
    print("=" * 60)
    
    examples = """
# Example 1: Control Notepad
from modules.ai_features.screenshot_analysis import control_notepad_fullscreen
import pyautogui

# First, open Notepad in fullscreen
control_notepad_fullscreen()

# Then control it
pyautogui.write("Hello, this is automated text!")
pyautogui.hotkey('ctrl', 's')  # Save

# Example 2: Control Browser
from modules.ai_features.screenshot_analysis import control_browser_fullscreen

# First, open browser in fullscreen
control_browser_fullscreen("chrome")

# Then navigate and control
# (use selenium or pyautogui here)

# Example 3: Open YouTube
from modules.ai_features.screenshot_analysis import control_youtube_fullscreen

# Open YouTube in fullscreen
control_youtube_fullscreen("chrome", "https://youtube.com/watch?v=dQw4w9WgXcQ")

# Then control playback
# (use selenium or pyautogui here)

# Example 4: Any App
from modules.ai_features.screenshot_analysis import ensure_app_fullscreen

# Open Calculator in fullscreen
ensure_app_fullscreen("calculator")

# Open VS Code in fullscreen
ensure_app_fullscreen("code")

# Open Spotify in fullscreen
ensure_app_fullscreen("spotify")
"""
    
    print(examples)


if __name__ == "__main__":
    print("\n🎯 Control Apps in Fullscreen - Demo")
    print("=" * 60)
    print("\nThis feature ensures apps are FULLSCREEN before controlling them")
    print("Perfect for automation where you need full screen access!")
    print("=" * 60)
    
    import sys
    
    if len(sys.argv) > 1:
        demo_choice = sys.argv[1]
        
        if demo_choice == "1":
            demo_control_notepad()
        elif demo_choice == "2":
            demo_control_browser()
        elif demo_choice == "3":
            demo_control_youtube()
        elif demo_choice == "4":
            demo_control_any_app()
        elif demo_choice == "5":
            demo_workflow_example()
        elif demo_choice == "examples":
            show_usage_examples()
        else:
            print("\n❌ Invalid choice. Use: 1, 2, 3, 4, 5, or 'examples'")
    else:
        print("\n📖 Available Demos:")
        print("\n  python demo_control_apps_fullscreen.py 1  - Control Notepad")
        print("  python demo_control_apps_fullscreen.py 2  - Control Browser")
        print("  python demo_control_apps_fullscreen.py 3  - Open YouTube")
        print("  python demo_control_apps_fullscreen.py 4  - Control Any App")
        print("  python demo_control_apps_fullscreen.py 5  - Complete Workflow")
        print("  python demo_control_apps_fullscreen.py examples  - Show code examples")
        
        print("\n" + "=" * 60)
        print("Quick Examples:")
        print("=" * 60)
        
        show_usage_examples()
        
        print("\n✅ Ready to control apps in fullscreen!")
        print("\n💡 Run any demo above to see it in action")
