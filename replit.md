# AI Desktop Automation Controller

## Overview
The AI Desktop Automation Controller is an intelligent desktop automation tool powered by Google's Gemini AI. It interprets natural language commands to execute a wide range of tasks on desktop computers. The project aims to be a comprehensive productivity powerhouse, offering a unified ecosystem with over 300+ features, including smart Desktop RAG, 9 Smart Automation & AI features, Natural Language Workflow Builder, 8 Communication Enhancement features, and a real-time WebSocket dashboard for live monitoring. It integrates advanced AI for code generation, screen analysis, natural language understanding, professional-grade data analysis, various utility modules, and real-time remote monitoring capabilities.

## User Preferences
- **Chat Monitoring:** User prefers visual/screen-based chat monitoring where AI controls the real Gmail/WhatsApp interface on screen, rather than background API calls. This allows them to watch the AI work in real-time.

## System Architecture
The AI Desktop Automation Controller is built with Python 3.11 and utilizes a modular architecture, enabling a wide range of desktop automation and AI-powered functionalities.

### UI/UX Decisions
The primary interface is a GUI application (`gui_app.py`) built with `tkinter`, featuring a modern, dark-themed, tabbed design. It includes a live clock, card-based design with gradient effects, quick-access buttons, and a real-time color-coded output console. A CLI interface (`main.py`) provides an interactive command-line alternative. The GUI integrates toggle buttons for "VATSAL Mode" (personality vs. direct responses) and "Self-Operating Mode" (autonomous control).

### Technical Implementations
- **AI Command Processing:** Gemini AI is integrated for natural language processing and converting commands into actions (`gemini_controller.py`).
- **AI Code Generation → Notepad:** Integrated Gemini AI-powered code generator that automatically generates clean, well-commented code in 10+ languages and writes it to Notepad automatically. Features smart template system for instant code generation of common algorithms, auto-language detection, and multi-language support (`code_generator.py`, `code_templates.py`).
- **GUI Automation:** Uses `PyAutoGUI` for cross-platform desktop control (`gui_automation.py`).
- **AI Vision Module:** Leverages Gemini Vision for OCR, UI element identification, and screen analysis (`screenshot_analyzer.py`).
- **Desktop RAG System:** Indexes desktop files for semantic search and Q&A (`desktop_rag.py`).
- **Smart Automation & AI:** Provides 9 AI-powered features (e.g., Auto-Bug Fixer, Meeting Scheduler AI) (`smart_automation.py`).
- **Visual Chat Monitor:** AI-powered visual email/WhatsApp monitoring via real browser interface control (`visual_chat_monitor.py`).
- **System Control:** Manages system-level automation including lock screen, shutdown, restart, brightness, volume, and disk cleanup (`system_control.py`).
- **Voice Assistant:** An ultra-intelligent, interactive voice commanding system with advanced AI capabilities, supporting multiple wake words, NLU, context awareness, and entity extraction (`voice_assistant.py`).
- **Self-Operating Computer:** Autonomous AI desktop control using Gemini Vision (Gemini 2.0 Flash Exp) for screen analysis and autonomous actions, with improved decision making, OCR, and error recovery (`self_operating_computer.py`).
- **Real-Time WebSocket System:** A Flask-SocketIO based server (`websocket_server.py`) provides a live dashboard (`templates/dashboard.html`) for real-time monitoring of system stats and command execution, supporting multi-client connections and remote access.
- **Mobile Companion System:** Offers complete mobile control via a REST API (`mobile_api.py`) and a touch-optimized web interface (`templates/mobile.html`), including PIN-based authentication, push notifications, remote screenshot viewing, and quick actions.
- **Automation Recording & Macro System:** Professional macro recording and playback for mouse clicks, movements, scrolls, and keyboard events, with loop support, speed control, and macro management (`macro_recorder.py`).
- **Natural Language Workflow Builder:** AI-powered workflow creation from plain English descriptions. Users can describe complex automation workflows in natural language, and the AI (Gemini 2.0 Flash) converts them into executable automation steps. Features include conversational refinement, workflow validation, reusable templates, and integration with the existing WorkflowManager (`nl_workflow_builder.py`, `workflow_templates.py`).
- **Advanced AI Enhancements:** Integrates Multi-Modal AI (vision + voice + text), Enhanced Contextual Memory, a Correction Learning System, and a Predictive Actions Engine for next-generation intelligence and learning (`multimodal_ai_core.py`, `contextual_memory_enhanced.py`, `correction_learning.py`, `predictive_actions_engine.py`).
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