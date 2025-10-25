# 📱 Visual AI Chat Monitor & Auto-Reply Guide

## Overview
The Visual Chat Monitor lets AI **control Gmail and WhatsApp on your actual screen** - you can watch everything happen in real-time! AI reads your messages using Vision AI and types replies with your approval.

⚠️ **Important Note:** Visual automation is **best-effort** and may require manual intervention. Keyboard shortcuts can fail if Gmail focus changes unexpectedly. For fully automated, reliable operation, use the **API mode** instead (requires Gmail App Password + Twilio credentials).

## 🎯 How It Works

### Visual Mode (Recommended - You Can Watch!)
1. **AI opens Gmail in your browser and maximizes window**
2. **Takes screenshot and reads emails with AI Vision**
3. **Uses Gmail keyboard shortcuts to navigate and open emails** (works on any screen size!)
4. **Reads the full content from screen**
5. **Generates smart AI reply**
6. **Shows you the suggestion and asks permission**
7. **Types the reply in Gmail compose window**
8. **Waits for you to review before sending**

Everything happens visually - you see the browser open, emails being navigated with keyboard, and replies being typed!

**Why keyboard shortcuts?** They work on ANY screen resolution, browser zoom level, or window size - unlike mouse clicks which need exact pixel positions.

## 🚀 Quick Start Commands

### Complete Workflow (All-in-One)
```
"Monitor my Gmail and reply with AI"
"Check my emails and help me reply"
"Visual Gmail monitor"
```

The AI will:
- Open Gmail
- Read the first unread email
- Generate a professional reply
- Type it for your review
- Wait for your approval

### Step-by-Step Commands

**1. Open Gmail**
```
"Open Gmail in browser"
```

**2. Read Emails from Screen**
```
"Read my emails from screen"
"What emails do I have?"
```
- Takes screenshot of Gmail inbox
- Uses AI Vision to read sender, subject, preview

**3. Open Specific Email**
```
"Read the first email on screen"
"Open email number 2"
```
- Clicks on the email
- Reads full content with AI Vision

**4. Generate Reply**
```
"Generate AI reply for this email"
```

**5. Open WhatsApp Web**
```
"Open WhatsApp Web"
"Check my WhatsApp"
```

**6. Read WhatsApp from Screen**
```
"Read my WhatsApp messages"
"What WhatsApp chats do I have?"
```

## 💡 Example Workflow

**You:** "Monitor my Gmail visually"

**AI:** 
1. Opens Gmail in browser
2. Takes screenshot
3. Shows you: "Found 3 emails: (1) John - Meeting Tomorrow, (2) Sarah - Project Update..."
4. Asks: "Press ENTER to read first email"
5. Clicks on first email
6. Reads content with AI Vision
7. Shows email content to you
8. Generates professional reply
9. Shows suggested reply
10. Asks: "Type 'yes' to type this reply in Gmail"
11. Types the reply in the compose window
12. YOU review it on screen and click Send yourself (or have AI click Send)

## ⚙️ Reply Styles

### Professional (Default)
```
"Monitor Gmail with professional replies"
```
- Formal tone
- Complete sentences
- Professional sign-off

### Casual
```
"Monitor Gmail with casual replies"
```
- Friendly, relaxed tone
- Conversational style

### Friendly
```
"Monitor Gmail with friendly replies"
```
- Warm, approachable
- Personal touch

## 🔧 Configuration

### Gmail Setup
1. Make sure you're logged into Gmail in your default browser
2. **Enable Gmail keyboard shortcuts** (Settings → See all settings → Keyboard shortcuts: ON)
3. AI will open `mail.google.com` and maximize the browser window
4. AI waits 7 seconds for page to load
5. Uses Gmail keyboard shortcuts (j/k to navigate, Enter to open, r to reply)
6. Works on ANY screen resolution or browser zoom level
7. Compatible with Chrome, Edge, Firefox, Safari

