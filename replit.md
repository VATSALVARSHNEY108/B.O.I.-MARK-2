# AI Desktop Automation Controller

## Overview
The AI Desktop Automation Controller is an intelligent desktop automation tool powered by Google's Gemini AI. It interprets natural language commands to execute a wide range of tasks on desktop computers. The project aims to be a comprehensive productivity powerhouse, offering a unified ecosystem with over 310+ features, including smart Desktop RAG, 9 Smart Automation & AI features, Natural Language Workflow Builder, 8 Communication Enhancement features, 7 new essential utility tools (November 2025), and a real-time WebSocket dashboard for live monitoring. It integrates advanced AI for code generation, screen analysis, natural language understanding, professional-grade data analysis, various utility modules, and real-time remote monitoring capabilities, including an Intelligent AI Assistant.

## User Preferences
- **Chat Monitoring:** User prefers visual/screen-based chat monitoring where AI controls the real Gmail/WhatsApp interface on screen, rather than background API calls. This allows them to watch the AI work in real-time.

## System Architecture
The AI Desktop Automation Controller is built with Python 3.11 and utilizes a modular architecture, enabling a wide range of desktop automation and AI-powered functionalities.

### UI/UX Decisions
The system offers two GUI options:
1.  **Original GUI** (`gui_app.py`): A comprehensive, feature-rich interface with a tabbed design, live clock, quick-access buttons, and real-time console output.
2.  **Enhanced Modern GUI** (`enhanced_gui.py`): A redesigned interface featuring a dark theme, a dashboard with live statistics, sidebar navigation, 6 major views, a stunning color palette (navy blue backgrounds, purple-blue accents), hover effects, and a professional high-contrast appearance with a terminal-style command prompt bar.

Both GUIs are built with `tkinter` and support VATSAL Mode and Self-Operating Mode. A CLI interface (`main.py`) is also available.

### Technical Implementations
-   **AI Command Processing:** Gemini AI is integrated for natural language processing and converting commands into actions.
-   **AI Code & Letter Generation:** Gemini AI-powered generator creates clean, well-commented code in multiple languages and professional letters using 13 templates, writing directly to Notepad.
-   **Full Screen Notepad Writer:** Enhanced Notepad integration automatically opens Notepad in full screen mode for generated content.
-   **GUI Automation:** Uses `PyAutoGUI` for cross-platform desktop control.
-   **AI Vision Module:** Leverages Gemini Vision for OCR, UI element identification, and screen analysis.
-   **Desktop RAG System:** Indexes desktop files for semantic search and Q&A.
-   **Smart Automation & AI:** Provides 9 AI-powered features for various tasks.
-   **Visual Chat Monitor:** AI-powered visual email/WhatsApp monitoring via real browser interface control.
-   **System Control:** Manages system-level automation (lock screen, shutdown, restart, brightness, volume, disk cleanup) with cross-platform support and Windows batch file integration. Includes new features for system information, clipboard, power management, window management, process management, quick app launchers, and timers/alarms.
-   **Voice Assistant:** An ultra-intelligent, interactive voice commanding system with advanced AI capabilities, supporting multiple wake words ("Vatsal", "Hey Vatsal", etc.), NLU, context awareness, and entity extraction.
-   **Face & Gesture Assistant:** Computer vision-powered face detection and hand gesture recognition using OpenCV and MediaPipe. Detects user's face to greet them by name ("Vatsal" or "Yes sir"), and recognizes hand gestures (open palm) to activate voice listening mode. Provides hands-free, natural interaction with full GUI integration.
-   **Self-Operating Computer:** Autonomous AI desktop control using Gemini Vision (Gemini 2.0 Flash Exp) for screen analysis and autonomous actions.
-   **Real-Time WebSocket System:** A Flask-SocketIO based server provides a live dashboard for real-time monitoring of system stats and command execution.
-   **Mobile Companion System:** Offers complete mobile control via a REST API and a touch-optimized web interface, including PIN-based authentication and push notifications.
-   **Automation Recording & Macro System:** Professional macro recording and playback for mouse and keyboard events.
-   **Natural Language Workflow Builder:** AI-powered workflow creation from plain English descriptions using Gemini 2.0 Flash.
-   **Advanced AI Enhancements:** Integrates Multi-Modal AI, Enhanced Contextual Memory, a Correction Learning System, and a Predictive Actions Engine.
-   **AI-Powered Security Dashboard:** Comprehensive security management powered by Gemini AI, integrating biometric authentication, 2FA, encrypted storage, and AI-driven threat analysis.
-   **Batch Form Filler System:** Comprehensive form automation system with 15+ pre-built templates supporting web forms (Selenium), desktop forms (PyAutoGUI), clipboard mode, and batch processing from CSV/Excel files. Features intelligent field detection, smart field matching, and supports job applications, registrations, surveys, medical forms, banking, e-commerce, and more.
-   **Hand Gesture Mouse Controller:** Touchless computer control using webcam and MediaPipe hand tracking. Control mouse cursor, click, scroll, drag, and adjust volume using natural hand gestures. Features real-time tracking at 30-60 FPS, 7 gesture types (cursor move, left/right click, scroll, drag, volume control), smooth cursor tracking with jitter reduction, and gesture statistics tracking.
-   **Utility Modules:** Includes integrations for Spotify, YouTube, Weather & News, Translation, Calculator, Password Vault, Quick Notes, Calendar Manager, Timer & Stopwatch, Quick Reminders, Habit Tracker, Color Tools, QR Code Tools, Screenshot Annotator, Image Resizer, Batch Form Filler, and Hand Gesture Controller.
    -   **Timer & Stopwatch:** Countdown timers with cancellation, stopwatch with lap times, and Pomodoro mode.
    -   **Quick Reminders:** Scheduled reminders with cross-platform pop-up notifications, sound alerts, and snooze functionality.
    -   **Habit Tracker:** Daily habit checklist with streak tracking, statistics, and completion history.
    -   **Color Picker & Converter:** Screen color picker, format conversion (HEX/RGB/HSL/HSV), palette generation, and color manipulation.
    -   **QR Code Tools:** Generate QR codes for URLs, text, contacts, WiFi credentials; read QR codes from files and screen.
    -   **Screenshot Annotator:** Add text, arrows, rectangles, circles, highlights, and blur areas to screenshots.
    -   **Image Resizer:** Batch image resizing, compression, format conversion, thumbnail creation, rotation, and cropping.
    -   **Batch Form Filler:** Intelligent form automation with 15+ templates (job applications, contact forms, surveys, medical, banking, etc.), web form automation (Selenium), desktop form filling (PyAutoGUI), clipboard mode, and batch processing from CSV/Excel with smart field matching.
    -   **Hand Gesture Controller:** Touchless mouse control via webcam using MediaPipe hand tracking. Features 7 gesture types: cursor movement, left/right click, scroll, drag & drop, and volume control. Real-time hand detection at 30-60 FPS with smooth cursor tracking.

