#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.core.modern_gui import main

if __name__ == "__main__":
    print("🚀 Launching Modern VATSAL GUI...")
    print("📦 Loading eye-comforting interface with 3D blocks...")
    main()
