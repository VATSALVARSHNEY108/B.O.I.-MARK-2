# AI Desktop Automation Controller

## Overview
The AI Desktop Automation Controller is an intelligent desktop automation tool powered by Google's Gemini AI. It interprets natural language commands to execute a wide range of tasks on desktop computers. The project aims to be a comprehensive productivity powerhouse, offering a unified ecosystem with over 300+ features, including smart Desktop RAG, 9 Smart Automation & AI features, Natural Language Workflow Builder, 8 Communication Enhancement features, and a real-time WebSocket dashboard for live monitoring. It integrates advanced AI for code generation, screen analysis, natural language understanding, professional-grade data analysis, various utility modules, and real-time remote monitoring capabilities.

**NEW:** Now includes an Intelligent AI Assistant (integrated in `modules/ai_features/chatbots.py`) - a Streamlit-based web interface that instantly understands user intent and generates appropriate responses (code, stories, explanations, letters, etc.) with no unnecessary commentary.

## Recent Changes
**November 4, 2025 - Windows Batch Files for Volume & Brightness**:
- **🪟 Windows Batch File Controls** (`scripts/windows_controls/`): Created comprehensive Windows batch files for easy volume and brightness control using `nircmd.exe`:
  - `windows_volume_brightness_control.bat` - Interactive menu with preset levels, custom input, and toggle options
  - `quick_volume_control.bat` - Command-line volume control (set, up, down, mute, get)
  - `quick_brightness_control.bat` - Command-line brightness control
  - `WINDOWS_BATCH_FILES_README.md` - Complete documentation with usage examples and troubleshooting
- **✅ Linux Volume Control Verified**: Confirmed working volume control on Linux using `pactl` commands for PulseAudio

