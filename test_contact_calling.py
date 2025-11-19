#!/usr/bin/env python3
"""
Test Contact-Based Calling
Demonstrates calling contacts by name
"""

from modules.communication.phone_dialer import create_phone_dialer
from modules.utilities.contact_manager import ContactManager
from ai_phone_link_controller import AIPhoneLinkController

print("=" * 70)
print("📇 CONTACT-BASED CALLING TEST")
print("=" * 70)
print()

# Initialize
contact_manager = ContactManager()
phone_dialer = create_phone_dialer()
ai_controller = AIPhoneLinkController()

# Check contacts
contacts = contact_manager.list_contacts()
print(f"📋 You have {len(contacts)} contacts in your system.")
print()

if len(contacts) == 0:
    print("⚠️  No contacts found! Let's add some...")
    print()
    
    # Add sample contacts
    samples = [
        {"name": "Mom", "phone": "+1234567890"},
        {"name": "Dad", "phone": "+1234567891"},
        {"name": "John", "phone": "+1234567892"},
    ]
    
    for sample in samples:
        contact_manager.add_contact(sample['name'], sample['phone'])
        print(f"✅ Added: {sample['name']} - {sample['phone']}")
    
    print()
    contacts = contact_manager.list_contacts()

# Show contacts
print("📇 Your Contacts:")
print("-" * 70)
for contact in contacts:
    print(f"  • {contact['name']:20} → {contact.get('phone', 'No phone')}")
print()

# Test 1: Call by name (direct method)
print("=" * 70)
print("TEST 1: Call Contact by Name (Direct)")
print("=" * 70)
print()

if contacts:
    test_contact = contacts[0]['name']
    print(f"Calling: {test_contact}")
    print()
    
    result = phone_dialer.call_contact(test_contact.lower())
    print(f"✅ {result['message']}")
    if 'contact_name' in result:
        print(f"   Contact: {result['contact_name']}")
    print()

# Test 2: Call by name (AI controller)
print("=" * 70)
print("TEST 2: Call Contact Using AI Commands")
print("=" * 70)
print()

ai_commands = [
    "Call Mom",
    "Call Dad",
    "Call John",
]

for cmd in ai_commands:
    print(f"💬 Command: '{cmd}'")
    result = ai_controller.process_command(cmd)
    print(f"   Result: {result.get('message', 'Done')}")
    print()

# Test 3: Mixed commands (names and numbers)
print("=" * 70)
print("TEST 3: Mixed Commands (Names and Numbers)")
print("=" * 70)
print()

mixed_commands = [
    "Call Mom",
    "Call +1234567890",
    "Dial John",
]

for cmd in mixed_commands:
    print(f"💬 Command: '{cmd}'")
    result = ai_controller.process_command(cmd)
    print(f"   Result: {result.get('message', 'Done')}")
    print()

# Test 4: Contact not found
print("=" * 70)
print("TEST 4: Contact Not Found Handling")
print("=" * 70)
print()

print("💬 Command: 'Call Unknown Person'")
result = ai_controller.process_command("Call Unknown Person")
print(f"   Result: {result.get('message', 'Done')}")
print()

# Show usage examples
print("=" * 70)
print("✅ TESTS COMPLETE!")
print("=" * 70)
print()
print("📚 How to Use:")
print()
print("1. Add contacts:")
print("   python manage_contacts.py")
print()
print("2. Call by name:")
print("   python ai_phone_link_controller.py 'Call Mom'")
print()
print("3. Or use interactive mode:")
print("   python ai_phone_link_controller.py")
print("   Then type: Call Mom")
print()
print("=" * 70)
