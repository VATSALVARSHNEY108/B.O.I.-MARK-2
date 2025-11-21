# 📱 WhatsApp Messenger Control

## Overview
Send WhatsApp messages directly from command line using batch files, Python scripts, or BOI voice commands!

---

## 🎯 Features

✅ **Send Instant Messages** - Quick messaging to contacts or phone numbers  
✅ **Schedule Messages** - Set messages to send at specific times  
✅ **Send Images** - Share photos with captions  
✅ **Group Messaging** - Send to WhatsApp groups  
✅ **Contact Integration** - Use contact names instead of phone numbers  
✅ **Interactive Menu** - User-friendly batch file interface  
✅ **BOI Integration** - Voice command support  

---

## 🗣️ Voice Commands for BOI

Just say:

- **"Send WhatsApp to John saying hello"**
- **"WhatsApp Mom I'm running late"**
- **"Send WhatsApp to +1234567890 saying meeting at 3pm"**
- **"Schedule WhatsApp to John at 3pm saying reminder"**
- **"Send WhatsApp image to Sarah"**

---

## 💻 Interactive Batch File Menu

Run the interactive menu:

```batch
cd batch_scripts\automation
whatsapp_messenger.bat
```

### Menu Options:

1. **Send Instant Message** - Send message now
2. **Send Scheduled Message** - Schedule for specific time
3. **Send Image/Photo** - Share images with caption
4. **Send to Group** - Message WhatsApp groups
5. **List Contacts** - View your contacts
6. **Quick Send (Contact Name)** - Fast send by name
7. **Quick Send (Phone Number)** - Fast send by number
8. **Help / Usage Guide** - Show detailed help
9. **Exit** - Close menu

---

## 🐍 Python CLI Usage

### Basic Message Sending

```bash
# Send to phone number
python scripts/whatsapp_cli.py send +1234567890 "Hello!"

# Send to contact by name
python scripts/whatsapp_cli.py send "John Doe" "How are you?"

# Multi-word messages
python scripts/whatsapp_cli.py send Mom "I'll be home by 6pm"
```

### Scheduled Messages

```bash
# Schedule for 3:30 PM (15:30)
python scripts/whatsapp_cli.py schedule +1234567890 15 30 "Meeting reminder"

# Schedule using contact name
python scripts/whatsapp_cli.py schedule "John" 9 0 "Good morning!"
```

### Send Images

```bash
# Send image with caption
python scripts/whatsapp_cli.py image +1234567890 photo.jpg "Check this out!"

# Send image to contact
python scripts/whatsapp_cli.py image "Sarah" vacation.png "From my trip!"

# Send image without caption
python scripts/whatsapp_cli.py image +1234567890 screenshot.png
```

### Group Messages

```bash
# Send to WhatsApp group
python scripts/whatsapp_cli.py group ABC123XYZ "Hello everyone!"
```

### List Contacts

```bash
# View all contacts
python scripts/whatsapp_cli.py contacts
```

---

## 📞 Phone Number Format

**Always include country code:**
- ✅ Correct: `+1234567890`
- ❌ Wrong: `1234567890`
- ❌ Wrong: `234-567-8900`

**Supported formats:**
- `+1234567890` (preferred)
- Contact name from `data/contacts.json`

---

## 📇 Contact Integration

The system uses your contacts from `data/contacts.json`:

```json
[
    {
        "name": "John Doe",
        "phone": "+1234567890",
        "email": "john@example.com"
    }
]
```

**Add contacts:**
```bash
python scripts/manage_contacts.py add "Jane Smith" +1987654321 jane@email.com
```

**Use contacts in commands:**
```bash
# By name instead of phone number
python scripts/whatsapp_cli.py send "John Doe" "Hey John!"
```

---

## 🚀 Quick Examples

### Example 1: Send Quick Message
```batch
whatsapp_messenger.bat
# Select option 7 (Quick Send - Phone Number)
# Enter: +1234567890
# Enter: "Hey, how's it going?"
```

### Example 2: Send to Contact
```batch
whatsapp_messenger.bat
# Select option 6 (Quick Send - Contact Name)
# Enter: Mom
# Enter: "I'll be late for dinner"
```

