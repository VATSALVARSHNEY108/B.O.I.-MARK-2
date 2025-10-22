"""
Test WhatsApp Desktop Integration
Simple script to open WhatsApp Desktop directly
"""

from whatsapp_automation import create_whatsapp_automation

def main():
    print("=" * 60)
    print("WhatsApp Desktop Launcher")
    print("=" * 60)
    
    wa = create_whatsapp_automation()
    
    print("\nChoose an option:")
    print("1. Open WhatsApp Desktop")
    print("2. Open chat with a contact")
    print("3. Open chat with pre-filled message")
    print("4. Launch WhatsApp Desktop (alternative method)")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🚀 Opening WhatsApp Desktop...")
        result = wa.open_whatsapp_desktop()
        print(result["message"])
    
    elif choice == "2":
        phone = input("\nEnter phone number with country code (e.g., +1234567890): ").strip()
        print(f"\n🚀 Opening chat with {phone}...")
        result = wa.open_chat_in_desktop(phone)
        print(result["message"])
    
    elif choice == "3":
        phone = input("\nEnter phone number with country code (e.g., +1234567890): ").strip()
        message = input("Enter message to pre-fill: ").strip()
        print(f"\n🚀 Opening chat with {phone} and message...")
        result = wa.open_chat_in_desktop(phone, message)
        print(result["message"])
    
    elif choice == "4":
        print("\n🚀 Launching WhatsApp Desktop (alternative method)...")
        result = wa.launch_desktop_app()
        print(result["message"])
    
    else:
        print("\n❌ Invalid choice!")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
