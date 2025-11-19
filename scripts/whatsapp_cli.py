#!/usr/bin/env python3
"""
WhatsApp Messaging CLI
Command-line interface for sending WhatsApp messages
"""

import sys
import os
import json

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from modules.communication.whatsapp_automation import WhatsAppAutomation


def load_contacts():
    """Load contacts from contacts.json"""
    contacts_file = os.path.join(project_root, "data", "contacts.json")
    if os.path.exists(contacts_file):
        with open(contacts_file, 'r') as f:
            return json.load(f)
    return []


def find_contact(name):
    """Find contact by name"""
    contacts = load_contacts()
    name_lower = name.lower()
    
    for contact in contacts:
        if contact['name'].lower() == name_lower:
            return contact
    
    # Fuzzy match
    for contact in contacts:
        if name_lower in contact['name'].lower():
            return contact
    
    return None


def send_instant_message(phone_or_name, message):
    """Send instant WhatsApp message"""
    wa = WhatsAppAutomation()
    
    # Check if it's a contact name
    if not phone_or_name.startswith('+'):
        contact = find_contact(phone_or_name)
        if contact:
            print(f"📇 Found contact: {contact['name']}")
            phone = contact.get('phone')
            if not phone:
                print(f"❌ Contact {contact['name']} has no phone number")
                return
            phone_or_name = phone
        else:
            print(f"❌ Contact '{phone_or_name}' not found")
            print("💡 Use phone number with country code (e.g., +1234567890)")
            return
    
    result = wa.send_message_instantly(phone_or_name, message)
    print(result['message'])


def send_scheduled_message(phone_or_name, message, hour, minute):
    """Send scheduled WhatsApp message"""
    wa = WhatsAppAutomation()
    
    # Check if it's a contact name
    if not phone_or_name.startswith('+'):
        contact = find_contact(phone_or_name)
        if contact:
            print(f"📇 Found contact: {contact['name']}")
            phone = contact.get('phone')
            if not phone:
                print(f"❌ Contact {contact['name']} has no phone number")
                return
            phone_or_name = phone
        else:
            print(f"❌ Contact '{phone_or_name}' not found")
            return
    
    result = wa.send_message_scheduled(phone_or_name, message, int(hour), int(minute))
    print(result['message'])


def send_image(phone_or_name, image_path, caption=""):
    """Send image via WhatsApp"""
    wa = WhatsAppAutomation()
    
    # Check if it's a contact name
    if not phone_or_name.startswith('+'):
        contact = find_contact(phone_or_name)
        if contact:
            print(f"📇 Found contact: {contact['name']}")
            phone = contact.get('phone')
            if not phone:
                print(f"❌ Contact {contact['name']} has no phone number")
                return
            phone_or_name = phone
        else:
            print(f"❌ Contact '{phone_or_name}' not found")
            return
    
    result = wa.send_image(phone_or_name, image_path, caption)
    print(result['message'])


def send_to_group(group_id, message):
    """Send message to WhatsApp group"""
    wa = WhatsAppAutomation()
    result = wa.send_to_group_instantly(group_id, message)
    print(result['message'])


def list_contacts():
    """List all contacts"""
    contacts = load_contacts()
    if not contacts:
        print("ℹ️ No contacts found")
        return
    
    print(f"\n📇 Contacts ({len(contacts)}):\n")
    for i, contact in enumerate(contacts, 1):
        phone = contact.get('phone', 'N/A')
        email = contact.get('email', 'N/A')
        print(f"{i}. {contact['name']}")
        print(f"   📱 Phone: {phone}")
        print(f"   📧 Email: {email}")
        print()


def show_help():
    """Show help message"""
    print("""
📱 WhatsApp Messaging CLI

Usage:
    whatsapp_cli.py send <phone/name> <message>
    whatsapp_cli.py schedule <phone/name> <hour> <minute> <message>
    whatsapp_cli.py image <phone/name> <image_path> [caption]
    whatsapp_cli.py group <group_id> <message>
    whatsapp_cli.py contacts

Examples:
    # Send instant message
    whatsapp_cli.py send +1234567890 "Hello!"
    whatsapp_cli.py send "John Doe" "How are you?"
    
    # Schedule message for 3:30 PM
    whatsapp_cli.py schedule +1234567890 15 30 "Meeting reminder"
    
    # Send image with caption
    whatsapp_cli.py image +1234567890 photo.jpg "Check this out!"
    
    # Send to group
    whatsapp_cli.py group ABC123XYZ "Hello everyone!"
    
    # List contacts
    whatsapp_cli.py contacts

Notes:
    - Phone numbers must include country code (e.g., +1234567890)
    - You can use contact names from your contacts.json
    - Images require full path or relative path to image file
""")


def main():
    """Main CLI handler"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "send" or command == "message":
        if len(sys.argv) < 4:
            print("❌ Usage: whatsapp_cli.py send <phone/name> <message>")
            return
        phone_or_name = sys.argv[2]
        message = " ".join(sys.argv[3:])
        send_instant_message(phone_or_name, message)
    
    elif command == "schedule":
        if len(sys.argv) < 6:
            print("❌ Usage: whatsapp_cli.py schedule <phone/name> <hour> <minute> <message>")
            return
        phone_or_name = sys.argv[2]
        hour = sys.argv[3]
        minute = sys.argv[4]
        message = " ".join(sys.argv[5:])
        send_scheduled_message(phone_or_name, message, hour, minute)
    
    elif command == "image" or command == "photo":
        if len(sys.argv) < 4:
            print("❌ Usage: whatsapp_cli.py image <phone/name> <image_path> [caption]")
            return
        phone_or_name = sys.argv[2]
        image_path = sys.argv[3]
        caption = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""
        send_image(phone_or_name, image_path, caption)
    
    elif command == "group":
        if len(sys.argv) < 4:
            print("❌ Usage: whatsapp_cli.py group <group_id> <message>")
            return
        group_id = sys.argv[2]
        message = " ".join(sys.argv[3:])
        send_to_group(group_id, message)
    
    elif command == "contacts" or command == "list":
        list_contacts()
    
    elif command == "help" or command == "-h" or command == "--help":
        show_help()
    
    else:
        print(f"❌ Unknown command: {command}")
        show_help()


if __name__ == "__main__":
    main()
