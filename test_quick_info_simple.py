#!/usr/bin/env python3
"""
Simple Direct Test of Quick Info Module
"""

import sys
from pathlib import Path

# Add modules to path
workspace_dir = Path(__file__).parent
sys.path.insert(0, str(workspace_dir))
sys.path.insert(0, str(workspace_dir / 'modules'))

from modules.utilities.quick_info import QuickInfo

def test_quick_info():
    """Test all QuickInfo methods"""
    print("=" * 70)
    print("🧪 TESTING QUICK INFO MODULE")
    print("=" * 70)
    
    quick_info = QuickInfo()
    
    tests = [
        ("Current Time", lambda: quick_info.get_current_time()),
        ("Current Date", lambda: quick_info.get_current_date()),
        ("Day Info", lambda: quick_info.get_day_info()),
        ("Week Info", lambda: quick_info.get_week_info()),
        ("Month Info", lambda: quick_info.get_month_info()),
        ("Year Info", lambda: quick_info.get_year_info()),
        ("Date & Time", lambda: quick_info.get_date_and_time()),
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*70}")
        print(f"✅ Testing: {test_name}")
        print(f"{'='*70}")
        try:
            result = test_func()
            print(result)
            print("✅ SUCCESS")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("🎉 All Tests Complete!")
    print("=" * 70)

if __name__ == "__main__":
    test_quick_info()
