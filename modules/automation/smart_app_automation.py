"""
Smart App Automation with AI Analysis
Opens apps in fullscreen, takes screenshots, and provides AI-powered insights
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from modules.automation.fullscreen_automation import FullscreenAutomation
from modules.ai_features.screenshot_analysis import ScreenshotAnalyzer
import time


class SmartAppAutomation:
    """
    Intelligent app automation that:
    1. Opens apps in fullscreen
    2. Takes screenshots
    3. Analyzes them with AI
    4. Performs actions based on analysis
    """
    
    def __init__(self):
        """Initialize smart automation"""
        self.fullscreen = FullscreenAutomation()
        self.analyzer = ScreenshotAnalyzer()
        self.screenshots = []
    
    def automate_app(self, app_name: str, analysis_type: str = "general") -> dict:
        """
        Open app in fullscreen, screenshot, and analyze
        
        Args:
            app_name: Application to open
            analysis_type: Type of analysis ('general', 'errors', 'code', 'design', 'improvements')
        
        Returns:
            Dict with results
        """
        print(f"\n{'='*70}")
        print(f"🤖 SMART APP AUTOMATION: {app_name}")
        print(f"{'='*70}\n")
        
        # Step 1: Open app in fullscreen
        print("📱 Step 1: Opening app in fullscreen...")
        open_result = self.fullscreen.open_app_fullscreen(app_name)
        print(f"   {open_result['message']}")
        
        if not open_result['success']:
            return open_result
        
        # Step 2: Wait for app to stabilize
        print("\n⏳ Step 2: Waiting for app to load...")
        time.sleep(3)
        print("   ✅ App loaded")
        
        # Step 3: Take screenshot
        print("\n📸 Step 3: Capturing screenshot...")
        screenshot_path = f"screenshots/{app_name.replace(' ', '_')}_{int(time.time())}.png"
        os.makedirs("screenshots", exist_ok=True)
        
        screenshot_result = self.fullscreen.take_screenshot(screenshot_path)
        print(f"   {screenshot_result['message']}")
        
        if not screenshot_result['success']:
            return screenshot_result
        
        self.screenshots.append(screenshot_path)
        
        # Step 4: AI Analysis
        print(f"\n🧠 Step 4: AI Analysis ({analysis_type})...")
        analysis = self._perform_analysis(screenshot_path, analysis_type)
        print(f"   ✅ Analysis complete\n")
        
        # Step 5: Display results
        print(f"{'='*70}")
        print("📊 AI ANALYSIS RESULTS")
        print(f"{'='*70}\n")
        print(analysis)
        print(f"\n{'='*70}\n")
        
        return {
            "success": True,
            "app": app_name,
            "screenshot": screenshot_path,
            "analysis": analysis,
            "analysis_type": analysis_type
        }
    
    def _perform_analysis(self, screenshot_path: str, analysis_type: str) -> str:
        """Perform the appropriate type of analysis"""
        if analysis_type == "errors":
            return self.analyzer.find_errors(screenshot_path)
        elif analysis_type == "code":
            return self.analyzer.analyze_code(screenshot_path)
        elif analysis_type == "design":
            return self.analyzer.analyze_design(screenshot_path)
        elif analysis_type == "improvements":
            return self.analyzer.suggest_improvements(screenshot_path)
        elif analysis_type == "tips":
            return self.analyzer.get_quick_tips(screenshot_path)
        else:  # general
            return self.analyzer.analyze(screenshot_path, "Analyze this application screenshot in detail")
    
    def automate_with_actions(self, app_name: str, actions: list) -> dict:
        """
        Open app and perform a series of actions
        
        Args:
            app_name: Application to open
            actions: List of actions to perform [{"type": "type", "text": "..."}, {"type": "key", "key": "enter"}]
        
        Returns:
            Dict with results
        """
        print(f"\n🎬 Automating {app_name} with {len(actions)} actions...")
        
        # Open app
        open_result = self.fullscreen.open_app_fullscreen(app_name)
        if not open_result['success']:
            return open_result
        
        time.sleep(2)
        results = []
        
        # Perform each action
        for i, action in enumerate(actions, 1):
            print(f"\n▶️  Action {i}/{len(actions)}: {action['type']}")
            
            if action['type'] == 'type':
                result = self.fullscreen.type_text(action['text'])
            elif action['type'] == 'key':
                result = self.fullscreen.press_key(action['key'])
            elif action['type'] == 'hotkey':
                result = self.fullscreen.hotkey(*action['keys'])
            elif action['type'] == 'click':
                result = self.fullscreen.click_at(action['x'], action['y'])
            elif action['type'] == 'wait':
                time.sleep(action['seconds'])
                result = {"success": True, "message": f"Waited {action['seconds']}s"}
            elif action['type'] == 'screenshot':
                result = self.fullscreen.take_screenshot(action.get('filename'))
            else:
                result = {"success": False, "message": f"Unknown action: {action['type']}"}
            
            print(f"   {result['message']}")
            results.append(result)
            
            time.sleep(0.5)  # Small delay between actions
        
        return {
            "success": True,
            "app": app_name,
            "actions_completed": len([r for r in results if r['success']]),
            "total_actions": len(actions),
            "results": results
        }
    
    def continuous_monitoring(self, app_name: str, interval: int = 10, duration: int = 60):
        """
        Monitor an app continuously and analyze periodically
        
        Args:
            app_name: Application to monitor
            interval: Seconds between screenshots
            duration: Total monitoring duration
        """
        print(f"\n🔍 Starting continuous monitoring of {app_name}")
        print(f"   Interval: {interval}s | Duration: {duration}s\n")
        
        # Open app
        self.fullscreen.open_app_fullscreen(app_name)
        time.sleep(3)
        
        screenshots = []
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            # Take screenshot
            screenshot_path = f"screenshots/{app_name}_monitor_{int(time.time())}.png"
            result = self.fullscreen.take_screenshot(screenshot_path)
            
            if result['success']:
                screenshots.append(screenshot_path)
                print(f"📸 Captured: {screenshot_path}")
                
                # Quick analysis
                analysis = self.analyzer.get_quick_tips(screenshot_path)
                print(f"💡 Tips: {analysis[:100]}...\n")
            
            # Wait for next interval
            time.sleep(interval)
        
        print(f"\n✅ Monitoring complete! Captured {len(screenshots)} screenshots")
        return {
            "success": True,
            "screenshots": screenshots,
            "count": len(screenshots)
        }


def demo_browser_automation():
    """Example: Open browser in fullscreen and analyze"""
    automation = SmartAppAutomation()
    
    # Example 1: Open Chrome and analyze
    result = automation.automate_app("chrome", analysis_type="general")
    
    # Example 2: Open VS Code and check for errors
    # result = automation.automate_app("code", analysis_type="errors")
    
    return result


def demo_notepad_typing():
    """Example: Type in notepad"""
    automation = SmartAppAutomation()
    
    actions = [
        {"type": "type", "text": "Hello from AI automation!"},
        {"type": "key", "key": "enter"},
        {"type": "type", "text": "This was typed automatically."},
        {"type": "wait", "seconds": 1},
        {"type": "screenshot", "filename": "notepad_result.png"}
    ]
    
    result = automation.automate_with_actions("notepad", actions)
    return result


if __name__ == "__main__":
    print("=" * 70)
    print("🤖 SMART APP AUTOMATION WITH AI ANALYSIS")
    print("=" * 70)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python smart_app_automation.py <app_name> [analysis_type]")
        print("\nExamples:")
        print("  python smart_app_automation.py chrome")
        print("  python smart_app_automation.py code errors")
        print("  python smart_app_automation.py notepad improvements")
        print("\nAnalysis types:")
        print("  - general (default)")
        print("  - errors")
        print("  - code")
        print("  - design")
        print("  - improvements")
        print("  - tips")
        sys.exit(1)
    
    app_name = sys.argv[1]
    analysis_type = sys.argv[2] if len(sys.argv) > 2 else "general"
    
    automation = SmartAppAutomation()
    result = automation.automate_app(app_name, analysis_type)
    
    if result['success']:
        print("\n✨ Automation completed successfully!")
        print(f"📁 Screenshot saved: {result['screenshot']}")
    else:
        print(f"\n❌ Automation failed: {result['message']}")
