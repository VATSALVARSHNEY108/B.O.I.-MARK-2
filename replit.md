# AI Desktop Automation Controller

## Overview
The AI Desktop Automation Controller is an intelligent desktop automation tool powered by Google's Gemini AI. It interprets natural language commands to execute a wide range of tasks on desktop computers. The project aims to be a comprehensive productivity powerhouse, offering a unified ecosystem with over 410+ features, including the new **Comprehensive Windows 11 Settings Controller** with 100+ settings functions, smart Desktop RAG, 9 Smart Automation & AI features, Natural Language Workflow Builder, 8 Communication Enhancement features, 7 essential utility tools, and a real-time WebSocket dashboard for live monitoring. It integrates advanced AI for code generation, screen analysis, natural language understanding, professional-grade data analysis, various utility modules, and real-time remote monitoring capabilities, including an Intelligent AI Assistant.

## User Preferences
-   **Interface:** User prefers desktop GUI interfaces only - NO web-based interfaces. Project uses tkinter-based GUIs (gui_app.py, enhanced_gui.py) for local desktop use.
-   **Chat Monitoring:** User prefers visual/screen-based chat monitoring where AI controls the real Gmail/WhatsApp interface on screen, rather than background API calls. This allows them to watch the AI work in real-time.
-   **File Structure:** Well-organized modular architecture with modules/ directory containing core, voice, automation, ai_features, utilities, etc.
-   **Desktop Path:** User's Desktop is located at `C:/Users/VATSAL VARSHNEY/OneDrive/Desktop` (configured in config/desktop_structure.json). System uses forward slashes for cross-platform compatibility and to avoid Windows path escape character issues.

## System Architecture
The AI Desktop Automation Controller is built with Python 3.11 and utilizes a modular architecture.