### Example 3: Schedule Reminder
```batch
whatsapp_messenger.bat
# Select option 2 (Send Scheduled Message)
# Enter: +1234567890
# Hour: 14 (2 PM)
# Minute: 30
# Message: "Meeting in 30 minutes!"
```

### Example 4: Send Image
```batch
whatsapp_messenger.bat
# Select option 3 (Send Image/Photo)
# Enter: Sarah
# Image path: C:\Users\YourName\Pictures\photo.jpg
# Caption: "Look at this!"
```

---

## ⚙️ How It Works

### 1. **PyWhatKit Mode** (Default)
- Uses `pywhatkit` library
- Opens WhatsApp Web automatically
- Sends messages programmatically
- Supports scheduling

### 2. **Web Mode** (Fallback)
- Opens WhatsApp Web with pre-filled message
- User presses Enter to send
- Works if pywhatkit is unavailable

---

## 🔧 Requirements

- ✅ Python 3.x
- ✅ WhatsApp Web access
- ✅ `pywhatkit` library (installed)
- ✅ Internet connection
- ✅ WhatsApp account linked to WhatsApp Web

---

## 💡 Pro Tips

### Tip 1: Use Contact Names
```bash
# Instead of remembering phone numbers
python scripts/whatsapp_cli.py send "Boss" "Report sent"
```

### Tip 2: Batch Multiple Messages
Create a batch script:
```batch
@echo off
python scripts/whatsapp_cli.py send "John" "Message 1"
timeout /t 20
python scripts/whatsapp_cli.py send "Sarah" "Message 2"
```

### Tip 3: Schedule Morning Messages
```bash
# Schedule good morning at 8 AM
python scripts/whatsapp_cli.py schedule Mom 8 0 "Good morning!"
```

### Tip 4: Quick Image Sharing
```bash
# Share screenshot quickly
python scripts/whatsapp_cli.py image +1234567890 %USERPROFILE%\Desktop\screenshot.png
```

---

## 🐛 Troubleshooting

**"Contact not found"**
- Check contact name spelling
- Ensure contact exists in `data/contacts.json`
- Use phone number instead

**"WhatsApp Web not opening"**
- Check internet connection
- Ensure WhatsApp Web is accessible
- Try logging into WhatsApp Web manually first

**"Message not sending"**
- Wait for WhatsApp Web to fully load
- Check if phone number format is correct (+country code)
- Ensure WhatsApp account is active

**"Scheduled message failed"**
- PyWhatKit must be installed
- Computer must stay on until scheduled time
- WhatsApp Web must remain accessible

---

## 📋 Command Reference

### CLI Commands
```bash
# Send instant message
whatsapp_cli.py send <phone/name> <message>

# Schedule message
whatsapp_cli.py schedule <phone/name> <hour> <minute> <message>

# Send image
whatsapp_cli.py image <phone/name> <image_path> [caption]

# Send to group
whatsapp_cli.py group <group_id> <message>

# List contacts
whatsapp_cli.py contacts

# Show help
whatsapp_cli.py help
```

---

## 📁 File Locations

- **Batch Menu:** `batch_scripts/automation/whatsapp_messenger.bat`
- **Python CLI:** `scripts/whatsapp_cli.py`
- **Contacts Data:** `data/contacts.json`
- **Module:** `modules/communication/whatsapp_automation.py`

---

## 🎯 Use Cases

### Personal Use
- Send quick messages to family
- Share photos instantly
- Schedule reminders
- Manage group chats

### Business Use
- Customer notifications
- Appointment reminders
- Team communications
- Marketing messages

### Automation
- Automated birthday wishes
- Daily reports to team
- Scheduled announcements
- System notifications

---

## 🔒 Privacy & Security

- Messages sent through official WhatsApp Web
- No data stored except contacts.json
- Uses your WhatsApp account credentials
- All communication encrypted by WhatsApp

---

## 🎉 Enjoy!

You can now send WhatsApp messages from:
- 📝 **Batch file menu** (interactive)
- 🐍 **Python CLI** (command line)
- 🗣️ **BOI voice** (natural language)

Happy messaging! 📱✨
