# 🚀 AI Phone Link Launchers

Quick access batch files and scripts to launch the AI Phone Link Controller.

---

## 📁 Files in This Directory

### Windows Batch Files (.bat)

#### **ai_phone_controller.bat**
🎯 **Interactive AI Phone Controller**
- Launches full AI chat mode
- Type natural language commands
- Understands: "Call +1234567890", "Dial mom", "Open Phone Link"
- Best for: Regular use, multiple calls, chatting with AI

**How to use:**
```
Double-click the file
```

---

#### **quick_dial.bat**
⚡ **One-Click Speed Dial**
- Dials a preset phone number instantly
- Edit the file to set your number
- No typing needed after setup
- Best for: Emergency contacts, frequent calls

**How to setup:**
1. Right-click → Edit
2. Change: `set PHONE_NUMBER=+1234567890`
3. Save and double-click to dial

---

#### **ai_phone_with_number.bat**
📱 **Quick Call Any Number**
- Prompts for phone number
- Uses AI to process command
- Best for: Occasional calls, different numbers

**How to use:**
```
Double-click and enter number when asked
OR
Drag to terminal: ai_phone_with_number.bat "+1234567890"
```

---

### PowerShell Script (.ps1)

#### **ai_phone_controller.ps1**
🔷 **PowerShell Alternative**
- Same as ai_phone_controller.bat
- For PowerShell users
- Colored output and better error handling

**How to use:**
```
Right-click → Run with PowerShell
OR
PowerShell: .\ai_phone_controller.ps1
```

---

## 🎯 Which One Should I Use?

| Your Need | Recommended File |
|-----------|-----------------|
| **Chat with AI to make calls** | `ai_phone_controller.bat` |
| **Call same number often** | `quick_dial.bat` (edit first) |
| **Call different numbers** | `ai_phone_with_number.bat` |
| **PowerShell preference** | `ai_phone_controller.ps1` |

---

## 🔑 Optional: Enable AI Smart Mode

All launchers work **without** AI using basic command parsing.

To enable **AI smart mode** (better natural language understanding):

1. Get free API key: https://makersuite.google.com/app/apikey
2. Add to Replit Secrets: `GOOGLE_API_KEY`
   OR
3. Windows command: `setx GOOGLE_API_KEY "your-key-here"`

---

## 🖥️ Desktop Shortcuts

Want these on your desktop?

Run from project root:
```batch
create_desktop_shortcuts.bat
```

This creates desktop shortcuts for:
- AI Phone Controller
- Quick Dial

---

## 📚 Full Documentation

- **Quick Start:** `../QUICK_START_AI_PHONE.md`
- **Complete Guide:** `../AI_PHONE_LINK_CONTROLLER_GUIDE.md`
- **Phone Link Guide:** `../PHONE_LINK_DIAL_GUIDE.md`

---

## 🐛 Troubleshooting

### Batch file won't run
- Right-click → Run as Administrator
- Check Python is installed

### "Phone Link not found"
- Install from Microsoft Store
- Make sure phone is connected
- Windows 10/11 only

### "Python not found"
- Install from python.org
- Restart computer

---

## 💡 Tips

1. **Edit quick_dial.bat** with your most-called number
2. **Pin to taskbar** for instant access
3. **Use Ctrl+C** to exit interactive mode
4. **Set GOOGLE_API_KEY** for best experience

---

**Made for VATSAL AI System** 📱🤖
