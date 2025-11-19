# 📇 Contact-Based Calling Guide

## 🎯 What's New

You can now **call contacts by name** instead of typing phone numbers! Just say "Call Mom" or "Call John" and the system finds their number automatically.

---

## ✨ Features

✅ **Call by name** - "Call Mom", "Call Dad", "Call John"  
✅ **Automatic contact lookup** - No need to remember numbers  
✅ **Contact manager** - Add, edit, delete contacts easily  
✅ **AI understanding** - Works with natural language  
✅ **Smart suggestions** - "Did you mean...?" for typos  
✅ **Sample contacts** - Quick import of test contacts  

---

## 🚀 Quick Start

### Step 1: Add Contacts

**Option A: Using Contact Manager (Recommended)**
```bash
# Launch interactive contact manager
python manage_contacts.py

# Or use the batch file
launchers\manage_contacts.bat
```

**Option B: Quick Command Line**
```bash
# Add a contact
python manage_contacts.py add

# List contacts
python manage_contacts.py list

# Call a contact
python manage_contacts.py call Mom
```

**Option C: Import Sample Contacts**
```bash
python manage_contacts.py
# Then select option 7: Import sample contacts
```

### Step 2: Call by Name

**AI Controller (Natural Language):**
```bash
python ai_phone_link_controller.py "Call Mom"
```

**Interactive Mode:**
```bash
python ai_phone_link_controller.py
```
Then type:
- "Call Mom"
- "Call Dad"
- "Call John"

**From Python Code:**
```python
from modules.communication.phone_dialer import create_phone_dialer

dialer = create_phone_dialer()
result = dialer.call_contact("mom")
print(result['message'])
```

---

## 📋 Contact Manager Features

### 1. List All Contacts
```
Select option 1 in the menu
```
Shows all saved contacts with phone numbers and emails.

### 2. Add New Contact
```
Select option 2 in the menu
```
- Enter name (e.g., "Mom", "John Smith")
- Enter phone number (e.g., "+1234567890")
- Enter email (optional)

### 3. Edit Contact
```
Select option 3 in the menu
```
Update phone number or email for existing contact.

### 4. Delete Contact
```
Select option 4 in the menu
```
Remove a contact from your list.

### 5. Search Contacts
```
Select option 5 in the menu
```
Find contacts by partial name match.

### 6. Call a Contact
```
Select option 6 in the menu
```
Direct call from contact manager interface.

### 7. Import Sample Contacts
```
Select option 7 in the menu
```
Adds 5 test contacts instantly.

---

## 📞 How to Call Contacts

### Method 1: AI Controller (Best)
```bash
python ai_phone_link_controller.py "Call Mom"
```

**Understands natural language:**
- "Call Mom"
- "Call my dad"
- "Ring John Smith"
- "Phone the office"

### Method 2: Interactive Mode
```bash
python ai_phone_link_controller.py
```
```
🎤 Enter command: Call Mom
```

### Method 3: From Code
```python
from modules.communication.phone_dialer import create_phone_dialer

dialer = create_phone_dialer()

# Call by name
result = dialer.call_contact("mom")

# Call by number (still works)
result = dialer.dial_with_phone_link("+1234567890")
```

### Method 4: Quick Dial
```python
# Works with both names and numbers
result = dialer.quick_dial("mom")
result = dialer.quick_dial("+1234567890")
```

---

## 📁 contacts.json Format

Your contacts are stored in `contacts.json`:

```json
{
  "mom": {
    "name": "Mom",
    "phone": "+1234567890",
    "email": "mom@example.com"
  },
  "dad": {
    "name": "Dad",
    "phone": "+1234567891",
    "email": "dad@example.com"
  },
  "john": {
    "name": "John Smith",
    "phone": "+1234567892",
    "email": "john@example.com"
  }
}
```

**Manual Editing:**
You can edit `contacts.json` directly if you prefer!

---

## 💡 Tips & Tricks

### 1. Name Matching is Smart
- Case-insensitive: "mom", "Mom", "MOM" all work
- Partial matching in search
- Fuzzy suggestions: "Did you mean...?"

### 2. Use Short Names
```
✅ Good: "mom", "dad", "john", "office"
❌ Avoid: "My Mother's Cell Phone"
```

### 3. Include Country Codes
```
✅ Good: "+1234567890"
⚠️  OK: "1234567890" (assumes US)
```

### 4. Backup Your Contacts
```bash
# Copy contacts.json to safe location
copy contacts.json contacts_backup.json
```

