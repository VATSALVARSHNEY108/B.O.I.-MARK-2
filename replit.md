# AI Desktop Automation Controller

## Overview
The AI Desktop Automation Controller is an intelligent desktop automation tool powered by Google's Gemini AI. It interprets natural language commands to execute a wide range of tasks on desktop computers. The project aims to be a comprehensive productivity powerhouse, offering a unified ecosystem with over 410+ features, including a Comprehensive Windows 11 Settings Controller (100+ functions), smart Desktop RAG, 9 Smart Automation & AI features, Natural Language Workflow Builder, 8 Communication Enhancement features, 7 essential utility tools, and a real-time WebSocket dashboard for live monitoring. It integrates advanced AI for code generation, screen analysis, natural language understanding, professional-grade data analysis, various utility modules, and real-time remote monitoring capabilities, including an Intelligent AI Assistant.

## User Preferences
-   **Interface:** User prefers desktop GUI interfaces only - NO web-based interfaces. Project uses tkinter-based GUIs (gui_app.py, enhanced_gui.py) for local desktop use.
-   **Chat Monitoring:** User prefers visual/screen-based chat monitoring where AI controls the real Gmail/WhatsApp interface on screen, rather than background API calls. This allows them to watch the AI work in real-time.
-   **File Structure:** Well-organized modular architecture with modules/ directory containing core, voice, automation, ai_features, utilities, etc.
-   **Desktop Path:** User's Desktop is located at `C:/Users/VATSAL VARSHNEY/OneDrive/Desktop` (configured in config/desktop_structure.json). System uses forward slashes for cross-platform compatibility and to avoid Windows path escape character issues.
-   **Direct Access:** User prefers having direct batch file access to individual features for instant control without going through menus or the main application.

## System Architecture
The AI Desktop Automation Controller is built with Python 3.11 and utilizes a modular architecture.

### UI/UX Decisions
The system offers desktop GUIs built with `tkinter` featuring a light cream background with Slate gray accents and multi-layer shadow effects. A "Modern Web GUI" is built with Flask and Flask-SocketIO. A CLI interface is available for headless environments.

### Technical Implementations
-   **AI Command Processing:** Gemini AI for natural language understanding, action conversion, code generation, and professional letter generation.
-   **GUI Automation:** Uses `PyAutoGUI` for cross-platform desktop control.
-   **AI Vision Module:** Leverages Gemini Vision for OCR, UI element identification, and screen analysis.
-   **Desktop RAG System:** Indexes desktop files for semantic search and Q&A.
-   **Smart Automation & AI:** 9 AI-powered features.
-   **Visual Chat Monitor:** AI-powered visual email/WhatsApp monitoring via real browser interface control.
-   **System Control:** Manages system-level automation (lock, shutdown, restart, brightness, volume, disk cleanup, system info, clipboard, power, window management, process management).
-   **Windows 11 Settings Controller:** Comprehensive control over all Windows 11 settings with 100+ functions covering Display, Sound, Network, Bluetooth, Privacy & Security, Personalization, System, Accessibility, Windows Update, Apps & Startup, Time & Language, Gaming, Power Plans, and Advanced System Settings. Integrates PowerShell and Registry. Bluetooth control uses Windows Runtime Radio API for reliable operation.
-   **Quick Access Batch Files:** 44 individual batch files in `batch_scripts/quick_access/` for direct feature access including Bluetooth (on/off/status), WiFi (on/off/status), Volume controls (up/down/mute/presets), Brightness controls (up/down/presets), Power options (shutdown/restart/sleep/hibernate/lock with confirmations), System monitoring (CPU/RAM/disk/battery/network), and Quick app launchers. Includes master menu (QUICK_ACCESS_MENU.bat) and comprehensive README documentation.
-   **Voice Assistant with Personality:** Interactive voice commanding system with empathetic responses, wake word detection, context awareness, and adaptive feedback via a PersonaResponseService.
-   **Face & Gesture Assistant:** Computer vision (OpenCV, MediaPipe) for face and hand gesture recognition to activate voice listening.
-   **Self-Operating Computer:** Autonomous AI desktop control using Gemini Vision for screen analysis and actions.
-   **Real-Time WebSocket System:** Flask-SocketIO server for live monitoring dashboard.
-   **Mobile Companion System:** Complete mobile control via REST API and touch-optimized web interface.
-   **Automation Recording & Macro System:** Professional macro recording and playback.
-   **Natural Language Workflow Builder:** AI-powered workflow creation from natural language descriptions using Gemini 2.0 Flash.
-   **Advanced AI Enhancements:** Multi-Modal AI, Enhanced Contextual Memory, Correction Learning System, and Predictive Actions Engine.
-   **AI-Powered Security Dashboard:** Gemini AI-powered security management with biometric auth, 2FA, encrypted storage, and threat analysis.
-   **Batch Form Filler System:** Comprehensive form automation for web (Selenium) and desktop (PyAutoGUI) with intelligent field detection.
-   **Hand Gesture Mouse Controller:** Touchless computer control using webcam and MediaPipe hand tracking.
-   **Batch Utilities System:** Comprehensive Python implementation of 20+ batch file utilities with GUI integration.
-   **Windows 11 Settings Batch Files:** Complete automation suite with 9 specialized batch modules for controlling all major Windows 11 settings.
-   **AI Phone Link Controller:** Gemini AI-powered Windows Phone Link automation for natural language phone control.
-   **Utility Modules:** Integrations for Spotify, YouTube, Weather & News, Translation, Calculator, Password Vault, Quick Notes, Calendar Manager, Timer & Stopwatch, Quick Reminders, Habit Tracker, Color Tools, QR Code Tools, Screenshot Annotator, Image Resizer, Batch Form Filler, and Hand Gesture Controller.
-   **AI Performance Optimizations:** Implemented response caching, model fallback, retry optimization, token limit tuning, and generation config adjustments.
-   **WhatsApp Automation:** Comprehensive batch and individual messaging systems for WhatsApp, including personalized templates, image sending, scheduling, and full contact management.
-   **Phone Link Notification Monitor:** System for monitoring and parsing Windows Action Center notifications from Phone Link.
-   **Contact-Based Calling:** Full contact management system with name-based calling integrated with Phone Link.

