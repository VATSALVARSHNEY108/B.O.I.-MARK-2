#!/usr/bin/env python3
"""
VATSAL AI Desktop Automation Controller - CLI Launcher
======================================================

This is the main entry point for running VATSAL AI in command-line mode.
Perfect for cloud environments like Replit where GUI display is not available.

For GUI desktop interfaces, run locally with:
- python -m modules.core.gui_app (original GUI)
- python -m modules.core.enhanced_gui (modern dark theme GUI)

Note: GUI interfaces require X server and won't work in headless cloud environments.
"""

import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from modules.core.main import main

if __name__ == "__main__":
    print("🚀 Launching VATSAL AI Desktop Automation Controller (CLI Mode)")
    print("=" * 70)
    main()
