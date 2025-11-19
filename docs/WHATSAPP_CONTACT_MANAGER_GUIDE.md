# WhatsApp Contact Manager Guide

Complete guide to managing contacts for easy WhatsApp messaging by name instead of phone numbers.

## Overview

The WhatsApp Contact Manager allows you to:
- **Save contacts** with names, phone numbers, emails, and notes
- **Message by name** instead of remembering phone numbers
- **Organize contacts** with search, edit, rename, and delete features
- **Import/export** contacts from/to CSV files
- **Create batch CSVs** directly from saved contacts

## Quick Start

### Add a Contact

**Using Batch File:**
```batch
batch_scripts\automation\whatsapp_contacts.bat
# Select option 1: Add New Contact
```

**Using Python CLI:**
```bash
python scripts/whatsapp_contact_manager.py add "John Doe" "+1234567890" --email "john@email.com" --notes "Friend"
```

### Message a Contact by Name

```bash
# Using WhatsApp CLI
python scripts/whatsapp_cli.py send "John Doe" "Hello!"

# Or use the batch automation menu
batch_scripts\automation\whatsapp_contacts.bat
# Select option 10: Quick Message by Name
```

## Features

### 1. Contact Management

#### Add Contact
Add a new contact with name, phone, email, and notes:
```bash
python scripts/whatsapp_contact_manager.py add "Alice Johnson" "+1234567890" --email "alice@email.com" --notes "Work colleague"
```

**Required:**
- Name (e.g., "John Doe", "Mom", "Office")
- Phone with country code (e.g., +1234567890)

**Optional:**
- Email address
- Notes

#### Edit Contact
Update contact information:
```bash
python scripts/whatsapp_contact_manager.py edit "John Doe" --phone "+0987654321" --email "newemail@example.com"
```

#### Rename Contact
Change a contact's name:
```bash
python scripts/whatsapp_contact_manager.py rename "John Doe" "John Smith"
```

#### Delete Contact
Remove a contact:
```bash
python scripts/whatsapp_contact_manager.py delete "John Doe"
```

### 2. Search & List

#### List All Contacts
```bash
python scripts/whatsapp_contact_manager.py list
```

Sort by name (default), phone, created, or updated date:
```bash
python scripts/whatsapp_contact_manager.py list --sort created
```

#### Search Contacts
Search by name, phone, or email:
```bash
python scripts/whatsapp_contact_manager.py search "john"
```

### 3. Import/Export

#### Import from CSV
Import multiple contacts from a CSV file:

**CSV Format:**
```csv
name,phone,email,notes
John Doe,+1234567890,john@email.com,Friend from school
Jane Smith,+0987654321,jane@email.com,Work colleague
```

**Import Command:**
```bash
python scripts/whatsapp_contact_manager.py import contacts.csv
```

#### Export to CSV
Export all contacts to CSV:
```bash
python scripts/whatsapp_contact_manager.py export my_contacts.csv
```

Export with all custom fields:
```bash
python scripts/whatsapp_contact_manager.py export my_contacts.csv --all-fields
```

### 4. Create Batch CSV

Create a batch messaging CSV directly from your saved contacts:

**All Contacts:**
```bash
python scripts/whatsapp_contact_manager.py create-batch batch_file.csv
```

**Specific Contacts:**
```bash
python scripts/whatsapp_contact_manager.py create-batch batch_file.csv --names "John Doe" "Jane Smith" "Bob Johnson"
```

**Template Types:**
- `basic` - phone, name, message columns
- `personalized` - phone, name, email columns
- `image` - phone, name, caption columns

```bash
python scripts/whatsapp_contact_manager.py create-batch batch_file.csv --type personalized
```

### 5. Statistics

View contact statistics:
```bash
python scripts/whatsapp_contact_manager.py stats
```

Shows:
- Total contacts
- Contacts with email
- Contacts with notes

## Integration with WhatsApp Batch Automation

The Contact Manager seamlessly integrates with the WhatsApp Batch Automation system:

### 1. Access from Batch Menu

```batch
batch_scripts\automation\whatsapp_batch_automation.bat
# Select option 7: Manage Contacts
```

This opens the full contact manager interface.

### 2. Use Contact Names in CSV Files

Your batch CSV files can now use **contact names** instead of phone numbers in the "phone" column:

**Before (phone numbers only):**
```csv
phone,name,message
+1234567890,John Doe,Hello John!
+0987654321,Jane Smith,Hi Jane!
```

**Now (contact names work too):**
```csv
phone,name,message
John Doe,,Hello John!
Jane Smith,,Hi Jane!
Mom,,Hi Mom! How are you?
```

The system automatically:
- Resolves contact names to phone numbers
- Fills in missing names from contact database
- Falls back to phone numbers if contact not found

### 3. Create Batch CSV from Contacts

Instead of manually creating CSV files:

1. Add contacts using Contact Manager
2. Create batch CSV from contacts:
   - Option 9 in WhatsApp Contacts menu
   - Or: `python scripts/whatsapp_contact_manager.py create-batch output.csv`
3. Use the generated CSV for batch messaging

## Use Cases

### Use Case 1: Personal Messaging

**Scenario:** Message friends and family by name