**November 2, 2025 - Enhanced Black & White GUI**:
- **⚫⚪ Enhanced Black & White GUI** (`modules/core/enhanced_gui.py`): Completely redesigned GUI with pure black backgrounds (#000000), crisp white borders (2px) on every element, and command prompt bar at bottom. Features include neon green/cyan/pink accents, terminal-style prompt (>>> with Consolas font), real-time command execution, dashboard with stats, sidebar navigation, 6 major views, and professional high-contrast appearance. Launch with `python launch_enhanced_gui.py`.
- **⚡ Command Prompt Bar**: NEW terminal-style command bar at bottom with green >>> prompt, direct command execution, real-time status updates, and Enter key support.
- **📝 Fullscreen Notepad Enhancement** (`modules/utilities/notepad_writer.py`): Improved notepad writer to open in TRUE fullscreen mode before writing. Uses two-step process (maximize + F11) with better timing for smooth transitions and professional appearance.

**November 2, 2025 - New Features**:
- **🖼️ AI Screenshot Analysis Module** (`modules/ai_features/screenshot_analysis.py`): Dedicated module for AI-powered screenshot analysis with Google Gemini Vision. Features include error detection, code analysis, UI/UX improvement suggestions, design analysis, and OCR text extraction.
- **🚀 Fullscreen App Automation** (`modules/automation/fullscreen_automation.py`): Cross-platform automation that opens applications in fullscreen mode and performs automated actions. Supports keyboard/mouse automation, window management, and screenshot capture.
- **🤖 Smart App Automation** (`modules/automation/smart_app_automation.py`): Intelligent automation that combines fullscreen app opening with AI screenshot analysis. Can automatically open apps, capture screenshots, analyze them with AI, perform automated actions, and provide continuous monitoring.
- **📝 Screenshot Analyzer Module** (`screenshot_analyzer.py`): Backward-compatible module that re-exports screenshot analysis functions with lazy imports to avoid circular dependencies.

**November 2, 2025 - Code Organization**: Consolidated `modules/ai_features/` directory from 12 files to 6 files for better code organization and maintainability:
- **chatbots.py** (17K): Merged `simple_chatbot.py` + `intelligent_assistant.py` - All chatbot implementations
- **code_generation.py** (43K): Merged `code_generator.py` + `code_templates.py` + `letter_templates.py` - Code and letter generation
- **vision_ai.py** (50K): Merged `multimodal_ai_core.py` + `screenshot_analyzer.py` + `virtual_language_model.py` - Vision and multimodal AI
- **automation_ai.py** (27K): Merged `advanced_ai_automation.py` + `advanced_ai_integration.py` - Advanced automation features
- **ai_features.py** (59K): Main AI features class (unchanged)
- **__init__.py**: Updated with proper exports for all consolidated modules

## User Preferences
- **Chat Monitoring:** User prefers visual/screen-based chat monitoring where AI controls the real Gmail/WhatsApp interface on screen, rather than background API calls. This allows them to watch the AI work in real-time.

## System Architecture
The AI Desktop Automation Controller is built with Python 3.11 and utilizes a modular architecture, enabling a wide range of desktop automation and AI-powered functionalities.

### UI/UX Decisions
The system now offers TWO GUI options:
1. **Original GUI** (`gui_app.py`): Comprehensive feature-rich interface with tabbed design, live clock, quick-access buttons, and real-time console output.
2. **Enhanced Modern GUI** (`enhanced_gui.py`): Beautiful redesigned interface with modern dark theme, dashboard with live statistics, sidebar navigation, 6 major views, stunning color palette (#0a0e27 navy blue backgrounds, #667eea purple-blue accents), hover effects, and professional appearance. Launch with `python launch_enhanced_gui.py`.

Both GUIs are built with `tkinter` and support VATSAL Mode, Self-Operating Mode, and comprehensive automation features. The Enhanced GUI provides a more polished, organized, and visually appealing experience. A CLI interface (`main.py`) also provides an interactive command-line alternative.

### Technical Implementations
- **AI Command Processing:** Gemini AI is integrated for natural language processing and converting commands into actions (`modules/core/gemini_controller.py`).
- **AI Code Generation → Notepad:** Integrated Gemini AI-powered code generator that automatically generates clean, well-commented code in 10+ languages and writes it to Notepad automatically. Features smart template system for instant code generation of common algorithms, auto-language detection, and multi-language support (`modules/ai_features/code_generation.py`).
- **Intelligent Letter Writing System:** Advanced letter generation system with 13 professional letter templates (leave applications, complaints, appreciation, recommendation, resignation, invitations, apologies, job applications, thank you notes, permission requests, inquiries, reference requests, and general formal letters). Features natural language detection, automatic variable extraction from voice commands, customizable templates with smart defaults, and seamless integration with the code generator and Notepad (`modules/ai_features/code_generation.py`).
- **Full Screen Notepad Writer:** Enhanced Notepad integration that automatically opens Notepad in full screen mode before writing any content. Provides better visibility and professional appearance for all generated letters and code. Includes automatic window maximization, formatted titles, and cross-platform support (`notepad_writer.py`).
- **GUI Automation:** Uses `PyAutoGUI` for cross-platform desktop control (`modules/automation/gui_automation.py`).
- **AI Vision Module:** Leverages Gemini Vision for OCR, UI element identification, and screen analysis (`modules/ai_features/vision_ai.py`).
- **Desktop RAG System:** Indexes desktop files for semantic search and Q&A (`desktop_rag.py`).
- **Smart Automation & AI:** Provides 9 AI-powered features (e.g., Auto-Bug Fixer, Meeting Scheduler AI) (`smart_automation.py`).
- **Visual Chat Monitor:** AI-powered visual email/WhatsApp monitoring via real browser interface control (`visual_chat_monitor.py`).
- **System Control:** Manages system-level automation including lock screen, shutdown, restart, brightness, volume, and disk cleanup (`system_control.py`). Cross-platform support for Windows, macOS, and Linux. Windows users can also use standalone batch files for quick volume/brightness control.
- **Voice Assistant:** An ultra-intelligent, interactive voice commanding system with advanced AI capabilities, supporting multiple wake words, NLU, context awareness, and entity extraction (`voice_assistant.py`).
- **Self-Operating Computer:** Autonomous AI desktop control using Gemini Vision (Gemini 2.0 Flash Exp) for screen analysis and autonomous actions, with improved decision making, OCR, and error recovery (`self_operating_computer.py`).
- **Real-Time WebSocket System:** A Flask-SocketIO based server (`websocket_server.py`) provides a live dashboard (`templates/dashboard.html`) for real-time monitoring of system stats and command execution, supporting multi-client connections and remote access.
- **Mobile Companion System:** Offers complete mobile control via a REST API (`mobile_api.py`) and a touch-optimized web interface (`templates/mobile.html`), including PIN-based authentication, push notifications, remote screenshot viewing, and quick actions.
- **Automation Recording & Macro System:** Professional macro recording and playback for mouse clicks, movements, scrolls, and keyboard events, with loop support, speed control, and macro management (`macro_recorder.py`).
- **Natural Language Workflow Builder:** AI-powered workflow creation from plain English descriptions. Users can describe complex automation workflows in natural language, and the AI (Gemini 2.0 Flash) converts them into executable automation steps. Features include conversational refinement, workflow validation, reusable templates, and integration with the existing WorkflowManager (`nl_workflow_builder.py`, `workflow_templates.py`).
- **Advanced AI Enhancements:** Integrates Multi-Modal AI (vision + voice + text), Enhanced Contextual Memory, a Correction Learning System, and a Predictive Actions Engine for next-generation intelligence and learning (`modules/ai_features/vision_ai.py`, `modules/intelligence/contextual_memory_enhanced.py`, `modules/intelligence/correction_learning.py`, `modules/intelligence/predictive_actions_engine.py`).
- **AI-Powered Security Dashboard:** Comprehensive security management powered by Gemini AI, integrating biometric authentication, 2FA, encrypted storage, activity monitoring, and sandbox mode. Features include AI-driven threat analysis, intelligent security recommendations, anomaly detection, natural language security queries, and automated security reporting (`security_dashboard.py`). Accessible through a dedicated "🛡️ Security" button in the GUI with an intuitive dashboard interface.
- **Utility Modules:** Includes integrations for Spotify, YouTube, Weather & News, Translation, Calculator, Password Vault, Quick Notes, and Calendar Manager.

## External Dependencies
- **google-genai:** For Gemini AI integration.
- **PyAutoGUI:** For GUI automation.
- **pyperclip:** For clipboard operations.
- **psutil:** For system monitoring.
- **python-dotenv:** For environment variable management.
- **streamlit:** For web tools application.
- **Twilio:** For SMS messaging.
- **Gmail SMTP:** For email sending.
- **watchdog:** For real-time file system monitoring.
- **speechrecognition & pyttsx3:** For voice commands and text-to-speech.
- **cryptography:** For encryption.
- **requests:** For HTTP API calls.
- **Replit Spotify Connector:** For Spotify API integration.
- **wttr.in API:** For weather data.
- **Google Translate API:** For language translation.
- **opencv-python:** For screen monitoring and image analysis.
- **Data Science Libraries:** pandas, numpy, scikit-learn, matplotlib, seaborn, statsmodels, nltk, openpyxl.