## External Dependencies
-   **google-genai:** For Gemini AI integration.
-   **PyAutoGUI:** For GUI automation.
-   **pyperclip:** For clipboard operations.
-   **psutil:** For system monitoring.
-   **python-dotenv:** For environment variable management.
-   **streamlit:** For web tools application.
-   **Twilio:** For SMS messaging.
-   **Gmail SMTP:** For email sending.
-   **watchdog:** For real-time file system monitoring.
-   **speechrecognition & pyttsx3:** For voice commands and text-to-speech.
-   **cryptography:** For encryption.
-   **requests:** For HTTP API calls.
-   **Replit Spotify Connector:** For Spotify API integration.
-   **wttr.in API:** For weather data.
-   **Google Translate API:** For language translation.
-   **opencv-python:** For screen monitoring, image analysis, and webcam capture for hand gesture control.
-   **MediaPipe:** For real-time hand tracking and gesture recognition.
-   **Data Science Libraries:** pandas, numpy, scikit-learn, matplotlib, seaborn, statsmodels, nltk, openpyxl.
-   **Image Processing:** Pillow (PIL), qrcode, pyzbar for QR code operations.
-   **Selenium:** For web automation and intelligent form filling.

## Recent Changes
-   **November 2025 (Latest Update):** Added **Custom Gesture Training System** - Train unlimited custom hand gestures using machine learning!
    - **GestureTrainer module** (`modules/automation/gesture_trainer.py`): Captures samples from camera, extracts HOG + Hu moment features, trains SVM classifier
    - **Hybrid Detection** in `opencv_hand_gesture_detector.py`: Tries ML model first (custom gestures), falls back to hardcoded finger-counting
    - **Training Utility** (`train_hand_gestures.py`): User-friendly CLI for capturing samples and training models
    - **Smart Recognition**: Detects custom gestures with confidence scoring (60% threshold)
    - **Backward Compatible**: All old hardcoded gestures (OPEN_PALM, FIST, etc.) still work!
    - **Documentation**: Complete guides in GESTURE_TRAINING_GUIDE.md and FIX_ENVIRONMENT.md
    - **Storage**: Models saved to biometric_data/hands/ directory
-   **November 2025:** Added **Enhanced Hand Gesture & Face Detection** with dual implementation:
    - **OpenCV-only detector** (works everywhere, including Python 3.13 on Windows and Replit)
    - **MediaPipe detector** (when available, for advanced tracking)
    - Features: Real-time face detection, hand gesture recognition (open palm 👋, fist ✊), automatic voice activation, greeting system
    - Gestures: Open palm activates listening, fist stops, with visual feedback
    - Full GUI integration, standalone demo (`demo_opencv_hand_gesture.py`), comprehensive documentation
    - Works without MediaPipe dependency using skin color detection and contour analysis
-   **November 2025:** Added Face & Gesture Assistant feature using OpenCV and MediaPipe. System now detects user's face via webcam, greets them by name ("Vatsal" or "Yes sir"), and recognizes hand gestures (open palm) to activate voice listening mode. Includes full GUI integration with toggle button (👤), thread-safe callbacks, real-time camera feed display, session statistics, and comprehensive documentation (docs/FACE_GESTURE_FEATURE.md).
-   **November 2025:** Added Hand Gesture Mouse Controller with MediaPipe integration for touchless computer control. Features 7 gesture types (cursor, clicks, scroll, drag, volume), real-time hand tracking at 30-60 FPS, smooth cursor movement, and gesture statistics. **Now fully integrated into both GUI applications** with easy-to-use launch buttons in the Automation section. Includes comprehensive demo, documentation, and standalone launcher.
-   **November 2025:** Added comprehensive Batch Form Filler system with 15+ pre-built templates supporting web forms, desktop applications, clipboard mode, and batch processing from CSV/Excel files. Includes smart field detection and intelligent field name matching for automated form filling across multiple platforms.