#!/usr/bin/env python3
"""
Test script for Phone Dialer functionality
Demonstrates how to make phone calls using VATSAL
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules', 'communication'))

from phone_dialer import create_phone_dialer

def test_phone_dialer():
    """Test the phone dialer functionality"""
    print("=" * 70)
    print("📞 VATSAL Phone Dialer Test")
    print("=" * 70)
    
    dialer = create_phone_dialer()
    
    print("\n✅ Phone dialer initialized")
    print(f"📡 Demo mode: {dialer.demo_mode}")
    print(f"☎️  Twilio available: {dialer.twilio_available}")
    
    print("\n" + "=" * 70)
    print("Test 1: Making a test call")
    print("=" * 70)
    
    result = dialer.dial_call(
        phone_number="+1234567890",
        message="This is a test call from VATSAL AI Assistant. Have a great day!"
    )
    
    print(f"\nResult: {result}")
    
    print("\n" + "=" * 70)
    print("Test 2: Quick dial with number normalization")
    print("=" * 70)
    
    result2 = dialer.dial_call(
        phone_number="123-456-7890",
        message="Testing number normalization. This call is automated."
    )
    
    print(f"\nResult: {result2}")
    
    print("\n" + "=" * 70)
    print("Test 3: View call history")
    print("=" * 70)
    
    history = dialer.get_call_history()
    print(f"\nCall history ({len(history)} calls):")
    for i, call in enumerate(history, 1):
        print(f"\n  Call {i}:")
        print(f"    Phone: {call['phone']}")
        print(f"    Status: {call['status']}")
        print(f"    Time: {call['timestamp']}")
    
    print("\n" + "=" * 70)
    print("✅ Phone Dialer Test Complete!")
    print("=" * 70)
    
    if dialer.demo_mode:
        print("\n💡 NOTE: Currently running in DEMO MODE")
        print("   To make real calls, set up Twilio integration:")
        print("   1. Get Twilio credentials from https://www.twilio.com")
        print("   2. Set environment variables:")
        print("      - TWILIO_ACCOUNT_SID")
        print("      - TWILIO_AUTH_TOKEN")
        print("      - TWILIO_PHONE_NUMBER")
        print("\n   Or use the Twilio integration in Replit for automatic setup!")
    
    return result

if __name__ == "__main__":
    test_phone_dialer()
