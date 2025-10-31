# Chatbot Organization

The chatbot files have been organized into separate folders for better project structure.

## New Structure

```
📁 Project Root
│
├── 📁 simple_chatbot/
│   ├── simple_chatbot.py          # Enhanced VATSAL Chatbot with commands
│   └── README.md
│
├── 📁 vatsal_chatbot/
│   ├── vatsal_chatbot.py          # VATSAL AI CLI Chatbot
│   └── README.md
│
├── 📁 vatsal_desktop/
│   ├── vatsal_desktop_automator.py # Desktop Automation Tool
│   └── README.md
│
└── 🚀 launch_gui.py               # Main GUI Application Launcher
```

## How to Use

### Launch the Main GUI Application
To open the full VATSAL AI Desktop Automation GUI with all features:

```bash
python launch_gui.py
```

or

```bash
python3 launch_gui.py
```

### Run Individual Chatbots

**Simple Chatbot:**
```bash
cd simple_chatbot
python simple_chatbot.py
```

**VATSAL Chatbot:**
```bash
cd vatsal_chatbot
python vatsal_chatbot.py
```

**Desktop Automator:**
```bash
cd vatsal_desktop
python vatsal_desktop_automator.py
```

## What Each Does

### 🤖 Simple Chatbot
- Chat naturally with AI
- Execute automation commands
- Open apps, folders, and files
- System control and monitoring

### 💬 VATSAL Chatbot
- Intelligent conversation AI
- Context-aware responses
- Session management
- Statistics tracking

### 🖥️ Desktop Automator
- Desktop automation
- System control (lock, shutdown, restart)
- File management
- Screenshot capabilities
- Mouse and keyboard control

### 🎨 GUI Application (Main App)
- Full-featured GUI interface
- All automation features
- Visual controls and monitoring
- Modern dark-themed interface

## Requirements
- Python 3.x
- GEMINI_API_KEY in environment variables
- All dependencies installed (see requirements)
