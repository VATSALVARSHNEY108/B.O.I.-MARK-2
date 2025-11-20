# WhatsApp Commands - Quick Guide

## ✅ Fixed: WhatsApp Messaging Now Works!

The `send_whatsapp` action has been successfully integrated with the command executor.

## How to Use WhatsApp Commands

### Method 1: Send by Contact Name (Recommended)

**Step 1: Add a contact first**
```
"Add WhatsApp contact Vatsal with phone +911234567890"
```

**Step 2: Send message**
```
"WhatsApp Vatsal Hi there!"
"Send WhatsApp to Vatsal saying Hello"
"Message Vatsal on WhatsApp: How are you?"
```

### Method 2: Send by Phone Number

```
"WhatsApp +911234567890 Hi there!"
"Send WhatsApp to +911234567890 saying Hello"
```

## Voice Command Examples

Here are natural ways to send WhatsApp messages:

✅ **Simple Commands:**
- "WhatsApp John hello"
- "Message Sarah on WhatsApp"
- "Send hi to Mike on WhatsApp"

✅ **With Full Message:**
- "WhatsApp Vatsal: How are you doing today?"
- "Send WhatsApp to Mom saying I'll be home late"
- "Message Dad on WhatsApp: Can you call me?"

✅ **By Phone Number:**
- "WhatsApp +1234567890 Hello"
- "Send WhatsApp to +91 98765 43210: Meeting at 5pm"

## Managing Contacts

### Add a Contact

Voice:
```
"Add WhatsApp contact [Name] with phone +[country code][number]"
```

CLI:
```bash
python scripts/whatsapp_contact_manager.py add "Vatsal Varshney" "+911234567890"
```

### List All Contacts

CLI:
```bash
python scripts/whatsapp_contact_manager.py list
```

### Search for a Contact

CLI:
```bash
python scripts/whatsapp_contact_manager.py search Vatsal
```

### Remove a Contact

CLI:
```bash
python scripts/whatsapp_contact_manager.py delete "Vatsal Varshney"
```

## Advanced Features

### Schedule a WhatsApp Message

```
"Schedule WhatsApp to John at 3pm saying Meeting reminder"
```

### Send Image via WhatsApp

```
"Send WhatsApp image to Sarah at path C:/image.jpg with caption Check this out"
```

### Open WhatsApp Desktop

```
"Open WhatsApp"
"Launch WhatsApp Desktop"
```

## Troubleshooting

### Error: "Contact not found"

**Solution:** Add the contact first
```bash
python scripts/whatsapp_contact_manager.py add "Name" "+CountryCodeNumber"
```

### Error: "No phone number provided"

**Solution:** Specify either:
1. A contact name that exists in your contacts, OR
2. A full phone number with country code (e.g., +1234567890)

### Error: "Phone number must include country code"

**Solution:** Always use format: `+[country code][number]`
- ✅ Correct: `+911234567890`
- ❌ Wrong: `1234567890`

### PyWhatKit Not Available

If you see "PyWhatKit not available", the system will fall back to WhatsApp Web:
- A browser window will open with WhatsApp Web
- The message will be pre-filled
- **You must press Enter to send**

## Contact File Location

Contacts are stored in: `data/contacts.json`

You can also manually edit this file to add bulk contacts.

## Examples for Your Use Case

Based on your command "whatsapp vatsal hi":

**Option 1: Add Vatsal as a contact first (Recommended)**
```bash
# Add contact
python scripts/whatsapp_contact_manager.py add "Vatsal" "+919876543210"

# Then send message
Voice: "WhatsApp Vatsal hi"
```

**Option 2: Use phone number directly**
```
Voice: "WhatsApp +919876543210 hi"
```

## Integration Details

The WhatsApp system now supports:
- ✅ Sending by contact name (auto-lookup)
- ✅ Sending by phone number
- ✅ Contact management integration
- ✅ PyWhatKit desktop automation
- ✅ WhatsApp Web fallback
- ✅ Scheduled messages
- ✅ Group messages
- ✅ Image sending

## Tips

1. **Always use country code** - Required for international format
2. **Add frequent contacts** - Makes sending faster
3. **Test with yourself first** - Send to your own number to test
4. **Browser must be logged in** - WhatsApp Web requires you to be logged in
5. **Desktop app preferred** - WhatsApp Desktop works better than web

---

**Quick Start:**
1. Add a contact: `python scripts/whatsapp_contact_manager.py add "Name" "+Phone"`
2. Send message: Voice command "WhatsApp Name your message"
3. Done! 🎉
