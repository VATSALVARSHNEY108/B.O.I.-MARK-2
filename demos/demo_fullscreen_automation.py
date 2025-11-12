#!/usr/bin/env python3
"""
🚀 Demo: Smart Fullscreen App Automation with AI Analysis
Shows how to use the new automation and screenshot analysis features
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from modules.automation.smart_app_automation import SmartAppAutomation
from modules.automation.fullscreen_automation import FullscreenAutomation
from modules.ai_features.screenshot_analysis import ScreenshotAnalyzer


def demo_1_simple_app_analysis():
    """Demo 1: Open app in fullscreen and analyze"""
    print("\n" + "="*70)
    print("DEMO 1: Open App in Fullscreen & Analyze")
    print("="*70)
    
    automation = SmartAppAutomation()
    
    # Open Notepad (or TextEdit on Mac) in fullscreen and analyze
    app = "notepad" if os.name == 'nt' else "TextEdit"
    result = automation.automate_app(app, analysis_type="general")
    
    if result['success']:
        print("\n✅ Success!")
        print(f"Screenshot: {result['screenshot']}")
        print(f"\nAI Analysis:\n{result['analysis']}")
    else:
        print(f"\n❌ Failed: {result['message']}")


def demo_2_screenshot_analysis_only():
    """Demo 2: Analyze an existing screenshot"""
    print("\n" + "="*70)
    print("DEMO 2: AI Screenshot Analysis")
    print("="*70)
    
    analyzer = ScreenshotAnalyzer()
    
    # If you have a screenshot, analyze it
    screenshot_path = "screenshots/sample.png"
    
    if os.path.exists(screenshot_path):
        print(f"\nAnalyzing: {screenshot_path}")
        
        # General analysis
        print("\n📊 General Analysis:")
        result = analyzer.analyze(screenshot_path)
        print(result)
        
        # Find errors
        print("\n🔍 Error Detection:")
        errors = analyzer.find_errors(screenshot_path)
        print(errors)
        
        # Get tips
        print("\n💡 Quick Tips:")
        tips = analyzer.get_quick_tips(screenshot_path)
        print(tips)
    else:
        print(f"\n⚠️ No screenshot found at {screenshot_path}")
        print("Take a screenshot first or use Demo 1 to create one")


def demo_3_fullscreen_automation():
    """Demo 3: Fullscreen automation with actions"""
    print("\n" + "="*70)
    print("DEMO 3: Fullscreen Automation with Actions")
    print("="*70)
    
    automation = SmartAppAutomation()
    
    app = "notepad" if os.name == 'nt' else "TextEdit"
    
    # Define automation actions
    actions = [
        {"type": "wait", "seconds": 2},
        {"type": "type", "text": "🤖 AUTOMATED BY AI"},
        {"type": "key", "key": "enter"},
        {"type": "key", "key": "enter"},
        {"type": "type", "text": "This text was typed automatically!"},
        {"type": "key", "key": "enter"},
        {"type": "type", "text": "Powered by VATSAL AI Desktop Automation"},
        {"type": "wait", "seconds": 1},
        {"type": "screenshot", "filename": "automated_result.png"}
    ]
    
    print(f"\nAutomating {app} with {len(actions)} actions...")
    result = automation.automate_with_actions(app, actions)
    
    if result['success']:
        print(f"\n✅ Completed {result['actions_completed']}/{result['total_actions']} actions")
    else:
        print(f"\n❌ Failed: {result.get('message', 'Unknown error')}")


def demo_4_code_analysis():
    """Demo 4: Open code editor and analyze code"""
    print("\n" + "="*70)
    print("DEMO 4: Open Code Editor & Analyze Code")
    print("="*70)
    
    automation = SmartAppAutomation()
    
    # Try VS Code or other code editors
    for app in ["code", "sublime_text", "atom", "notepad++"]:
        print(f"\nTrying to open {app}...")
        result = automation.automate_app(app, analysis_type="code")
        
        if result['success']:
            print(f"\n✅ Analyzed {app}!")
            print(f"\nCode Analysis:\n{result['analysis']}")
            break
    else:
        print("\n⚠️ No code editor found. Install VS Code or another editor.")


def demo_5_error_detection():
    """Demo 5: Open browser and check for errors"""
    print("\n" + "="*70)
    print("DEMO 5: Open Browser & Check for Errors")
    print("="*70)
    
    automation = SmartAppAutomation()
    
    # Try different browsers
    for browser in ["chrome", "firefox", "safari", "edge"]:
        print(f"\nTrying {browser}...")
        result = automation.automate_app(browser, analysis_type="errors")
        
        if result['success']:
            print(f"\n✅ Analyzed {browser}!")
            print(f"\nError Detection:\n{result['analysis']}")
            break
    else:
        print("\n⚠️ No browser found.")


def interactive_demo():
    """Interactive demo menu"""
    print("\n" + "="*70)
    print("🤖 SMART FULLSCREEN AUTOMATION - INTERACTIVE DEMO")
    print("="*70)
    print("\nChoose a demo:")
    print("1. Simple App Analysis (Notepad)")
    print("2. Screenshot Analysis Only")
    print("3. Fullscreen Automation with Actions")
    print("4. Code Editor Analysis")
    print("5. Browser Error Detection")
    print("6. Run All Demos")
    print("0. Exit")
    
    choice = input("\nEnter choice (0-6): ").strip()
    
    demos = {
        "1": demo_1_simple_app_analysis,
        "2": demo_2_screenshot_analysis_only,
        "3": demo_3_fullscreen_automation,
        "4": demo_4_code_analysis,
        "5": demo_5_error_detection,
    }
    
    if choice == "6":
        for demo_func in demos.values():
            demo_func()
            input("\nPress Enter to continue to next demo...")
    elif choice in demos:
        demos[choice]()
    elif choice == "0":
        print("\n👋 Goodbye!")
        return
    else:
        print("\n❌ Invalid choice")


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("🚀 SMART FULLSCREEN APP AUTOMATION")
    print("AI-Powered Screenshot Analysis & Automation")
    print("="*70)
    
    if len(sys.argv) > 1:
        demo_choice = sys.argv[1]
        if demo_choice == "1":
            demo_1_simple_app_analysis()
        elif demo_choice == "2":
            demo_2_screenshot_analysis_only()
        elif demo_choice == "3":
            demo_3_fullscreen_automation()
        elif demo_choice == "4":
            demo_4_code_analysis()
        elif demo_choice == "5":
            demo_5_error_detection()
        else:
            print(f"\n❌ Unknown demo: {demo_choice}")
            print("Usage: python demo_fullscreen_automation.py [1-5]")
    else:
        interactive_demo()


if __name__ == "__main__":
    main()
