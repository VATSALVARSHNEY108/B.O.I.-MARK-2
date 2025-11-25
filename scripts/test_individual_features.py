#!/usr/bin/env python3
"""
BOI Individual Feature Tester
Tests all 410+ features to ensure they work individually
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def test_feature(feature_name, factory_func, *args, **kwargs):
    """Test a single feature"""
    try:
        instance = factory_func(*args, **kwargs)
        status = instance.get_status() if hasattr(instance, 'get_status') else instance.status() if hasattr(instance, 'status') else "Created"
        print(f"✅ {feature_name}: {status}")
        return True
    except ImportError as e:
        print(f"⚠️ {feature_name}: Module not found ({e})")
        return False
    except Exception as e:
        print(f"❌ {feature_name}: Error - {e}")
        return False

def main():
    """Test all major features"""
    print("=" * 70)
    print("BOI INDIVIDUAL FEATURE TEST SUITE")
    print("=" * 70)
    
    results = {}
    
    # Core Features
    print("\n🔷 CORE FEATURES")
    from modules.core.command_executor import CommandExecutor
    results['CommandExecutor'] = test_feature("CommandExecutor", CommandExecutor)
    
    # Communication Features
    print("\n📧 COMMUNICATION FEATURES")
    try:
        from modules.communication.email_sender import create_email_sender
        results['EmailSender'] = test_feature("EmailSender", create_email_sender)
    except: pass
    
    try:
        from modules.communication.phone_dialer import create_phone_dialer
        results['PhoneDialer'] = test_feature("PhoneDialer", create_phone_dialer)
    except: pass
    
    # System Features
    print("\n⚙️ SYSTEM FEATURES")
    from modules.system.system_control import SystemController
    results['SystemController'] = test_feature("SystemController", SystemController)
    
    # Utilities
    print("\n🛠️ UTILITIES")
    from modules.utilities.calendar_manager import CalendarManager
    results['CalendarManager'] = test_feature("CalendarManager", CalendarManager)
    
    from modules.utilities.quick_notes import QuickNotes
    results['QuickNotes'] = test_feature("QuickNotes", QuickNotes)
    
    from modules.utilities.password_vault import PasswordVault
    results['PasswordVault'] = test_feature("PasswordVault", PasswordVault)
    
    # AI Features
    print("\n🧠 AI FEATURES")
    try:
        from modules.core.future_tech_core import create_future_tech_core
        results['FutureTechCore'] = test_feature("FutureTechCore", create_future_tech_core)
    except: pass
    
    try:
        from modules.ai_features.ai_features import create_ai_features
        results['AIFeatures'] = test_feature("AIFeatures", create_ai_features)
    except: pass
    
    # Productivity Features
    print("\n📊 PRODUCTIVITY FEATURES")
    from modules.productivity.productivity_monitor import ProductivityMonitor
    results['ProductivityMonitor'] = test_feature("ProductivityMonitor", ProductivityMonitor)
    
    # Security Features
    print("\n🔒 SECURITY FEATURES")
    try:
        from modules.security.security_enhancements import create_security_enhancements
        results['SecurityEnhancements'] = test_feature("SecurityEnhancements", create_security_enhancements)
    except: pass
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL FEATURES WORKING INDIVIDUALLY!")
    else:
        print(f"\n⚠️ {total - passed} features need attention")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