### UI/UX Decisions
The system offers desktop GUIs built with `tkinter` featuring a light cream background with Slate gray accents and beautiful multi-layer shadow effects on all buttons and boxes. The theme uses cream backgrounds (#e8e4dc), white console (#ffffff), Slate 500 borders/accents (#64748b), emerald green execute button (#059669), and light Slate-based shadows. A "Modern Web GUI" is built with Flask and Flask-SocketIO. A CLI interface is available for headless environments.

### Technical Implementations
-   **AI Command Processing:** Gemini AI for natural language understanding and action conversion, code generation, and professional letter generation.
-   **GUI Automation:** Uses `PyAutoGUI` for cross-platform desktop control.
-   **AI Vision Module:** Leverages Gemini Vision for OCR, UI element identification, and screen analysis.
-   **Desktop RAG System:** Indexes desktop files for semantic search and Q&A.
-   **Smart Automation & AI:** 9 AI-powered features for various tasks.
-   **Visual Chat Monitor:** AI-powered visual email/WhatsApp monitoring via real browser interface control.
-   **System Control:** Manages system-level automation (lock, shutdown, restart, brightness, volume, disk cleanup, system info, clipboard, power, window management with close all windows/tabs feature, process management).
-   **Windows 11 Settings Controller:** Comprehensive control over ALL Windows 11 settings with 100+ functions covering Display (resolution, scaling, night light, refresh rate), Sound (spatial audio, device management), Network (WiFi, airplane mode, proxy, DNS, adapters), Bluetooth, Privacy & Security (camera, microphone, location access, Windows Defender, Firewall, telemetry), Personalization (dark mode, wallpaper, accent colors, taskbar, Start menu), System (notifications, focus assist, clipboard history, storage sense, remote desktop), Accessibility (narrator, magnifier, high contrast, sticky keys), Windows Update (check, install, pause/resume), Apps & Startup, Time & Language, Gaming (Game Mode, Xbox Game Bar), Power Plans, and Advanced System Settings (virtual memory, performance optimization). Full PowerShell and Registry integration for native Windows control.
-   **Voice Assistant with Personality:** An ultra-intelligent, interactive voice commanding system with empathetic responses, wake word detection, context awareness, and adaptive feedback. Includes a PersonaResponseService for conversational AI interactions.
-   **Face & Gesture Assistant:** Computer vision (OpenCV, MediaPipe) for face detection and hand gesture recognition to activate voice listening.
-   **Self-Operating Computer:** Autonomous AI desktop control using Gemini Vision for screen analysis and actions.
-   **Real-Time WebSocket System:** Flask-SocketIO server for live monitoring dashboard.
-   **Mobile Companion System:** Complete mobile control via REST API and touch-optimized web interface.
-   **Automation Recording & Macro System:** Professional macro recording and playback.
-   **Natural Language Workflow Builder:** AI-powered workflow creation from natural language descriptions using Gemini 2.0 Flash.
-   **Advanced AI Enhancements:** Multi-Modal AI, Enhanced Contextual Memory, Correction Learning System, and Predictive Actions Engine.
-   **AI-Powered Security Dashboard:** Gemini AI-powered security management with biometric auth, 2FA, encrypted storage, and threat analysis.
-   **Batch Form Filler System:** Comprehensive form automation for web (Selenium) and desktop (PyAutoGUI) with intelligent field detection.
-   **Hand Gesture Mouse Controller:** Touchless computer control using webcam and MediaPipe hand tracking.
-   **Batch Utilities System:** Comprehensive Python implementation of 20+ batch file utilities with GUI integration (e.g., volume, power, battery, file management, network tools, maintenance, Spotify control, window management).
-   **Windows 11 Settings Batch Files:** Complete automation suite with 9 specialized batch modules for controlling all major Windows 11 settings. Includes Display (resolution, orientation, refresh rate, scaling, night light), Sound (volume, spatial audio, devices), Network (WiFi, airplane mode, DNS, proxy), Bluetooth (on/off, pairing), Privacy & Security (camera, mic, location, Defender, firewall, UAC), Personalization (dark mode, themes, taskbar, Start menu), System (notifications, clipboard, storage sense, remote desktop, power), Windows Update (check, install, pause/resume), and Accessibility (narrator, magnifier, high contrast, keyboard/mouse aids). Master controller provides unified access to all modules. Located in `batch_scripts/windows11_settings/`.
-   **AI Phone Link Controller:** Gemini AI-powered Windows Phone Link automation for natural language phone control (interactive chat, quick dialing, command history).
-   **Utility Modules:** Integrations for Spotify, YouTube, Weather & News, Translation, Calculator, Password Vault, Quick Notes, Calendar Manager, Timer & Stopwatch, Quick Reminders, Habit Tracker, Color Tools, QR Code Tools, Screenshot Annotator, Image Resizer, Batch Form Filler, and Hand Gesture Controller.
-   **AI Performance Optimizations:** Implemented response caching, model fallback, retry optimization, token limit tuning, and generation config adjustments.
-   **WhatsApp Automation:** Comprehensive batch messaging and individual messaging systems for WhatsApp, including personalized templates, image sending, scheduling, and full contact management system. Features contact CRUD operations (add/edit/rename/delete), search functionality, import/export CSV, create batch CSV from contacts, automatic contact name resolution in batch messaging, seamless integration across all WhatsApp tools. Fully integrated with command executor for voice control. Documentation: `docs/WHATSAPP_CONTACT_MANAGER_GUIDE.md`, `docs/WHATSAPP_BATCH_AUTOMATION_GUIDE.md`, `docs/WHATSAPP_COMMANDS_QUICK_GUIDE.md`.
-   **Phone Link Notification Monitor:** System for monitoring and parsing Windows Action Center notifications from Phone Link.
-   **Contact-Based Calling:** Full contact management system with name-based calling integrated with Phone Link.

## Recent Updates (November 2025)
-   **Enhanced File Creation System with Batch Files (Nov 21):** Complete overhaul of file creation system with batch file integration for maximum Windows reliability. Features: (1) Smart path expansion for shortcuts like "Desktop/file.txt", "Downloads/notes.txt" automatically resolves to full paths, (2) Windows batch file execution for reliable file operations using native `echo` and `type` commands, (3) Automatic fallback to Python methods on non-Windows systems, (4) AI prompt updates to use correct parameter naming (file_path), (5) Three actions: `create_file`, `write_file` (with append mode), `read_file`. Now supports natural language like "make a text file of name vatsal on desktop" or "create file Desktop/vatsal.txt with content Hello World". Path expansion helper in `CommandExecutor._expand_path_shortcuts()` handles Desktop, Downloads, Documents, Pictures, Home, and ~ shortcuts (case-insensitive).
-   **Screenshot Fix (Nov 21):** Fixed screenshot functionality to properly validate filenames and handle empty paths. Auto-adds .png extension when missing. VNC workflow support for cloud screenshot capture.
-   **Windows 11 Settings Batch Automation Suite (NEW):** Complete batch file automation for all Windows 11 settings with 9 specialized modules + master controller. Located in `batch_scripts/windows11_settings/`. Includes Display Settings, Sound Settings, Network Settings, Bluetooth Control, Privacy & Security, Personalization, System Settings, Windows Update, and Accessibility. All modules feature interactive menus, registry modifications, PowerShell integration, and Windows Settings URI access. Full documentation in `batch_scripts/windows11_settings/README.md`
-   **Windows 11 Settings Controller (NEW):** Comprehensive Python control system for ALL Windows 11 settings with 100+ functions. Voice-controlled settings for Display, Sound, Network, Bluetooth, Privacy & Security, Personalization, System, Accessibility, Windows Update, Apps, Time & Language, Gaming, Power, and Advanced System settings. PowerShell and Registry integration for native Windows control. Full documentation in `docs/WINDOWS11_SETTINGS_GUIDE.md`
-   **Fixed Shutdown & Restart:** Enhanced error handling with proper return code checking, error messages, and diagnostic testing scripts
-   **Close All Windows Feature:** New comprehensive window/tab closing with batch file integration, protects system-critical processes and BOI itself
-   **WhatsApp Messaging Fixed:** Integrated WhatsApp automation with command executor, supports sending by contact name or phone number
-   **Spotify Integration Enhanced:** Added Windows batch files for Spotify control, play song functionality with search, full voice command integration

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
-   **wttr.in API:** For weather data.
-   **Google Translate API:** For language translation.
-   **opencv-python:** For screen monitoring, image analysis, and webcam capture.
-   **MediaPipe:** For hand tracking and gesture recognition.
-   **Data Science Libraries:** pandas, numpy, scikit-learn, matplotlib, seaborn, statsmodels, nltk, openpyxl.
-   **Image Processing:** Pillow (PIL), qrcode, pyzbar.
-   **Selenium:** For web automation and intelligent form filling.