### 5. Import from Other Sources
```python
from modules.utilities.contact_manager import ContactManager

cm = ContactManager()

# Add contacts from CSV, database, etc.
contacts_to_add = [
    {"name": "Mom", "phone": "+1234567890"},
    {"name": "Dad", "phone": "+1234567891"},
]

for contact in contacts_to_add:
    cm.add_contact(contact['name'], contact['phone'])
```

---

## 🎯 Examples

### Example 1: Emergency Contacts
```python
from modules.utilities.contact_manager import ContactManager

cm = ContactManager()

# Add emergency contacts
cm.add_contact("Emergency", "911")
cm.add_contact("Mom", "+1234567890")
cm.add_contact("Doctor", "+1234567891")
cm.add_contact("Hospital", "+1234567892")
```

Then call:
```bash
python ai_phone_link_controller.py "Call Emergency"
```

### Example 2: Office Directory
```python
# Add office contacts
cm.add_contact("Main Office", "+1234567893")
cm.add_contact("IT Support", "+1234567894")
cm.add_contact("HR Department", "+1234567895")
cm.add_contact("Boss", "+1234567896")
```

### Example 3: Family & Friends
```python
# Add personal contacts
cm.add_contact("Mom", "+1234567890")
cm.add_contact("Dad", "+1234567891")
cm.add_contact("Sister", "+1234567892")
cm.add_contact("John", "+1234567893")
cm.add_contact("Sarah", "+1234567894")
```

---

## 🐛 Troubleshooting

### "Contact not found"
**Problem:** You typed a name that doesn't exist  
**Solution:**
1. Check spelling
2. List all contacts: `python manage_contacts.py list`
3. Add the contact first

### "Did you mean...?"
**Problem:** Contact name is similar but not exact  
**Solution:** This is helpful! Use the suggested name instead

### Contact has no phone number
**Problem:** Contact exists but phone field is empty  
**Solution:**
```bash
python manage_contacts.py
# Select option 3: Edit contact
# Add phone number
```

### Calling wrong person
**Problem:** Two contacts have similar names  
**Solution:** Use more specific names:
- ❌ "John" (ambiguous)
- ✅ "John Smith", "John Work"

---

## 🔄 Sync with Other Systems

### Import from Phone
1. Export contacts from your phone (CSV format)
2. Write a simple script to convert to contacts.json
3. Or add manually using contact manager

### Backup to Cloud
```bash
# Upload contacts.json to Dropbox, Google Drive, etc.
# Restore by copying file back
```

---

## 📊 Comparison

| Feature | Before | With Contacts |
|---------|--------|---------------|
| **Call Mom** | ❌ Can't | ✅ "Call Mom" |
| **Remember numbers** | ❌ Required | ✅ Not needed |
| **Typing** | 📱 +1234567890 | 👤 mom |
| **AI commands** | ⚠️ Number only | ✅ Name or number |
| **Speed** | 🐢 Slower | ⚡ Faster |

---

## 🎮 All Available Commands

### AI Controller Commands:
```
✅ "Call Mom"
✅ "Call Dad"
✅ "Call John Smith"
✅ "Ring the office"
✅ "Phone emergency"
✅ "Call +1234567890"  ← Still works!
```

### Contact Manager Commands:
```bash
python manage_contacts.py          # Interactive mode
python manage_contacts.py list     # List all
python manage_contacts.py add      # Add new
python manage_contacts.py call Mom # Call contact
```

---

## 📚 Files Created

| File | Purpose |
|------|---------|
| `contacts.json` | Your contact database |
| `manage_contacts.py` | Contact management tool |
| `launchers/manage_contacts.bat` | Windows launcher |
| `test_contact_calling.py` | Test script |
| `CONTACT_CALLING_GUIDE.md` | This guide |

---

## ✅ Quick Test

**Try this now:**

```bash
# 1. Import sample contacts
python manage_contacts.py
# Select option 7

# 2. Test calling by name
python ai_phone_link_controller.py "Call Mom"

# 3. Try your own contact
python manage_contacts.py add
# Add a real contact

# 4. Call it!
python ai_phone_link_controller.py "Call <your contact>"
```

---

## 🎉 Summary

Now you can:
- ✅ Save contacts with names and phone numbers
- ✅ Call anyone by just saying their name
- ✅ Manage contacts easily with contact manager
- ✅ Use AI to understand natural language
- ✅ Get smart suggestions for typos
- ✅ Call by name or number (both work!)

**No more memorizing phone numbers!** 📇📱🎉

---

**Enjoy calling by name!** 🚀
