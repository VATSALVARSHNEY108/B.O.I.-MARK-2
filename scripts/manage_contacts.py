#!/usr/bin/env python3
"""
Contact Manager for Phone Link
Add, edit, delete, and view contacts
"""

import sys
from modules.utilities.contact_manager import ContactManager
from modules.communication.phone_dialer import create_phone_dialer


class ContactCLI:
    """Command-line interface for contact management"""
    
    def __init__(self):
        self.contact_manager = ContactManager("data/contacts.json")
        self.phone_dialer = create_phone_dialer()
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "=" * 70)
        print("📇 CONTACT MANAGER")
        print("=" * 70)
        print()
        print("1. List all contacts")
        print("2. Add new contact")
        print("3. Edit contact")
        print("4. Delete contact")
        print("5. Search contacts")
        print("6. Call a contact")
        print("7. Import sample contacts")
        print("8. Exit")
        print()
    
    def list_contacts(self):
        """List all contacts"""
        contacts = self.contact_manager.list_contacts()
        
        if not contacts:
            print("\n📭 No contacts found. Add some contacts first!")
            return
        
        print("\n" + "=" * 70)
        print(f"📇 ALL CONTACTS ({len(contacts)} total)")
        print("=" * 70)
        
        for contact in sorted(contacts, key=lambda x: x['name']):
            print(f"\n👤 {contact['name']}")
            print(f"   📱 Phone: {contact.get('phone', 'N/A')}")
            print(f"   📧 Email: {contact.get('email', 'N/A')}")
    
    def add_contact(self):
        """Add a new contact"""
        print("\n" + "=" * 70)
        print("➕ ADD NEW CONTACT")
        print("=" * 70)
        
        name = input("\nEnter name: ").strip()
        if not name:
            print("❌ Name cannot be empty!")
            return
        
        phone = input("Enter phone number (with country code, e.g., +1234567890): ").strip()
        email = input("Enter email (optional): ").strip() or None
        
        if self.contact_manager.add_contact(name, phone, email):
            print(f"\n✅ Contact '{name}' added successfully!")
        else:
            print(f"\n❌ Failed to add contact '{name}'")
    
    def edit_contact(self):
        """Edit an existing contact"""
        print("\n" + "=" * 70)
        print("✏️  EDIT CONTACT")
        print("=" * 70)
        
        name = input("\nEnter contact name to edit: ").strip()
        
        contact = self.contact_manager.get_contact(name)
        if not contact:
            print(f"\n❌ Contact '{name}' not found!")
            return
        
        print(f"\nCurrent details:")
        print(f"  Name: {contact['name']}")
        print(f"  Phone: {contact.get('phone', 'N/A')}")
        print(f"  Email: {contact.get('email', 'N/A')}")
        print()
        
        phone = input("Enter new phone (press Enter to keep current): ").strip()
        email = input("Enter new email (press Enter to keep current): ").strip()
        
        phone = phone if phone else None
        email = email if email else None
        
        if self.contact_manager.update_contact(name, phone=phone, email=email):
            print(f"\n✅ Contact '{name}' updated successfully!")
        else:
            print(f"\n❌ Failed to update contact '{name}'")
    
    def delete_contact(self):
        """Delete a contact"""
        print("\n" + "=" * 70)
        print("🗑️  DELETE CONTACT")
        print("=" * 70)
        
        name = input("\nEnter contact name to delete: ").strip()
        
        contact = self.contact_manager.get_contact(name)
        if not contact:
            print(f"\n❌ Contact '{name}' not found!")
            return
        
        confirm = input(f"\n⚠️  Are you sure you want to delete '{contact['name']}'? (y/n): ").lower()
        
        if confirm == 'y':
            if self.contact_manager.delete_contact(name):
                print(f"\n✅ Contact '{name}' deleted successfully!")
            else:
                print(f"\n❌ Failed to delete contact '{name}'")
        else:
            print("\n❌ Deletion cancelled.")
    
    def search_contacts(self):
        """Search for contacts"""
        print("\n" + "=" * 70)
        print("🔍 SEARCH CONTACTS")
        print("=" * 70)
        
        query = input("\nEnter search query: ").strip()
        
        results = self.contact_manager.search_contacts(query)
        
        if not results:
            print(f"\n📭 No contacts found matching '{query}'")
            return
        
        print(f"\n📇 Found {len(results)} contact(s):")
        for contact in results:
            print(f"\n👤 {contact['name']}")
            print(f"   📱 Phone: {contact.get('phone', 'N/A')}")
            print(f"   📧 Email: {contact.get('email', 'N/A')}")
    
    def call_contact(self):
        """Call a contact using Phone Link"""
        print("\n" + "=" * 70)
        print("📞 CALL CONTACT")
        print("=" * 70)
        
        name = input("\nEnter contact name to call: ").strip()
        
        contact = self.contact_manager.get_contact(name)
        if not contact:
            print(f"\n❌ Contact '{name}' not found!")
            
            # Try to find similar contacts
            similar = self.contact_manager.search_contacts(name)
            if similar:
                print("\n🔍 Did you mean:")
                for c in similar[:3]:
                    print(f"   • {c['name']}")
            return
        
        if not contact.get('phone'):
            print(f"\n❌ No phone number for '{contact['name']}'!")
            return
        
        print(f"\n📞 Calling {contact['name']} at {contact['phone']}")
        print("⏳ Opening Phone Link...")
        
        result = self.phone_dialer.call_contact(name)
        
        print(f"\n{result['message']}")
    
    def import_samples(self):
        """Import sample contacts"""
        print("\n" + "=" * 70)
        print("📥 IMPORT SAMPLE CONTACTS")
        print("=" * 70)
        
        samples = [
            {"name": "Mom", "phone": "+1234567890", "email": "mom@example.com"},
            {"name": "Dad", "phone": "+1234567891", "email": "dad@example.com"},
            {"name": "John Smith", "phone": "+1234567892", "email": "john@example.com"},
            {"name": "Office", "phone": "+1234567893", "email": "office@example.com"},
            {"name": "Emergency", "phone": "911", "email": None},
        ]
        
        print(f"\nThis will add {len(samples)} sample contacts.")
        confirm = input("Continue? (y/n): ").lower()
        
        if confirm != 'y':
            print("❌ Import cancelled.")
            return
        
        added = 0
        for sample in samples:
            if self.contact_manager.add_contact(sample['name'], sample['phone'], sample['email']):
                added += 1
                print(f"✅ Added: {sample['name']}")
        
        print(f"\n✅ Imported {added} sample contacts!")
    
    def run(self):
        """Run the contact manager CLI"""
        while True:
            self.show_menu()
            choice = input("Select option (1-8): ").strip()
            
            if choice == '1':
                self.list_contacts()
            elif choice == '2':
                self.add_contact()
            elif choice == '3':
                self.edit_contact()
            elif choice == '4':
                self.delete_contact()
            elif choice == '5':
                self.search_contacts()
            elif choice == '6':
                self.call_contact()
            elif choice == '7':
                self.import_samples()
            elif choice == '8':
                print("\n👋 Goodbye!")
                break
            else:
                print("\n❌ Invalid option. Please select 1-8.")
            
            input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    cli = ContactCLI()
    
    # Check if command provided via arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "list":
            cli.list_contacts()
        elif command == "add":
            cli.add_contact()
        elif command == "call" and len(sys.argv) > 2:
            name = " ".join(sys.argv[2:])
            contact = cli.contact_manager.get_contact(name)
            if contact:
                result = cli.phone_dialer.call_contact(name)
                print(f"\n{result['message']}")
            else:
                print(f"\n❌ Contact '{name}' not found!")
        else:
            print("Usage:")
            print("  python manage_contacts.py        # Interactive mode")
            print("  python manage_contacts.py list   # List all contacts")
            print("  python manage_contacts.py add    # Add new contact")
            print("  python manage_contacts.py call <name>  # Call a contact")
    else:
        # Interactive mode
        cli.run()


if __name__ == "__main__":
    main()