### WhatsApp Web Setup
1. Have WhatsApp installed on your phone
2. AI opens `web.whatsapp.com`
3. Scan QR code on your phone if not logged in
4. AI waits 8 seconds for WhatsApp to load

## 🎮 Control Options

### Auto-Send Mode (Careful!)
```
"Monitor Gmail and auto-send replies"
```
- AI will type AND click Send button
- Use only if you trust AI completely

### Review Mode (Recommended)
```
"Monitor Gmail visually"
```
- AI types the reply
- YOU review it on screen
- YOU click Send manually
- **This is the safe default**

## 📊 vs API Mode

| Feature | Visual Mode | API Mode |
|---------|-------------|----------|
| **You Can Watch** | ✅ Yes | ❌ No (background) |
| **Setup Required** | Just login to Gmail | API credentials (GMAIL_APP_PASSWORD, Twilio) |
| **Speed** | Slower (visual) | Faster |
| **Reliability** | ⚠️ **Best-effort** - may need manual help | ✅ Fully automated & reliable |
| **Works With** | Any email in browser | Gmail IMAP + Twilio SMS |
| **Best For** | Watching AI work, learning | Production use, automation |
| **Limitations** | Focus issues, screen-dependent | Requires API setup |

**Recommendation:** Use **Visual Mode** for demonstration/learning. Use **API Mode** for reliable daily automation.

## 🔒 Privacy & Safety

✅ **What AI Can See:**
- Emails visible on your screen
- Content you choose to open
- Only when you run the command

✅ **What AI CANNOT Do:**
- Send replies without your permission (review mode)
- Access emails when not actively running
- See passwords (they're hidden in browsers)

✅ **Safety Tips:**
1. Use **Review Mode** (default) - you approve every reply
2. Watch the screen as AI works
3. Review typed replies before clicking Send
4. Start with less important emails to test

## 🐛 Troubleshooting

**Gmail not loading?**
- Wait longer (increase sleep time in code)
- Make sure you're logged in
- Check your internet connection

**Keyboard shortcuts not working?**
- Enable them in Gmail Settings → Keyboard shortcuts: ON
- Make sure browser window is focused (click on it)
- Try pressing keys manually to verify Gmail responds
- **If shortcuts keep failing:** Click manually on the inbox/email/compose area to help focus
- **For reliable automation:** Switch to API mode (`monitor chats` command)

**AI can't read emails?**
- Screenshot might be unclear
- Try again with better screen resolution
- Make sure Gmail is fully loaded

**WhatsApp not showing messages?**
- Make sure you're logged in on phone
- QR code scanned successfully
- Wait for chats to load fully

## 🎓 Advanced Usage

### Gmail Keyboard Shortcuts Used
- **j** - Move down to next email
- **k** - Move up to previous email
- **Enter** - Open selected email
- **r** - Reply to email
- **Ctrl+Enter** - Send email
- **Ctrl+Home** - Jump to top of inbox

### Longer Wait Times
If pages load slowly, increase sleep times:
```python
time.sleep(10)  # Wait 10 seconds instead of 5
```

## 📝 Notes & Limitations

- Works on Windows, Mac, Linux
- Requires active internet connection
- Browser must be visible (not minimized)
- Best with clean, uncluttered inbox
- AI Vision works best with clear text
- Screenshots saved to `screenshots/` folder
- ⚠️ **May require manual intervention** if keyboard shortcuts fail to acquire proper focus
- ⚠️ **Not recommended for critical emails** - use API mode for reliability
- ✅ **Great for demonstration** - you can watch and learn how AI interprets emails

## 🎉 Benefits

1. **Visual Transparency** - Watch AI work in real-time
2. **Full Control** - Approve every reply before sending
3. **No API Setup** - Just login to Gmail normally
4. **Works Everywhere** - Any email visible on screen
5. **Learning Tool** - See how AI interprets your emails

Enjoy your AI-powered email assistant! 🤖📧
