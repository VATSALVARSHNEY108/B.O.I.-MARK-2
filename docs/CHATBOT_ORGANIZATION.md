# Chatbot Organization

The chatbot files have been organized into separate folders for better project structure.

## New Structure

```
📁 Project Root
│
├── 📁 simple_chatbot/
│   ├── simple_chatbot.py          # Enhanced BOI Chatbot with commands
│   └── README.md
│
├── 📁 vatsal_chatbot/
│   ├── vatsal_chatbot.py          # BOI (Barely Obeys Instructions) CLI Chatbot
│   └── README.md
│
├── 📁 vatsal_desktop/
│   ├── vatsal_desktop_automator.py # Desktop Automation Tool
│   └── README.md
│
├── 📁 vnc_tools/
│   ├── vnc_web_viewer.py          # Web-based VNC viewer
│   ├── start_gui_with_vnc.sh      # Launch GUI with VNC
│   └── README.md
│
├── 📁 test_data/
│   ├── test_sample_data.csv       # Sample test data
│   └── README.md
│
└── 🚀 launch_gui.py               # Main GUI Application Launcher
```

## How to Use

### Launch the Main GUI Application
To open the full BOI (Barely Obeys Instructions) Desktop Automation GUI with all features:

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

**BOI Chatbot:**
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

### 💬 BOI Chatbot
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

### 🖥️ VNC Tools
- Web-based VNC viewer for remote access
- Script to launch GUI with VNC support
- Advanced remote desktop capabilities

### 📊 Test Data
- Sample CSV files for testing
- Data analysis testing
- File processing validation

## Requirements
- Python 3.x
- GEMINI_API_KEY in environment variables
- All dependencies installed (see requirements)

## Benefits of This Organization
✅ **Clean Root Directory** - Only the main launcher in root  
✅ **Easy to Find** - Related files grouped together  
✅ **Better Navigation** - Clear folder structure  
✅ **Documentation** - Each folder has its own README  
✅ **Simple Launch** - Just run `python launch_gui.py` to start
