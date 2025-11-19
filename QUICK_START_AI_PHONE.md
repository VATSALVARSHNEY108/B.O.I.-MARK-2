# 🚀 Quick Start: AI Phone Link Controller

## 📱 What This Does
Control your phone using **AI + Windows Phone Link** app! Make calls, send messages, and control your phone with natural language commands.

---

## ⚡ Quick Start (3 Steps)

### Step 1: Choose Your Launcher

#### 🎯 Option A: Interactive Mode (Best for chatting)
```batch
Double-click: launchers/ai_phone_controller.bat
```
Then type commands like:
- "Call +1234567890"
- "Open Phone Link"
- "Dial mom at 9876543210"

#### 🎯 Option B: Quick Dial (Best for one number)
1. Edit `launchers/quick_dial.bat`
2. Change: `set PHONE_NUMBER=+YOUR_NUMBER`
3. Double-click to call instantly!

#### 🎯 Option C: Custom Number (Best for flexibility)
```batch
Double-click: launchers/ai_phone_with_number.bat
```
Enter any number when prompted!

### Step 2: (Optional) Enable AI Power
Without AI key = Basic mode ✓ (still works!)
With AI key = Smart mode ✓✓ (understands natural language)

**Get free API key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Create API key
3. In Replit: Add Secret `GOOGLE_API_KEY` = your key

**Or on Windows:**
```batch
setx GOOGLE_API_KEY "your-api-key-here"
```

### Step 3: Make Sure Phone Link is Ready
- ✅ Windows 10/11
- ✅ Phone Link app installed (Microsoft Store)
- ✅ Phone connected to Phone Link

---

## 🎮 How to Use

### From Batch Files (Easiest):
1. **ai_phone_controller.bat** - Chat with AI
2. **quick_dial.bat** - One-click calling
3. **ai_phone_with_number.bat** - Dial any number

### From Command Line:
```bash
# Interactive mode
python ai_phone_link_controller.py

# Direct command
python ai_phone_link_controller.py "Call +1234567890"

# Run demo
python demo_ai_phone_control.py
```

### From Python Code:
```python
from ai_phone_link_controller import AIPhoneLinkController

controller = AIPhoneLinkController()

# Natural language
controller.process_command("Call mom at +1234567890")

# Quick dial
controller.quick_dial("+1234567890")
```

---

## 💬 Example Commands

**With AI (Smart Mode):**
```
✅ "Call my friend at +1234567890"
✅ "Dial 9876543210"
✅ "Ring +91 98765 43210"
✅ "Open Phone Link app"
✅ "Phone (123) 456-7890"
```

**Without AI (Basic Mode):**
```
✅ "Call +1234567890"
✅ "Dial 9876543210"
✅ "Open Phone Link"
```

Both work! AI just makes it smarter. 🧠

---

## 🎯 What Each File Does

| File | Purpose | Use When |
|------|---------|----------|
| `ai_phone_link_controller.py` | Main AI controller | You want full control |
| `ai_phone_controller.bat` | Interactive launcher | You want to chat with AI |
| `quick_dial.bat` | Fast dial preset number | You call same number often |
| `ai_phone_with_number.bat` | Dial any number | You want flexibility |
| `demo_ai_phone_control.py` | Demo/examples | You want to see how it works |

---

## 🔧 Troubleshooting

### "AI Engine: ⚠️ Basic mode"
- **Not a problem!** Controller still works
- To enable AI: Add `GOOGLE_API_KEY` secret

### "Phone Link: ❌"
- Install Phone Link from Microsoft Store
- Make sure your phone is connected
- This only works on Windows 10/11

### "Python not found"
- Install Python from python.org
- Restart computer after installation

---

## 📖 Full Documentation
Read `AI_PHONE_LINK_CONTROLLER_GUIDE.md` for complete details!

---

## 🎉 You're Ready!

**Try it now:**
```batch
Double-click: launchers/ai_phone_controller.bat
```

**Or run demo:**
```bash
python demo_ai_phone_control.py
```

Enjoy AI-powered phone control! 📱🤖
