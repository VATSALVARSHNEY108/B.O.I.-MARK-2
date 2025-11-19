#!/usr/bin/env python3
"""
WhatsApp Contact Manager
Manage contacts for easy WhatsApp messaging by name
"""

import sys
import os
import json
import csv
from typing import List, Dict, Optional
from datetime import datetime

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


class WhatsAppContactManager:
    """Manages WhatsApp contacts for easy messaging by name"""
    
    def __init__(self, contacts_file: Optional[str] = None):
        """
        Initialize contact manager
        
        Args:
            contacts_file: Path to contacts JSON file (default: data/contacts.json)
        """
        if contacts_file is None:
            contacts_file = os.path.join(project_root, "data", "contacts.json")
        
        self.contacts_file = contacts_file
        self.contacts_dir = os.path.dirname(contacts_file)
        
        if not os.path.exists(self.contacts_dir):
            os.makedirs(self.contacts_dir)
        
        self.contacts = self._load_contacts()
    
    def _load_contacts(self) -> List[Dict]:
        """Load contacts from JSON file"""
        if not os.path.exists(self.contacts_file):
            return []
        
        try:
            with open(self.contacts_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, dict) and data and isinstance(list(data.values())[0], dict):
                print("📦 Migrating old contact format to new format...")
                contacts = []
                for key, value in data.items():
                    if isinstance(value, dict):
                        contact = {
                            "name": value.get('name', key),
                            "phone": value.get('phone', ''),
                            "email": value.get('email', ''),
                            "notes": value.get('notes', ''),
                            "created": datetime.now().isoformat(),
                            "updated": datetime.now().isoformat()
                        }
                        contacts.append(contact)
                
                self.contacts = contacts
                self._save_contacts()
                print(f"✅ Migrated {len(contacts)} contacts to new format")
                return contacts
            
            elif isinstance(data, list):
                return data
            
            return []
        except Exception as e:
            print(f"⚠️  Error loading contacts: {e}")
            return []
    
    def _save_contacts(self):
        """Save contacts to JSON file"""
        try:
            with open(self.contacts_file, 'w', encoding='utf-8') as f:
                json.dump(self.contacts, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving contacts: {e}")
            return False
    
    def add_contact(self, name: str, phone: str, email: str = "", notes: str = "", **kwargs) -> bool:
        """
        Add a new contact
        
        Args:
            name: Contact name
            phone: Phone number with country code (e.g., +1234567890)
            email: Email address (optional)
            notes: Additional notes (optional)
            **kwargs: Additional custom fields
        
        Returns:
            Success status
        """
        if not name or not phone:
            print("❌ Name and phone number are required")
            return False
        
        if not phone.startswith('+'):
            print("❌ Phone number must include country code (e.g., +1234567890)")
            return False
        
        if self.find_contact(name):
            print(f"⚠️  Contact '{name}' already exists. Use edit_contact to update.")
            return False
        
        contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "notes": notes,
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat()
        }
        
        contact.update(kwargs)
        
        self.contacts.append(contact)
        
        if self._save_contacts():
            print(f"✅ Contact '{name}' added successfully")
            return True
        
        return False
    
    def edit_contact(self, name: str, **updates) -> bool:
        """
        Edit an existing contact
        
        Args:
            name: Contact name to edit
            **updates: Fields to update (phone, email, notes, etc.)
        
        Returns:
            Success status
        """
        contact = self.find_contact(name)
        
        if not contact:
            print(f"❌ Contact '{name}' not found")
            return False
        
        for key, value in updates.items():
            if key == "name":
                print("⚠️  Use rename_contact to change the contact name")
                continue
            contact[key] = value
        
        contact["updated"] = datetime.now().isoformat()
        
        if self._save_contacts():
            print(f"✅ Contact '{name}' updated successfully")
            return True
        
        return False
    
    def rename_contact(self, old_name: str, new_name: str) -> bool:
        """
        Rename a contact
        
        Args:
            old_name: Current contact name
            new_name: New contact name
        
        Returns:
            Success status
        """
        if self.find_contact(new_name):
            print(f"❌ Contact '{new_name}' already exists")
            return False
        
        contact = self.find_contact(old_name)
        
        if not contact:
            print(f"❌ Contact '{old_name}' not found")
            return False
        
        contact["name"] = new_name
        contact["updated"] = datetime.now().isoformat()
        
        if self._save_contacts():
            print(f"✅ Contact renamed from '{old_name}' to '{new_name}'")
            return True
        
        return False
    
    def delete_contact(self, name: str) -> bool:
        """
        Delete a contact
        
        Args:
            name: Contact name to delete
        
        Returns:
            Success status
        """
        contact = self.find_contact(name)
        
        if not contact:
            print(f"❌ Contact '{name}' not found")
            return False
        
        self.contacts.remove(contact)
        
        if self._save_contacts():
            print(f"✅ Contact '{name}' deleted successfully")
            return True
        
        return False
    
    def find_contact(self, name: str) -> Optional[Dict]:
        """
        Find contact by name (case-insensitive, fuzzy matching)
        
        Args:
            name: Contact name to search
        
        Returns:
            Contact dict or None
        """
        name_lower = name.lower()
        
        for contact in self.contacts:
            if contact['name'].lower() == name_lower:
                return contact
        
        for contact in self.contacts:
            if name_lower in contact['name'].lower():
                return contact
        
        return None
    
    def search_contacts(self, query: str) -> List[Dict]:
        """
        Search contacts by name, phone, or email
        
        Args:
            query: Search query
        
        Returns:
            List of matching contacts
        """
        query_lower = query.lower()
        results = []
        
        for contact in self.contacts:
            if (query_lower in contact['name'].lower() or
                query_lower in contact.get('phone', '').lower() or
                query_lower in contact.get('email', '').lower()):
                results.append(contact)
        
        return results
    
    def list_contacts(self, sort_by: str = "name") -> List[Dict]:
        """
        List all contacts
        
        Args:
            sort_by: Field to sort by (name, phone, created, updated)
        
        Returns:
            Sorted list of contacts
        """
        if sort_by in ["name", "phone", "email"]:
            return sorted(self.contacts, key=lambda x: x.get(sort_by, "").lower())
        elif sort_by in ["created", "updated"]:
            return sorted(self.contacts, key=lambda x: x.get(sort_by, ""))
        
        return self.contacts
    
    def get_contact_phone(self, name: str) -> Optional[str]:
        """
        Get phone number for a contact
        
        Args:
            name: Contact name
        
        Returns:
            Phone number or None
        """
        contact = self.find_contact(name)
        return contact.get('phone') if contact else None
    
    def import_from_csv(self, csv_file: str) -> Dict[str, int]:
        """
        Import contacts from CSV file
        
        Args:
            csv_file: Path to CSV file with columns: name, phone, email (optional)
        
        Returns:
            Dict with counts: added, skipped, errors
        """
        if not os.path.exists(csv_file):
            print(f"❌ CSV file not found: {csv_file}")
            return {"added": 0, "skipped": 0, "errors": 0}
        
        stats = {"added": 0, "skipped": 0, "errors": 0}
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    name = row.get('name', '').strip()
                    phone = row.get('phone', '').strip()
                    email = row.get('email', '').strip()
                    notes = row.get('notes', '').strip()
                    
                    if not name or not phone:
                        stats["skipped"] += 1
                        continue
                    
                    if self.find_contact(name):
                        stats["skipped"] += 1
                        continue
                    
                    if self.add_contact(name, phone, email, notes):
                        stats["added"] += 1
                    else:
                        stats["errors"] += 1
            
            print(f"\n📊 Import Summary:")
            print(f"   ✅ Added: {stats['added']}")
            print(f"   ⏭️  Skipped: {stats['skipped']}")
            print(f"   ❌ Errors: {stats['errors']}")
            
            return stats
        
        except Exception as e:
            print(f"❌ Error importing CSV: {e}")
            return stats
    
    def export_to_csv(self, csv_file: str, include_all_fields: bool = False) -> bool:
        """
        Export contacts to CSV file
        
        Args:
            csv_file: Path to output CSV file
            include_all_fields: Include all custom fields (default: False)
        
        Returns:
            Success status
        """
        try:
            if include_all_fields:
                if not self.contacts:
                    headers = ["name", "phone", "email", "notes"]
                else:
                    headers = list(self.contacts[0].keys())
            else:
                headers = ["name", "phone", "email", "notes"]
            
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(self.contacts)
            
            print(f"✅ Exported {len(self.contacts)} contacts to {csv_file}")
            return True
        
        except Exception as e:
            print(f"❌ Error exporting CSV: {e}")
            return False
    
    def create_batch_csv(self, output_file: str, contact_names: List[str] = None, template_type: str = "basic"):
        """
        Create batch CSV from existing contacts
        
        Args:
            output_file: Path to output CSV file
            contact_names: List of contact names to include (None = all)
            template_type: "basic", "personalized", or "image"
        """
        try:
            contacts_to_export = []
            
            if contact_names:
                for name in contact_names:
                    contact = self.find_contact(name)
                    if contact:
                        contacts_to_export.append(contact)
            else:
                contacts_to_export = self.contacts
            
            if not contacts_to_export:
                print("❌ No contacts to export")
                return False
            
            if template_type == "basic":
                headers = ["phone", "name", "message"]
                rows = [[c['phone'], c['name'], f"Hi {c['name']}!"] for c in contacts_to_export]
            
            elif template_type == "personalized":
                headers = ["phone", "name", "email"]
                rows = [[c['phone'], c['name'], c.get('email', '')] for c in contacts_to_export]
            
            elif template_type == "image":
                headers = ["phone", "name", "caption"]
                rows = [[c['phone'], c['name'], f"Hi {c['name']}!"] for c in contacts_to_export]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
            
            print(f"✅ Created batch CSV with {len(contacts_to_export)} contacts: {output_file}")
            return True
        
        except Exception as e:
            print(f"❌ Error creating batch CSV: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get contact statistics"""
        total = len(self.contacts)
        with_email = sum(1 for c in self.contacts if c.get('email'))
        with_notes = sum(1 for c in self.contacts if c.get('notes'))
        
        return {
            "total": total,
            "with_email": with_email,
            "with_notes": with_notes
        }


def main():
    """CLI interface for contact management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="WhatsApp Contact Manager")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    add_parser = subparsers.add_parser('add', help='Add a new contact')
    add_parser.add_argument('name', help='Contact name')
    add_parser.add_argument('phone', help='Phone number with country code')
    add_parser.add_argument('--email', '-e', default='', help='Email address')
    add_parser.add_argument('--notes', '-n', default='', help='Notes')
    
    edit_parser = subparsers.add_parser('edit', help='Edit a contact')
    edit_parser.add_argument('name', help='Contact name')
    edit_parser.add_argument('--phone', '-p', help='New phone number')
    edit_parser.add_argument('--email', '-e', help='New email')
    edit_parser.add_argument('--notes', '-n', help='New notes')
    
    rename_parser = subparsers.add_parser('rename', help='Rename a contact')
    rename_parser.add_argument('old_name', help='Current name')
    rename_parser.add_argument('new_name', help='New name')
    
    delete_parser = subparsers.add_parser('delete', help='Delete a contact')
    delete_parser.add_argument('name', help='Contact name')
    
    search_parser = subparsers.add_parser('search', help='Search contacts')
    search_parser.add_argument('query', help='Search query')
    
    list_parser = subparsers.add_parser('list', help='List all contacts')
    list_parser.add_argument('--sort', '-s', default='name', choices=['name', 'phone', 'created', 'updated'], help='Sort by field')
    
    import_parser = subparsers.add_parser('import', help='Import contacts from CSV')
    import_parser.add_argument('csv_file', help='Path to CSV file')
    
    export_parser = subparsers.add_parser('export', help='Export contacts to CSV')
    export_parser.add_argument('csv_file', help='Path to output CSV file')
    export_parser.add_argument('--all-fields', action='store_true', help='Include all fields')
    
    batch_parser = subparsers.add_parser('create-batch', help='Create batch CSV from contacts')
    batch_parser.add_argument('output_file', help='Output CSV file')
    batch_parser.add_argument('--names', '-n', nargs='+', help='Contact names to include')
    batch_parser.add_argument('--type', '-t', choices=['basic', 'personalized', 'image'], default='basic', help='Template type')
    
    stats_parser = subparsers.add_parser('stats', help='Show contact statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = WhatsAppContactManager()
    
    if args.command == 'add':
        manager.add_contact(args.name, args.phone, args.email, args.notes)
    
    elif args.command == 'edit':
        updates = {}
        if args.phone:
            updates['phone'] = args.phone
        if args.email is not None:
            updates['email'] = args.email
        if args.notes is not None:
            updates['notes'] = args.notes
        
        if updates:
            manager.edit_contact(args.name, **updates)
        else:
            print("⚠️  No updates provided")
    
    elif args.command == 'rename':
        manager.rename_contact(args.old_name, args.new_name)
    
    elif args.command == 'delete':
        confirm = input(f"Are you sure you want to delete '{args.name}'? (y/n): ")
        if confirm.lower() == 'y':
            manager.delete_contact(args.name)
    
    elif args.command == 'search':
        results = manager.search_contacts(args.query)
        if results:
            print(f"\n🔍 Found {len(results)} contact(s):\n")
            for i, contact in enumerate(results, 1):
                print(f"{i}. {contact['name']}")
                print(f"   📱 Phone: {contact.get('phone', 'N/A')}")
                print(f"   📧 Email: {contact.get('email', 'N/A')}")
                if contact.get('notes'):
                    print(f"   📝 Notes: {contact['notes']}")
                print()
        else:
            print(f"ℹ️  No contacts found matching '{args.query}'")
    
    elif args.command == 'list':
        contacts = manager.list_contacts(args.sort)
        if contacts:
            print(f"\n📇 Contacts ({len(contacts)}):\n")
            for i, contact in enumerate(contacts, 1):
                print(f"{i}. {contact['name']}")
                print(f"   📱 Phone: {contact.get('phone', 'N/A')}")
                print(f"   📧 Email: {contact.get('email', 'N/A')}")
                if contact.get('notes'):
                    print(f"   📝 Notes: {contact['notes']}")
                print()
        else:
            print("ℹ️  No contacts found")
    
    elif args.command == 'import':
        manager.import_from_csv(args.csv_file)
    
    elif args.command == 'export':
        manager.export_to_csv(args.csv_file, args.all_fields)
    
    elif args.command == 'create-batch':
        manager.create_batch_csv(args.output_file, args.names, args.type)
    
    elif args.command == 'stats':
        stats = manager.get_stats()
        print(f"\n📊 Contact Statistics:\n")
        print(f"   Total Contacts: {stats['total']}")
        print(f"   With Email: {stats['with_email']}")
        print(f"   With Notes: {stats['with_notes']}")
        print()


if __name__ == "__main__":
    main()
