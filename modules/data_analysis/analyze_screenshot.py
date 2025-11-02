#!/usr/bin/env python3
"""
📸 Screenshot Analyzer - Simple & Fast!

Usage:
  python analyze_screenshot.py <screenshot.png>
  
Example:
  python analyze_screenshot.py my_screen.png
"""

import sys
import os
from modules.monitoring.smart_screen_monitor import SmartScreenMonitor

def analyze_screenshot(image_path: str):
    """Analyze a screenshot and print results"""
    
    # Check API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY not set!")
        print("\n📝 Quick Setup:")
        print("   1. Go to Replit Secrets (🔒 icon)")
        print("   2. Add: GEMINI_API_KEY = your_key")
        print("   3. Get key: https://aistudio.google.com/app/apikey")
        return
    
    # Check file exists
    if not os.path.exists(image_path):
        print(f"❌ Error: File not found: {image_path}")
        print("\n💡 Upload your screenshot to Replit first!")
        return
    
    print("=" * 70)
    print("📸 SCREENSHOT ANALYZER")
    print("=" * 70)
    print(f"\n📁 File: {image_path}")
    print(f"📊 Size: {os.path.getsize(image_path):,} bytes")
    
    # Analyze
    monitor = SmartScreenMonitor()
    print("\n🤖 Analyzing with AI Vision...")
    print("-" * 70)
    
    result = monitor.analyze_uploaded_screenshot(image_path, focus="general")
    
    if result["success"]:
        print("\n✅ ANALYSIS COMPLETE\n")
        print(result['analysis'])
        print("\n" + "-" * 70)
        print(f"⏰ Analyzed at: {result['timestamp']}")
    else:
        print("\n❌ ANALYSIS FAILED\n")
        print(result['message'])
    
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n📸 Screenshot Analyzer")
        print("\nUsage:")
        print("  python analyze_screenshot.py <screenshot_file>")
        print("\nExample:")
        print("  python analyze_screenshot.py my_screen.png")
        print("\n💡 Upload your screenshot to Replit, then run this command!")
    else:
        analyze_screenshot(sys.argv[1])
