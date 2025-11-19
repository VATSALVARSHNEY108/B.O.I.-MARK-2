# 🤖 AI Phone Link Controller Guide

## 🎯 Overview
Control your Windows Phone Link app using AI! This system uses Google Gemini AI to understand natural language commands and operate your phone.

---

## 📦 What You Get

### 1. **AI Phone Link Controller** (`ai_phone_link_controller.py`)
- 🧠 Understands natural language commands
- 📞 Dials phone numbers automatically
- 🤖 Powered by Google Gemini AI
- 💬 Interactive chat mode
- 📝 Command history tracking

### 2. **Batch Files for Easy Launch**

#### **ai_phone_controller.bat**
Launch the interactive AI phone controller
```batch
Double-click to start interactive mode
```

#### **quick_dial.bat**
One-click dialing of your favorite number
```batch
Edit the file to set your number, then double-click
```

#### **ai_phone_with_number.bat**
Dial any number quickly
```batch
Double-click and enter number when prompted
OR
Drag file to terminal: ai_phone_with_number.bat "+1234567890"
```

---

## 🚀 Quick Start

### Method 1: Interactive Mode (Recommended)
1. Double-click `launchers/ai_phone_controller.bat`
2. Type commands in natural language:
   - "Call +1234567890"
   - "Dial mom at 9876543210"
   - "Open Phone Link"
3. Type 'quit' to exit

### Method 2: Quick Dial
1. Edit `launchers/quick_dial.bat`
2. Set your phone number: `set PHONE_NUMBER=+1234567890`
3. Double-click to call instantly

### Method 3: Command Line
```bash
python ai_phone_link_controller.py "Call +1234567890"
```

---

## 🔑 Setup AI (Optional but Recommended)

The controller works **without AI** using simple command parsing, but AI gives you:
- ✅ Natural language understanding
- ✅ Smart number extraction
- ✅ Better command interpretation

### Get Google Gemini API Key:

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your key
4. Set environment variable:

**Windows (Permanent):**
```batch
setx GOOGLE_API_KEY "your-api-key-here"
```

**Or add to Replit Secrets:**
- Open Secrets panel (🔒 icon)
- Add key: `GOOGLE_API_KEY`
- Value: Your API key

---

## 💬 Example Commands

The AI understands natural language:

```
✅ "Call +1234567890"
✅ "Dial my friend at 9876543210"
✅ "Ring +91 98765 43210"
✅ "Open Phone Link"
✅ "Phone 555-123-4567"
✅ "Call (123) 456-7890"
```

**Without AI**, use simpler commands:
```
✅ "Dial +1234567890"
✅ "Call 9876543210"
✅ "Open Phone Link"
```

---

## 🎮 How to Use

### Interactive Mode:
```bash
python ai_phone_link_controller.py
```

**Screenshot:**
```
🎤 Enter command: Call mom at +1234567890

🤖 AI Understanding:
   Action: dial
   Phone: +1234567890
   Confidence: 95%

📱 Opening Phone Link to dial +1234567890

✅ Phone Link opened and dialing
```

### Direct Command:
```bash
python ai_phone_link_controller.py "Call +1234567890"
```

### From Python Code:
```python
from ai_phone_link_controller import AIPhoneLinkController

controller = AIPhoneLinkController()

# Natural language
result = controller.process_command("Call +1234567890")

# Quick dial
result = controller.quick_dial("+1234567890")

# Get history
history = controller.get_history(limit=5)
```

---

## 🔧 Integration with VATSAL AI

This controller integrates seamlessly with your VATSAL AI system:

```python
# In your VATSAL modules
from ai_phone_link_controller import AIPhoneLinkController

# Initialize
phone_ai = AIPhoneLinkController()

# Use in voice commands
def handle_voice_command(text):
    if "call" in text.lower() or "dial" in text.lower():
        result = phone_ai.process_command(text)
        return result['message']
```

---

## 📋 Features

### ✅ Current Features
- 🧠 AI-powered command understanding (Gemini)
- 📞 Phone Link dialing
- 💬 Interactive chat mode
- 🔄 Fallback to simple parsing (no AI needed)
- 📝 Command history
- 🪟 Windows Phone Link integration
- 📱 Multiple phone number formats
- 🎯 Quick dial shortcuts
- 🔨 Batch file launchers

