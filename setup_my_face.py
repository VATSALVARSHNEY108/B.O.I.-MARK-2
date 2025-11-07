#!/usr/bin/env python3
"""
Quick Face Enrollment Script
Run this to set up your face for VATSAL security
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from security.enhanced_biometric_auth import BiometricAuthenticationSystem

def quick_face_setup():
    """Simple face enrollment"""
    print("=" * 60)
    print("🔐 VATSAL FACE SETUP")
    print("=" * 60)
    print()
    
    # Get user info
    print("Let's set up your face for security!")
    print()
    user_id = input("Your username (e.g., john): ").strip()
    user_name = input("Your full name (e.g., John Doe): ").strip()
    
    if not user_id or not user_name:
        print("❌ Please provide both username and name!")
        return
    
    # Initialize system
    print("\n🔄 Initializing face recognition system...")
    bio_auth = BiometricAuthenticationSystem()
    
    # Instructions
    print("\n📸 READY TO CAPTURE YOUR FACE")
    print("=" * 60)
    print("Instructions:")
    print("1. Make sure you have good lighting")
    print("2. Sit 2-3 feet from your camera")
    print("3. Look directly at the camera")
    print("4. Slowly move your head (left, right, up, down)")
    print("5. The system will capture 30 face samples")
    print()
    print("Press ENTER when ready (or Ctrl+C to cancel)...")
    input()
    
    # Enroll face
    print("\n📷 Starting face capture...")
    print("(A camera window will open - look at the green rectangle)")
    print()
    
    result = bio_auth.enroll_face(user_id, user_name, num_samples=30)
    
    # Show result
    print("\n" + "=" * 60)
    if result["success"]:
        print("✅ SUCCESS! Your face is now enrolled!")
        print(f"   Samples captured: {result['samples_captured']}")
        print(f"   User: {user_name}")
        print()
        print("Your face data is saved in: biometric_data/faces/")
        print()
        print("🔐 You can now use face authentication!")
        print()
        print("Next steps:")
        print("  - Test with: python demo_face_security.py (Option 2)")
        print("  - Or use in your code: bio_auth.authenticate_face()")
    else:
        print("❌ FAILED!")
        print(f"   Error: {result['message']}")
        print()
        print("Common issues:")
        print("  - No camera found (connect webcam)")
        print("  - Camera in use by another app (close it)")
        print("  - Running on cloud server (needs local machine)")
    print("=" * 60)

if __name__ == "__main__":
    try:
        quick_face_setup()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nNote: This requires a webcam and works on local machines")
        print("(Windows/Mac/Linux). Cloud environments like Replit")
        print("don't have camera access.")
