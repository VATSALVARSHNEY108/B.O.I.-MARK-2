# WhatsApp Automation Guide

## Features

Your AI assistant can now send WhatsApp messages! Here's what you can do:

### 1. Send Instant Message
Send a WhatsApp message right away.

**Example commands:**
- "Send WhatsApp to +1234567890 saying Hello!"
- "WhatsApp +1234567890 with the message How are you?"
- "Send a WhatsApp message to +1234567890: Meeting at 3pm"

**Requirements:**
- Phone number must include country code (e.g., +1 for USA, +91 for India)
- WhatsApp Web must be logged in on your default browser

### 2. Schedule Message
Schedule a WhatsApp message for a specific time.

**Example commands:**
- "Schedule WhatsApp to +1234567890 at 3pm saying Don't forget the meeting"
- "Send WhatsApp to +1234567890 at 15:30 with message Reminder"

**Note:** Time is in 24-hour format (15 = 3pm, 20 = 8pm)

### 3. Send to Group
Send message to a WhatsApp group.

**Example commands:**
- "Send WhatsApp to group ABC123 saying Hello everyone"

**Note:** You need the group ID from the group invite link

### 4. Send Image
Send an image with optional caption.

**Example commands:**
- "Send image photo.jpg to +1234567890 via WhatsApp"
- "WhatsApp image /path/to/photo.jpg to +1234567890 with caption Check this out!"

**Note:** Only JPG images are supported (PNG not supported by pywhatkit)

## Important Notes

1. **First Time Setup:**
   - WhatsApp Web will open in your browser
   - You may need to scan QR code if not already logged in
   - Keep WhatsApp Web logged in for automatic messages

2. **Phone Number Format:**
   - Always include country code
   - Example: +1234567890 (not 1234567890)
   - USA: +1, UK: +44, India: +91, etc.

3. **Browser Requirements:**
   - Your default browser will be used
   - WhatsApp Web opens for 15 seconds before sending
   - The tab closes automatically after sending

## Examples

### Simple Message
```
You: "Send WhatsApp to +1234567890 saying Hello friend!"
```

### Scheduled Message
```
You: "Schedule WhatsApp at 9am to +1234567890 with message Good morning!"
```

### With Image
```
You: "Send image vacation.jpg to +1234567890 via WhatsApp"
```

## Troubleshooting

**Message not sending?**
- Make sure WhatsApp Web is logged in
- Check phone number has country code
- Ensure your browser allows pop-ups

**QR Code appears?**
- Scan it with your phone's WhatsApp
- This only happens once per browser/session

**Browser doesn't close?**
- This is normal for some systems
- The message is still sent successfully