```bash
# Add contacts once
python scripts/whatsapp_contact_manager.py add "Mom" "+1234567890"
python scripts/whatsapp_contact_manager.py add "Dad" "+0987654321"
python scripts/whatsapp_contact_manager.py add "Sister" "+1122334455"

# Then message by name anytime
python scripts/whatsapp_cli.py send "Mom" "Hi Mom! Just checking in."
python scripts/whatsapp_cli.py send "Dad" "Happy birthday Dad!"
```

### Use Case 2: Business Communications

**Scenario:** Manage business contacts and send targeted campaigns

```bash
# Import business contacts
python scripts/whatsapp_contact_manager.py import clients.csv

# Create batch CSV for specific clients
python scripts/whatsapp_contact_manager.py create-batch promo_campaign.csv --names "Client A" "Client B" "Client C"

# Send batch messages with template
python scripts/whatsapp_batch.py send promo_campaign.csv --template "Hi {name}, special offer just for you!"
```

### Use Case 3: Event Invitations

**Scenario:** Send event invitations to saved contacts

```bash
# Create batch CSV from all contacts
python scripts/whatsapp_contact_manager.py create-batch event_invites.csv

# Send invitations with template
python scripts/whatsapp_batch.py send event_invites.csv --template "Hi {name}! You're invited to our event on Dec 15th. RSVP: [link]"
```

## Contact Data Storage

Contacts are stored in `data/contacts.json` in the following format:

```json
[
  {
    "name": "John Doe",
    "phone": "+1234567890",
    "email": "john@email.com",
    "notes": "Friend from school",
    "created": "2025-11-19T10:30:00",
    "updated": "2025-11-19T10:30:00"
  },
  {
    "name": "Jane Smith",
    "phone": "+0987654321",
    "email": "jane@email.com",
    "notes": "Work colleague",
    "created": "2025-11-19T11:00:00",
    "updated": "2025-11-19T11:00:00"
  }
]
```

**Backup Recommendation:** Regularly backup `data/contacts.json`

## Best Practices

### Naming Contacts
- Use clear, memorable names
- Examples: "Mom", "Dr. Smith", "Office Main", "Emergency"
- Avoid special characters that might cause issues

### Phone Numbers
- Always include country code (+1, +44, +91, etc.)
- Format: +1234567890 (no spaces or dashes)
- Verify numbers before adding

### Organization
- Use notes field for important context
- Add emails for multi-channel communication
- Regular cleanup: delete outdated contacts

### Privacy & Security
- Don't share contacts.json file publicly
- Keep backup of important contacts
- Be cautious when importing from unknown sources

## Troubleshooting

### Contact Not Found
**Issue:** "Contact 'John' not found"

**Solutions:**
1. Check exact name: `python scripts/whatsapp_contact_manager.py list`
2. Use search: `python scripts/whatsapp_contact_manager.py search "john"`
3. Case doesn't matter, but spelling does

### Phone Number Format Error
**Issue:** "Phone number must include country code"

**Solution:** Add `+` and country code:
- ✅ Correct: `+1234567890`
- ❌ Wrong: `1234567890`
- ❌ Wrong: `123-456-7890`

### Import CSV Errors
**Issue:** Contacts skipped during import

**Check:**
1. CSV has headers: `name,phone,email,notes`
2. Phone numbers include country code
3. No duplicate names
4. Proper CSV encoding (UTF-8)

### Batch CSV Not Resolving Names
**Issue:** Batch system not finding contact

**Solutions:**
1. Verify contact exists: `python scripts/whatsapp_contact_manager.py list`
2. Check spelling in CSV matches contact name exactly
3. Fall back to phone number in CSV if needed

## CLI Reference

### Add
```bash
python scripts/whatsapp_contact_manager.py add <name> <phone> [--email <email>] [--notes <notes>]
```

### Edit
```bash
python scripts/whatsapp_contact_manager.py edit <name> [--phone <phone>] [--email <email>] [--notes <notes>]
```

### Rename
```bash
python scripts/whatsapp_contact_manager.py rename <old_name> <new_name>
```

### Delete
```bash
python scripts/whatsapp_contact_manager.py delete <name>
```

### List
```bash
python scripts/whatsapp_contact_manager.py list [--sort {name,phone,created,updated}]
```

### Search
```bash
python scripts/whatsapp_contact_manager.py search <query>
```

### Import
```bash
python scripts/whatsapp_contact_manager.py import <csv_file>
```

### Export
```bash
python scripts/whatsapp_contact_manager.py export <csv_file> [--all-fields]
```

### Create Batch CSV
```bash
python scripts/whatsapp_contact_manager.py create-batch <output_file> [--names <name1> <name2> ...] [--type {basic,personalized,image}]
```

### Stats
```bash
python scripts/whatsapp_contact_manager.py stats
```

## Summary

The WhatsApp Contact Manager makes messaging easier by:
- ✅ Saving contacts once, use forever
- ✅ Messaging by name instead of phone numbers
- ✅ Organizing contacts with full CRUD operations
- ✅ Seamless integration with batch messaging
- ✅ Import/export for bulk management

**Get Started:** Run `batch_scripts\automation\whatsapp_contacts.bat`

---

## Related Documentation

- [WhatsApp Batch Automation Guide](./WHATSAPP_BATCH_AUTOMATION_GUIDE.md) - Batch messaging system
- [WhatsApp Messenger Guide](./WHATSAPP_MESSENGER_GUIDE.md) - Single message sending

---

**Last Updated**: November 19, 2025
**Version**: 1.0.0
