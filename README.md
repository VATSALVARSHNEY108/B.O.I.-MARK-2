# AI Desktop Automation Controller

An **incredibly intelligent** desktop automation tool powered by Google's Gemini AI with **50+ features** including AI Vision, system monitoring, advanced file management, code execution, and workflow automation. Control your computer with natural language!

## Features

### 🤖 AI Code Generation (Comprehensive!)
- **Write Code Automatically**: Just describe what you want - "Write code for checking palindrome"
- **Auto-Language Detection**: Automatically detects language from your description
- **10+ Programming Languages**: Python, JavaScript, Java, C, C++, C#, Ruby, Go, HTML, CSS
- **Auto-Type to Editor**: Generates code and types it directly into notepad or any text editor
- **Smart & Educational**: Includes detailed comments and best practices
- **Code Explanation**: Understand what any code does
- **Code Improvement**: Get optimized versions of existing code
- **Code Debugging**: Fix errors automatically
- **Clean Output**: Removes markdown formatting automatically
- **Examples**:
  - "Write code for checking palindrome"
  - "Generate bubble sort algorithm"
  - "Create JavaScript code for form validation"
  - "Explain this code: [your code]"
  - "Improve this code: [your code]"

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
- **YouTube Integration**: Search and play YouTube videos
- **File Operations**: Create files with content

### 📱 Messaging & Communication (Advanced)
- **SMS Messaging**: Send text messages to contacts via Twilio
- **Email**: Send emails with attachments via Gmail
- **File Sharing**: Send photos and files to contacts
- **Contact Management**: Store and manage contact information
- **Natural Language**: "Send this photo to John" or "Text Sarah I'm on my way"

### 🔧 Built With
- **Gemini AI** (gemini-2.0-flash-exp) for natural language understanding and code generation
- **Tkinter** for the beautiful GUI interface
- **PyAutoGUI** for GUI automation
- **Pyperclip** for clipboard operations
- **Python 3.11**

## Usage

### GUI Version (Recommended)
Run the beautiful graphical interface:
```bash
python gui_app.py
```

Features:
- 🎨 Modern dark theme interface
- 💡 Quick example buttons
- 📋 Real-time output display
- ⚡ Easy-to-use command input
- 🔘 Help, Contacts, and Clear buttons

### CLI Version
Run the command-line interface:
```bash
python main.py
```

### Example Commands

**AI Code Generation (NEW!):**
- "Write code for checking palindrome"
- "Generate Python code for bubble sort algorithm"
- "Create JavaScript code for a calculator"
- "Write Java code for fibonacci sequence"
- "Generate C++ code for binary search"

**Simple Actions:**
- "Open notepad"
- "Type Hello World"
- "Take a screenshot"
- "Press enter"
- "Search Google for Python tutorials"
- "Search YouTube for funny cats"
- "Play music video on YouTube"
- "Open YouTube video [video URL]"

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
