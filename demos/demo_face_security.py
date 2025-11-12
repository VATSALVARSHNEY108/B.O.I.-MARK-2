#!/usr/bin/env python3
"""
🔐 VATSAL Face Detection Security Demo
Step-by-step demonstration of biometric face authentication
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from security.enhanced_biometric_auth import BiometricAuthenticationSystem

def print_header():
    """Print demo header"""
    print("=" * 70)
    print("🔐 VATSAL FACE DETECTION SECURITY SYSTEM")
    print("=" * 70)
    print()

def print_menu():
    """Print main menu"""
    print("\n📋 MENU:")
    print("1. 👤 Enroll Your Face (Register)")
    print("2. 🔐 Authenticate with Face (Login)")
    print("3. 📊 View Enrolled Users")
    print("4. 📜 View Authentication Log")
    print("5. ⚙️  Security Settings")
    print("6. ❌ Exit")
    print()

def enroll_user(bio_auth):
    """Enroll a new user"""
    print("\n" + "=" * 70)
    print("👤 FACE ENROLLMENT")
    print("=" * 70)
    print()
    
    user_id = input("Enter User ID (e.g., john123): ").strip()
    if not user_id:
        print("❌ User ID cannot be empty!")
        return
    
    user_name = input("Enter Full Name (e.g., John Doe): ").strip()
    if not user_name:
        print("❌ Name cannot be empty!")
        return
    
    print("\n📸 INSTRUCTIONS:")
    print("1. Make sure you have good lighting")
    print("2. Look directly at the camera")
    print("3. Move your head slightly (left, right, up, down)")
    print("4. The system will capture 30 face samples")
    print("5. Press 'Q' anytime to cancel")
    print()
    
    input("Press ENTER when ready to start...")
    
    result = bio_auth.enroll_face(user_id, user_name, num_samples=30)
    
    if result["success"]:
        print(f"\n✅ SUCCESS!")
        print(f"   {result['message']}")
        print(f"   Samples captured: {result['samples_captured']}")
    else:
        print(f"\n❌ FAILED!")
        print(f"   {result['message']}")

def authenticate_user(bio_auth):
    """Authenticate using face recognition"""
    print("\n" + "=" * 70)
    print("🔐 FACE AUTHENTICATION")
    print("=" * 70)
    print()
    
    print("📸 INSTRUCTIONS:")
    print("1. Look directly at the camera")
    print("2. Stay still for a moment")
    print("3. Press 'Q' to cancel")
    print()
    
    confidence = input("Confidence threshold (default 70, lower = stricter): ").strip()
    confidence = int(confidence) if confidence else 70
    
    input("Press ENTER when ready to authenticate...")
    
    result = bio_auth.authenticate_face(confidence_threshold=confidence)
    
    if result["success"]:
        print(f"\n✅ AUTHENTICATION SUCCESSFUL!")
        print(f"   Welcome: {result['user_name']}")
        print(f"   User ID: {result['user_id']}")
        print(f"   Confidence: {result['confidence']:.2f}")
    else:
        print(f"\n❌ AUTHENTICATION FAILED!")
        print(f"   {result['message']}")

def view_enrolled_users(bio_auth):
    """View all enrolled users"""
    print("\n" + "=" * 70)
    print("👥 ENROLLED USERS")
    print("=" * 70)
    print()
    
    users = bio_auth.get_enrolled_users()
    
    if not users:
        print("No users enrolled yet.")
        return
    
    for i, user in enumerate(users, 1):
        print(f"\n{i}. {user['user_name']}")
        print(f"   ID: {user['user_id']}")
        print(f"   Enrolled: {user['enrollment_date'][:10]}")
        print(f"   Face: {'✓' if user['face_enrolled'] else '✗'}")
        print(f"   Fingerprint: {'✓' if user['fingerprint_enrolled'] else '✗'}")

def view_auth_log(bio_auth):
    """View authentication log"""
    print("\n" + "=" * 70)
    print("📜 AUTHENTICATION LOG (Last 10 attempts)")
    print("=" * 70)
    print()
    
    log = bio_auth.get_auth_log(limit=10)
    
    if not log:
        print("No authentication attempts yet.")
        return
    
    for entry in log:
        status = "✅" if entry['success'] else "❌"
        print(f"\n{status} {entry['timestamp'][:19]}")
        print(f"   User: {entry['user_id']}")
        print(f"   Method: {entry['method']}")
        print(f"   Details: {entry.get('details', 'N/A')}")

def security_settings(bio_auth):
    """Configure security settings"""
    print("\n" + "=" * 70)
    print("⚙️  SECURITY SETTINGS")
    print("=" * 70)
    print()
    
    config = bio_auth.config
    
    print("Current Settings:")
    print(f"1. Face Recognition: {'✓ Enabled' if config['face_recognition_enabled'] else '✗ Disabled'}")
    print(f"2. Confidence Threshold: {config['confidence_threshold']} (lower = stricter)")
    print(f"3. Session Timeout: {config['session_timeout_minutes']} minutes")
    print(f"4. Max Failed Attempts: {config['max_failed_attempts']}")
    print(f"5. Lockout Duration: {config['lockout_duration_minutes']} minutes")
    print()
    
    print("What would you like to change?")
    print("1. Toggle Face Recognition")
    print("2. Change Confidence Threshold")
    print("3. Change Session Timeout")
    print("4. Back to Main Menu")
    print()
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        config['face_recognition_enabled'] = not config['face_recognition_enabled']
        bio_auth._save_config()
        status = "Enabled" if config['face_recognition_enabled'] else "Disabled"
        print(f"✅ Face Recognition {status}")
    
    elif choice == "2":
        threshold = input("Enter new threshold (30-100, recommended 70): ").strip()
        if threshold.isdigit() and 30 <= int(threshold) <= 100:
            config['confidence_threshold'] = int(threshold)
            bio_auth._save_config()
            print(f"✅ Confidence threshold set to {threshold}")
        else:
            print("❌ Invalid threshold")
    
    elif choice == "3":
        timeout = input("Enter timeout in minutes (1-1440): ").strip()
        if timeout.isdigit() and 1 <= int(timeout) <= 1440:
            config['session_timeout_minutes'] = int(timeout)
            bio_auth._save_config()
            print(f"✅ Session timeout set to {timeout} minutes")
        else:
            print("❌ Invalid timeout")

def main():
    """Main demo loop"""
    print_header()
    
    print("🔄 Initializing Biometric Authentication System...")
    bio_auth = BiometricAuthenticationSystem()
    print("✅ System Ready!")
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            enroll_user(bio_auth)
        
        elif choice == "2":
            authenticate_user(bio_auth)
        
        elif choice == "3":
            view_enrolled_users(bio_auth)
        
        elif choice == "4":
            view_auth_log(bio_auth)
        
        elif choice == "5":
            security_settings(bio_auth)
        
        elif choice == "6":
            print("\n👋 Goodbye!")
            print("=" * 70)
            break
        
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
