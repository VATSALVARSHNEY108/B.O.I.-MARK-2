# AI Desktop Automation Controller

An intelligent desktop automation tool powered by Google's Gemini AI that understands natural language commands and executes them on your computer.

## Features

### 🎯 Natural Language Control
- Issue commands in plain English - no coding required
- AI-powered command interpretation using Gemini
- Multi-step workflow automation

### 🖥️ Desktop Automation Capabilities
- **Application Control**: Open and manage applications
- **Text Input**: Type text automatically with customizable speed
- **Mouse Control**: Click, move, and interact with GUI elements
- **Keyboard Actions**: Press keys and key combinations (hotkeys)
- **Screenshots**: Capture screen content
- **Clipboard**: Copy and paste operations
- **Web Search**: Quick web searches
- **File Operations**: Create files with content

### 📱 Messaging & Communication (Advanced)
- **SMS Messaging**: Send text messages to contacts via Twilio
- **Email**: Send emails with attachments via Gmail
- **File Sharing**: Send photos and files to contacts
- **Contact Management**: Store and manage contact information
- **Natural Language**: "Send this photo to John" or "Text Sarah I'm on my way"

### 🔧 Built With
- **Gemini AI** (gemini-2.0-flash-exp) for natural language understanding
- **PyAutoGUI** for GUI automation
- **Pyperclip** for clipboard operations
- **Python 3.11**

## Usage

Run the automation controller:
```bash
python main.py
```

### Example Commands

**Simple Actions:**
- "Open notepad"
- "Type Hello World"
- "Take a screenshot"
- "Press enter"
- "Search Google for Python tutorials"

**Multi-Step Workflows:**
- "Open notepad and type my name"
- "Open chrome and search for weather"
- "Create a file called test.txt with content Hello"

**Messaging Commands (Advanced):**
- "Send this photo to John"
- "Text Sarah that I'm running late"
- "Email my boss about the meeting"
- "Add contact Mom with phone 555-1234 and email mom@example.com"
- Type `contacts` - List all contacts

**Utility Commands:**
- Type `help` - Show available features
- Type `position` - See current mouse coordinates
- Type `exit` or `quit` - Stop the controller

## How It Works

1. You enter a command in natural language
2. Gemini AI parses your command into structured actions
3. The command executor performs the actions using PyAutoGUI
4. You receive feedback on success or failure

## Safety Features

- **Failsafe**: Move mouse to corner to emergency stop
- **Error Handling**: Informative error messages
- **Validation**: Commands are validated before execution

## Requirements

- Python 3.11+
- Gemini API Key (configured in environment)
- Desktop environment (Linux, macOS, or Windows)

**Optional (for Messaging Features):**
- **Twilio Account** (for SMS): Set `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_PHONE_NUMBER`
- **Gmail Account** (for Email): Set `GMAIL_USER` (your email) and `GMAIL_APP_PASSWORD` 
  - Gmail App Password setup: https://support.google.com/accounts/answer/185833
  - Regular Gmail passwords won't work - you need an app-specific password

## Notes

- The controller works on Linux, macOS, and Windows
- Some actions may require appropriate permissions
- Mouse coordinates can be found using the `position` command
- For complex workflows, describe all steps in one command
