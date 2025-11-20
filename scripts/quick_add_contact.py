#!/usr/bin/env python3
"""
Quick script to add a WhatsApp contact
Usage: python quick_add_contact.py "Name" "+PhoneNumber"
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.whatsapp_contact_manager import WhatsAppContactManager

def main():
    if len(sys.argv) < 3:
        print("=" * 60)
        print("QUICK ADD WHATSAPP CONTACT")
        print("=" * 60)
        print("\nUsage:")
        print(f"  python {sys.argv[0]} \"Name\" \"+PhoneNumber\"")
        print("\nExamples:")
        print(f"  python {sys.argv[0]} \"Vatsal Varshney\" \"+911234567890\"")
        print(f"  python {sys.argv[0]} \"John Doe\" \"+1234567890\"")
        print("\nNOTE: Phone number MUST include country code with + prefix")
        print("=" * 60)
        return
    
    name = sys.argv[1]
    phone = sys.argv[2]
    
    manager = WhatsAppContactManager()
    
    print(f"\n📱 Adding WhatsApp contact...")
    print(f"  Name: {name}")
    print(f"  Phone: {phone}")
    
    if manager.add_contact(name, phone):
        print(f"\n✅ Contact added successfully!")
        print(f"\nYou can now use:")
        print(f"  Voice: \"WhatsApp {name} your message here\"")
        print(f"  Or: \"Send WhatsApp to {name} saying hello\"")
    else:
        print(f"\n❌ Failed to add contact")
        print(f"\nTips:")
        print(f"  - Phone must start with + and country code")
        print(f"  - Contact name might already exist (use different name or update)")
        print(f"  - Check if phone format is correct: +[country][number]")

if __name__ == "__main__":
    main()
