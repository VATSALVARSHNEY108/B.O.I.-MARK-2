# 🤖 BOI (Barely Obeys Instructions) - Advanced Desktop Automation System

> **Intelligent AI-powered desktop automation with 300+ features**

[![Status](https://img.shields.io/badge/Status-Production%20Ready-success)]()
[![Python](https://img.shields.io/badge/Python-3.11+-blue)]()
[![Gemini](https://img.shields.io/badge/Gemini-2.5--flash-orange)]()
[![Organization](https://img.shields.io/badge/Project-Organized-green)]()

---

## ✨ Features Overview

- 🤖 **AI Code Generation** with Gemini (404 error fixed!)
- 🖥️ **Desktop Automation** via PyAutoGUI
- 🎙️ **Voice Commands** with advanced NLU
- 📊 **Smart Screen Monitoring** with AI analysis
- 💬 **WhatsApp & Email Automation**
- 🎵 **Spotify & YouTube Control**
- 🔐 **Advanced Security** with 2FA & biometric auth
- 📈 **Productivity Dashboard** with AI insights
- 🌐 **WebSocket Real-time Monitoring**
- 📱 **Mobile Companion App**
- And **290+ more features**!

---

## 🗂️ Project Structure

```
BOI-AI/
├── modules/           # All Python code (organized by category)
├── tests/             # All test files (31 tests)
├── docs/              # All documentation (98 docs)
├── config/            # Configuration files
├── scripts/           # Utility scripts
├── data/              # Runtime data
└── [root]/            # Main entry points
```

**📖 See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for complete details**

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r docs/requirements.txt
```

### 2. Set Up Gemini API Key
```bash
export GEMINI_API_KEY='your-api-key-here'
```

### 3. Run BOI AI
```bash
# GUI Mode
python vnc_web_viewer.py

# CLI Mode  
python -m modules.core.main

# Chatbot Mode
python vatsal_chatbot.py
```

---

## 🎯 Key Features by Category

### 🤖 AI Features
- **Code Generation** → Automatically write code in 10+ languages
- **Screen Analysis** → AI understands what's on your screen
- **Natural Language** → Talk to your computer naturally
- **Learning System** → Learns from corrections

### 🔧 Automation
- **Desktop Control** → Full desktop automation
- **Macro Recording** → Record and replay actions
- **File Management** → Smart file organization
- **Web Automation** → Automate web tasks

### 📊 Monitoring
- **Screen Monitoring** → AI-powered screen analysis
- **Activity Tracking** → Track productivity
- **Chat Monitoring** → Monitor WhatsApp/Email
- **System Monitoring** → CPU, memory, disk usage

### 🧠 Intelligence
- **Memory System** → Remembers conversations
- **Learning Engine** → Improves over time
- **Predictive Actions** → Suggests next actions
- **Desktop RAG** → Search your files with AI

---

## 💡 Special Features

### ✅ Gemini Code Generator (Recently Fixed!)

Generate code and automatically write it to Notepad:

```bash
# Run the demo
python gemini_code_generator/scripts/demo_gemini_to_notepad.py

# Or quick script
python gemini_code_generator/scripts/simple_gemini_notepad.py
```

**What it does:**
1. You describe what code you want
2. Gemini AI generates clean, commented code
3. Notepad opens automatically
4. Code is typed into Notepad

**Supported languages:** Python, JavaScript, Java, C, C++, C#, Ruby, Go, HTML, CSS

**📖 Read more:** [gemini_code_generator/docs/README_GEMINI_INTEGRATION.md](gemini_code_generator/docs/README_GEMINI_INTEGRATION.md)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Complete project organization |
| [docs/COMPREHENSIVE_SYSTEM_SUMMARY.md](docs/COMPREHENSIVE_SYSTEM_SUMMARY.md) | Full system documentation |
| [docs/QUICK_START_COMPREHENSIVE_CONTROL.md](docs/QUICK_START_COMPREHENSIVE_CONTROL.md) | Getting started guide |
| [docs/FEATURES_GUIDE.md](docs/FEATURES_GUIDE.md) | All features explained |
| [docs/CODE_GENERATION_GUIDE.md](docs/CODE_GENERATION_GUIDE.md) | Code generation guide |

**📁 All documentation is in the [docs/](docs/) folder**

---

## 🛠️ Technology Stack

- **Language:** Python 3.11+
- **AI:** Google Gemini 2.5-flash
- **GUI:** Tkinter
- **Automation:** PyAutoGUI
- **Voice:** SpeechRecognition, pyttsx3
- **Web:** Flask, SocketIO
- **Data:** pandas, numpy, scikit-learn

---

## 🎓 Module Categories

| Category | Files | Purpose |
|----------|-------|---------|
| **core** | 7 | Main application logic |
| **ai_features** | 8 | AI & code generation |
| **automation** | 10 | Desktop automation |
| **monitoring** | 8 | Screen & activity monitoring |
| **intelligence** | 7 | Memory & learning |
| **communication** | 6 | Messaging & email |
| **utilities** | 9 | Spotify, YouTube, etc. |
| **web** | 4 | Web automation |
| **system** | 3 | System control |
| **security** | 5 | Security features |
| **productivity** | 8 | Productivity tools |
| **file_management** | 4 | File operations |
| **voice** | 3 | Voice assistant |
| **network** | 5 | WebSocket & mobile |
| **smart_features** | 6 | Smart automation |
| **integration** | 7 | Integration modules |
| **data_analysis** | 2 | Data analysis |
| **development** | 3 | Dev tools |
| **misc** | 4 | Miscellaneous |

**Total:** 110 Python modules across 19 categories

---

## 🧪 Testing

Run all tests:
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_gemini_fix.py
```

**Total:** 31 test files

---

## 📊 Project Stats

- **Python Modules:** 110 organized files
- **Test Files:** 32 files
- **Documentation:** 98 files
- **Config Files:** 15
- **Utility Scripts:** 11
- **Features:** 300+
- **Lines of Code:** 50,000+
- **Organization:** ✅ 100% Complete!

---

## 🔧 Configuration

All configuration files are in [config/](config/):

- `system_config.json` - System settings
- `vatsal_user_profile.json` - User preferences
- `productivity_config.json` - Productivity settings
- And more...

---

## 🤝 Contributing

This is a personal AI assistant project. Feel free to fork and customize!

---

## 📝 Recent Updates

### ✅ October 31, 2025
- **Fixed:** Gemini 404 error (updated to gemini-2.5-flash)
- **Added:** Smart multi-model fallback system
- **Organized:** Entire project into structured folders (265+ files)
- **Structured:** 110 modules into 19 logical categories
- **Centralized:** All tests (32), docs (98), configs (15), scripts (11)
- **Created:** Comprehensive documentation
- **Status:** 100% organized and production ready!

---

## 📞 Support

For detailed information about any feature:
1. Check [docs/](docs/) folder
2. See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
3. Read feature-specific guides

---

## 📜 License

Personal project - All rights reserved

---

## 🎉 Status

✅ **Production Ready**
✅ **Fully Organized**
✅ **Well Documented**
✅ **Actively Maintained**

---

**Built with ❤️ using Python & Google Gemini AI**

*Last Updated: October 31, 2025*