### 🔮 Future Enhancements
- 📨 SMS message sending
- 📖 Contact name lookup
- 🎤 Voice command integration
- 📞 Call history from Phone Link
- 🔔 Notification handling
- 📱 Screen mirroring control

---

## 🛠️ Troubleshooting

### "AI Engine: ⚠️ Basic mode"
- **Cause:** No Google API key configured
- **Solution:** Set `GOOGLE_API_KEY` environment variable (see Setup section)
- **Note:** Controller still works with simple parsing

### "Phone Link: ❌ Windows only"
- **Cause:** Not running on Windows
- **Solution:** Phone Link only works on Windows 10/11

### "Phone Link doesn't open"
- **Cause:** Phone Link not installed or phone not connected
- **Solution:** 
  1. Install Phone Link from Microsoft Store
  2. Connect your phone
  3. Complete Phone Link setup

### "Number doesn't dial"
- **Cause:** Phone Link permissions
- **Solution:** Check Phone Link has permission to make calls

---

## 🎯 Use Cases

### 1. Voice Assistant Integration
Add to VATSAL voice assistant for hands-free calling

### 2. Emergency Calling
Quick dial emergency contacts with one click

### 3. CRM Integration
Auto-dial customers from your database

### 4. Productivity Automation
Schedule automated reminder calls

### 5. Smart Home Integration
"Call the front desk when someone rings doorbell"

---

## 📊 Architecture

```
User Command
    ↓
AI Understanding (Gemini)
    ↓
Command Parser
    ↓
Phone Dialer Module
    ↓
Phone Link (tel: URI)
    ↓
Your Phone Dials
```

---

## 🔐 Privacy & Security

- ✅ All processing happens locally
- ✅ No call recording or logging (except local history)
- ✅ API keys stored in environment variables
- ✅ No data sent to third parties (except Gemini API for text processing)
- ✅ Command history stored only in memory

---

## 📚 API Reference

### AIPhoneLinkController

#### Methods:

**`process_command(user_input: str) -> Dict`**
- Process natural language command
- Returns: Execution result

**`quick_dial(phone_number: str) -> Dict`**
- Direct dial without AI parsing
- Returns: Dial result

**`interactive_mode()`**
- Start interactive chat mode

**`understand_command(user_input: str) -> Dict`**
- Parse command with AI
- Returns: Parsed action and parameters

**`execute_phone_command(command: Dict) -> Dict`**
- Execute parsed command
- Returns: Execution result

**`get_history(limit: int = 5) -> List`**
- Get recent command history

---

## 🎓 Examples

### Example 1: Emergency Contact System
```python
controller = AIPhoneLinkController()

emergency_contacts = {
    "mom": "+1234567890",
    "dad": "+1234567891",
    "911": "911"
}

def emergency_dial(contact_name):
    number = emergency_contacts.get(contact_name.lower())
    if number:
        return controller.quick_dial(number)
    return {"success": False, "message": "Contact not found"}

# Usage
emergency_dial("mom")
```

### Example 2: Scheduled Calls
```python
import schedule
import time

controller = AIPhoneLinkController()

def daily_reminder_call():
    controller.quick_dial("+1234567890")

# Call every day at 9 AM
schedule.every().day.at("09:00").do(daily_reminder_call)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Example 3: CRM Integration
```python
controller = AIPhoneLinkController()

def call_customer(customer_id):
    # Fetch from database
    customer = db.get_customer(customer_id)
    
    # Dial
    result = controller.process_command(f"Call {customer['name']} at {customer['phone']}")
    
    # Log call
    db.log_call(customer_id, result)
    
    return result
```

---

## 🆚 Comparison

| Feature | AI Controller | Basic Phone Dialer |
|---------|--------------|-------------------|
| **Natural Language** | ✅ Yes | ❌ No |
| **AI Understanding** | ✅ Gemini | ❌ N/A |
| **Interactive Mode** | ✅ Yes | ❌ No |
| **Batch Files** | ✅ Yes | ⚠️ Limited |
| **Command History** | ✅ Yes | ❌ No |
| **Flexibility** | ✅ High | ⚠️ Medium |

---

## 📞 Support

For issues or questions:
1. Check `PHONE_LINK_DIAL_GUIDE.md`
2. Run test files: `test_phone_link_simple.py`
3. Check VATSAL AI documentation

---

**Made with ❤️ for VATSAL AI System**

Enjoy AI-powered phone control! 🚀📱
