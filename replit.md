# AI Desktop Automation Controller

## Overview
The AI Desktop Automation Controller is an intelligent desktop automation tool powered by Google's Gemini AI. It interprets natural language commands to execute a wide range of tasks on desktop computers. The project aims to be a comprehensive productivity powerhouse, offering a unified ecosystem with over 310+ features, including smart Desktop RAG, 9 Smart Automation & AI features, Natural Language Workflow Builder, 8 Communication Enhancement features, 7 new essential utility tools, and a real-time WebSocket dashboard for live monitoring. It integrates advanced AI for code generation, screen analysis, natural language understanding, professional-grade data analysis, various utility modules, and real-time remote monitoring capabilities, including an Intelligent AI Assistant.

## User Preferences
-   **Interface:** User prefers desktop GUI interfaces only - NO web-based interfaces. Project uses tkinter-based GUIs (gui_app.py, enhanced_gui.py) for local desktop use.
-   **Chat Monitoring:** User prefers visual/screen-based chat monitoring where AI controls the real Gmail/WhatsApp interface on screen, rather than background API calls. This allows them to watch the AI work in real-time.
-   **File Structure:** Well-organized modular architecture with modules/ directory containing core, voice, automation, ai_features, utilities, etc.

## Recent Changes (November 16, 2025)
-   **Dark Theme UI Upgrade:** Updated GUI theme in `gui_app.py` to match the dark navy/cyan aesthetic from VATSAL Chat and VATSAL Auto pages. Changed from light beige to dark navy backgrounds (#1e2433), cyan accent colors (#1dd3b0), and updated all shadows to complement the dark theme.
-   **Cloud Environment Compatibility:** Fixed CLI workflow to run successfully in cloud/headless environments (Replit) without X11 display. Added graceful fallback handling for PyAutoGUI-dependent features with clear user feedback.
-   **System Dependencies:** Installed gcc-unwrapped to resolve libstdc++.so.6 missing library error for numpy and pandas compatibility.
-   **Import Fixes:** Corrected import paths in smart_screen_monitor.py for analyze_screenshot function.
-   **Spotify Integration:** Successfully configured Replit Spotify connector integration with OAuth authentication.
-   **GUI Aesthetic Upgrade:** Added beautiful multi-layer shadow effects to all buttons and boxes in `gui_app.py` for a modern, elevated 3D appearance.
-   **Command Executor Comprehensive Upgrade:** Added 40+ missing system control actions including lock_screen, shutdown, restart, sleep, hibernate, system monitoring, window management, clipboard operations, and more. The executor now has complete coverage of all system_control.py functions.

## System Architecture
The AI Desktop Automation Controller is built with Python 3.11 and utilizes a modular architecture, enabling a wide range of desktop automation and AI-powered functionalities.

### UI/UX Decisions
The system offers desktop GUIs built with `tkinter` featuring a **modern dark navy/cyan theme** with beautiful multi-layer shadow effects on all buttons and boxes for depth and aesthetic appeal. The dark theme uses navy backgrounds (#1e2433), cyan accents (#1dd3b0), and subtle dark shadows for a professional, cohesive look matching the VATSAL Chat and VATSAL Auto pages. A "Modern Web GUI" is built with Flask and Flask-SocketIO. A CLI interface is available for headless environments.

### Technical Implementations
-   **AI Command Processing:** Gemini AI for natural language understanding and action conversion.
-   **AI Code & Letter Generation:** Gemini AI-powered code and professional letter generation.
-   **GUI Automation:** Uses `PyAutoGUI` for cross-platform desktop control.
-   **AI Vision Module:** Leverages Gemini Vision for OCR, UI element identification, and screen analysis.
-   **Desktop RAG System:** Indexes desktop files for semantic search and Q&A.
-   **Smart Automation & AI:** 9 AI-powered features for various tasks.
-   **Visual Chat Monitor:** AI-powered visual email/WhatsApp monitoring via real browser interface control.
-   **System Control:** Manages system-level automation (lock, shutdown, restart, brightness, volume, disk cleanup), including new features for system information, clipboard, power, window, and process management.
-   **Voice Assistant with Personality:** An ultra-intelligent, interactive voice commanding system with empathetic responses, wake word detection, context awareness, and adaptive feedback.
-   **PersonaResponseService:** A comprehensive personality layer for warm, empathetic, and conversational AI interactions, adapting to user mood, offering proactive suggestions, and providing empathetic error handling.
-   **Face & Gesture Assistant:** Computer vision (OpenCV, MediaPipe) for face detection and hand gesture recognition to activate voice listening.
-   **Self-Operating Computer:** Autonomous AI desktop control using Gemini Vision for screen analysis and actions.
-   **Real-Time WebSocket System:** Flask-SocketIO server for live monitoring dashboard.
-   **Mobile Companion System:** Complete mobile control via REST API and touch-optimized web interface.
-   **Automation Recording & Macro System:** Professional macro recording and playback.
-   **Natural Language Workflow Builder:** AI-powered workflow creation from natural language descriptions using Gemini 2.0 Flash.
-   **Advanced AI Enhancements:** Multi-Modal AI, Enhanced Contextual Memory, Correction Learning System, and Predictive Actions Engine.
-   **AI-Powered Security Dashboard:** Gemini AI-powered security management with biometric auth, 2FA, encrypted storage, and threat analysis.
-   **Batch Form Filler System:** Comprehensive form automation for web (Selenium) and desktop (PyAutoGUI) with intelligent field detection.
-   **Hand Gesture Mouse Controller:** Touchless computer control using webcam and MediaPipe hand tracking for mouse functions.
-   **Utility Modules:** Integrations for Spotify, YouTube, Weather & News, Translation, Calculator, Password Vault, Quick Notes, Calendar Manager, Timer & Stopwatch, Quick Reminders, Habit Tracker, Color Tools, QR Code Tools, Screenshot Annotator, Image Resizer, Batch Form Filler, and Hand Gesture Controller.
-   **AI Performance Optimizations:** Implemented response caching, model fallback, retry optimization, token limit tuning, and generation config adjustments for faster AI responses.

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
-   **opencv-python:** For screen monitoring, image analysis, and webcam capture for hand gesture control.
-   **MediaPipe:** For hand tracking and gesture recognition.
-   **Data Science Libraries:** pandas, numpy, scikit-learn, matplotlib, seaborn, statsmodels, nltk, openpyxl.
-   **Image Processing:** Pillow (PIL), qrcode, pyzbar.
-   **Selenium:** For web automation and intelligent form filling.