#!/usr/bin/env python3
"""
Demo: Enhanced Modern GUI for VATSAL AI
Shows off the new beautiful interface
"""

import sys
import os

# Setup paths
workspace_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(workspace_dir, 'modules')
sys.path.insert(0, workspace_dir)
sys.path.insert(0, modules_dir)
sys.path.insert(0, os.path.join(modules_dir, 'core'))

def main():
    """Run the enhanced GUI demo"""
    print("=" * 70)
    print("✨ ENHANCED MODERN GUI DEMO ✨")
    print("=" * 70)
    print()
    print("🎨 Features:")
    print("   • Modern dark theme with beautiful colors")
    print("   • Dashboard with real-time statistics")
    print("   • Quick actions organized by category")
    print("   • AI chat interface for natural language")
    print("   • Automation center for workflows")
    print("   • Analytics and insights dashboard")
    print("   • Settings panel for customization")
    print()
    print("🚀 Navigation:")
    print("   • Use sidebar to switch between sections")
    print("   • Hover over buttons for effects")
    print("   • Click quick action cards to execute")
    print("   • Chat interface accepts natural language")
    print()
    print("💡 Tips:")
    print("   • Start with Dashboard for overview")
    print("   • Try Quick Actions for common tasks")
    print("   • Explore all sections via sidebar")
    print("   • Check Settings for customization")
    print()
    print("=" * 70)
    print("Opening Enhanced GUI...")
    print("=" * 70)
    print()
    
    try:
        from modules.core.enhanced_gui import main as gui_main
        gui_main()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