## Recent Changes (November 25, 2025)
-   **🌟 FUTURE-TECH CORE SYSTEM:** Created the ultimate AI desktop automation system combining all cutting-edge features. Includes: AI Vision Screen Understanding, Predictive Action Engine, Holographic Memory System (remembers everything), Quantum-Fast Search, Multi-Modal Input Fusion, Emotion & Context Detection, Autonomous Task Completion, Real-Time Translation, Biometric Awareness, and Smart Recall Engine. Integrates with all existing BOI modules for unprecedented intelligence. Launch with `batch_scripts\launch_future_tech.bat` or `python demos/demo_future_tech_core.py`. Full guide at `docs/FUTURE_TECH_GUIDE.md`.
-   **Phone Link Auto-Call Fix with Calibration:** Fixed Phone Link call button clicking. Saved exact coordinates (X=1670, Y=893) in `config/phone_link_button.json`. Implemented multi-strategy approach: (1) Calibrated position (primary), (2) Visual button detection, (3) OCR text recognition, (4) Multiple estimated positions. Created calibration tool at `scripts/calibrate_phone_link_button.py` for finding exact button position on any screen.
-   **Major Cleanup:** Removed 18 redundant directories (web_gui, simple_chatbot, vatsal_chatbot, vatsal_desktop, vnc_tools, gemini_code_generator, notebooks, sandbox_environment, encrypted_storage, security_dashboard, smart_templates, auto_generated_docs, 2fa_data, activity_monitoring, macros, screenshots, static, templates) and 100+ unnecessary markdown files.
-   **Weather Service Enhancement:** Fixed weather timeout issues by increasing timeout from 5s to 15s, adding 3-attempt retry logic with delays, specific error handling for timeout/connection errors, and formatted error messages. Weather service now much more reliable.
-   **YouTube Integration:** Added Selenium-based YouTube video playing in GUI with search functionality and quick action buttons, replacing unreliable screen coordinate clicking.
-   **WebDriver Management:** Installed webdriver-manager for automatic ChromeDriver management (Selenium features require Google Chrome).

## External Dependencies
-   **google-genai:** For Gemini AI integration.
-   **PyAutoGUI:** For GUI automation.
-   **pyperclip:** For clipboard operations.
-   **psutil:** For system monitoring.
-   **python-dotenv:** For environment variable management.
-   **Flask & Flask-SocketIO:** For real-time WebSocket dashboard and mobile companion API.
-   **Twilio:** For SMS messaging and phone calls.
-   **Gmail SMTP:** For email sending.
-   **watchdog:** For real-time file system monitoring.
-   **speechrecognition & pyttsx3:** For voice commands and text-to-speech.
-   **cryptography:** For encryption.
-   **requests:** For HTTP API calls.
-   **Replit Spotify Connector:** For Spotify API integration.
-   **wttr.in API:** For weather data (with 15s timeout and 3-attempt retry logic).
-   **Google Translate API:** For language translation.
-   **opencv-python:** For screen monitoring, image analysis, and webcam capture.
-   **MediaPipe:** For hand tracking and gesture recognition.
-   **Data Science Libraries:** pandas, numpy, scikit-learn, matplotlib, seaborn, statsmodels, nltk, openpyxl.
-   **Image Processing:** Pillow (PIL), qrcode, pyzbar.
-   **Selenium & webdriver-manager:** For web automation, intelligent form filling, and YouTube integration.