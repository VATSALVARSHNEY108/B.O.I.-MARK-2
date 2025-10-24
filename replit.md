# AI Desktop Automation Controller

## Overview
An intelligent desktop automation tool powered by Google's Gemini AI, designed to interpret natural language commands and execute them on desktop computers. The project features a **unified ecosystem** where all 120+ features work together intelligently, including **500+ Web Tools Integration** (via In-One-Box Streamlit app), **Spotify music control**, system control, voice commands, productivity monitoring, smart typing, auto-organization, file management, web automation, fun features, and **7 utility modules** (Weather & News, Translation, Calculator, Password Vault, Quick Notes, and Calendar Manager). The **Ecosystem Manager** connects all modules, enabling cross-feature workflows, smart suggestions, unified dashboards, and context-aware automation. It integrates advanced AI capabilities for code generation, screen analysis, and natural language understanding to create a comprehensive productivity powerhouse.

## Recent Changes (2025-10-24 - WEB TOOLS INTEGRATION)
- ✅ **HYBRID INTEGRATION**: Added 500+ Web Tools via In-One-Box Streamlit app
  - **web_tools_launcher.py**: Launch and manage Streamlit web app from desktop
  - **tools_mapper.py**: Intelligent mapping of natural language to specific web tools
  - **15 Tool Categories**: Text, Image, File, Coding, Color, CSS, Data, Security, Math, SEO, Social Media, Audio/Video, Web Dev, AI, News & Events
  - **AI-Powered Access**: Natural language commands like "generate QR code", "convert image to PNG"
  - **Seamless Integration**: Desktop automation launches and controls web tools
- ✅ **GUI ENHANCEMENT**: Added dedicated Web Tools tab with 30+ quick actions
- ✅ **GEMINI INTEGRATION**: Updated AI controller to recognize 500+ web tool commands
- ✅ **COMMAND EXECUTOR**: Integrated web tools functionality into main automation system

## Recent Changes (2025-10-23 - FINAL)
- ✅ **COMPLETE**: Fixed all Gemini API key initialization issues across all modules
- ✅ **NEW MODULE**: desktop_controller_advanced.py with complete desktop control
  - Window management (minimize, maximize, close, switch)
  - Display control and multi-monitor support
  - Macro recording and playback system
  - Desktop organization automation
  - Window-specific screenshots
- ✅ **DOCUMENTATION**: Created comprehensive deployment guide (RUNNING_LOCALLY.md)
- ✅ **PROJECT SUMMARY**: Complete feature overview and architecture documentation
- ✅ **PRODUCTION READY**: All 120+ features implemented and tested

## Recent Changes (2025-10-23)
- ✅ **Ecosystem Integration**: Added unified Ecosystem Manager connecting all features
- ✅ **Smart Dashboard**: Unified view of calendar, notes, Pomodoro, weather, and suggestions
- ✅ **Morning/Evening Briefings**: Comprehensive daily summaries
- ✅ **Cross-Module Search**: Search across notes, events, and passwords simultaneously
- ✅ **Auto Organization**: Automated data cleanup and maintenance
- ✅ **Custom Workflows**: Multi-step automation combining features
- ✅ **Smart Suggestions**: Context-aware recommendations based on all ecosystem data
- ✅ **Productivity Insights**: Data-driven analysis from combined modules
- ✅ **Security Improvements**: Enhanced calculator validation, password vault warnings, news API configuration

## User Preferences
None specified yet.

## System Architecture
The AI Desktop Automation Controller is built with Python 3.11 and features a modular architecture.

### UI/UX Decisions
- **Enhanced GUI Application (`gui_app.py`):** Features a modern dark theme with a tabbed interface organizing 50+ functions into 9 categories (Code Generation, Desktop Automation, Messaging, System Control, Productivity, Utilities, Ecosystem, Fun Features, and Web Tools). The new Web Tools tab provides access to 500+ web-based tools through natural language commands. Includes quick-access buttons for all major functions, text input field, real-time color-coded output display, status indicators, and comprehensive help documentation. Utilizes `tkinter` with scrollable panels and threading for non-blocking command execution. Fully functional in cloud/headless environments with graceful degradation.
- **CLI Interface (`main.py`):** Provides an alternative interactive command-line interface with user-friendly prompts and special commands.
- **WhatsApp Desktop Integration:** Dual-mode support: desktop automation via PyWhatKit (when available) and web-based fallback using WhatsApp Web URLs with pre-filled messages. Includes input validation and clear error messaging for unsupported operations in cloud environments.

### Technical Implementations & Feature Specifications
- **AI Command Parser (`gemini_controller.py`):** Integrates with the Gemini API (gemini-2.0-flash-exp model) to parse natural language into structured JSON actions, provide AI suggestions, handle single and multi-step workflows, and manage messaging/contact commands.
- **GUI Automation Module (`gui_automation.py`):** Wraps PyAutoGUI for cross-platform desktop control (mouse, keyboard, applications, clipboard), including graceful handling for headless environments with a demo mode.
- **Command Execution Engine (`command_executor.py`):** Maps parsed commands to automation functions, executes actions, provides feedback, and handles errors.
- **Contact Management System (`contact_manager.py`):** Stores and manages contact information in a JSON-based persistent storage (`contacts.json`), supporting add, update, delete, search, and list operations.
- **Messaging Service (`messaging_service.py`):** Handles SMS (via Twilio), email (via Gmail with attachments), and file sending, utilizing contact information and supporting a demo mode.
- **Code Generation Module (`code_generator.py`):** An advanced AI system that auto-detects programming languages (10+ supported), generates clean code, explains, improves, and debugs code, and includes language templates.
- **Code Execution Module (`code_executor.py`):** Safely executes generated Python and JavaScript code with safety validation, timeout protection, and output/error capture.
- **Conversation Memory (`conversation_memory.py`):** Tracks conversation history, remembers commands and results, and stores usage statistics persistently.
- **AI Vision Module (`screenshot_analyzer.py`):** Analyzes screenshots using Gemini Vision for text extraction (OCR), UI element finding, comparison, and image understanding, also providing AI screen analysis for improvement suggestions, error detection, and quick tips.
- **System Monitoring (`system_monitor.py`):** Monitors CPU, RAM, disk usage, network statistics, battery information, and processes, generating system health reports.
- **Advanced File Operations (`advanced_file_operations.py`):** Includes functionalities for searching, finding large/duplicate files, calculating directory sizes, and organizing files.
- **Workflow Management (`workflow_templates.py`):** Allows saving and reusing workflows via a template system with usage tracking and persistent storage.
- **System Control Module (`system_control.py`):** Manages microphone auto-mute/unmute, brightness control, sleep/wake scheduling, temporary file cleanup, recycle bin management, and disk space monitoring.
- **App Automation Module (`app_scheduler.py`):** Schedules app openings, detects idle time to close heavy apps, monitors heavy app usage, and launches multiple websites.
- **Download Organization (`download_organizer.py`):** Automatically organizes downloads by category, using real-time file system watching and providing statistics.
- **Voice Commands (`voice_assistant.py`):** Implements speech recognition for hands-free control, text-to-speech responses, continuous listening, and voice command processing.
- **Smart Typing Assistant (`smart_typing.py`):** Provides text snippet expansion, email template generation, form filling automation, auto-correction, and password generation.
- **Productivity Tracking (`productivity_monitor.py`):** Tracks screen time, blocks distractions, enables focus mode, scores productivity, provides smart reminders, and logs activity.
- **Fun Features (`fun_features.py`):** Includes a random compliments system, task celebration messages, mood themes, a mini chatbot, and playlist suggestions.
- **Spotify Integration (`spotify_automation.py`):** Full Spotify playback control via natural language commands, including play/pause, skip tracks, volume control, search and play songs, playlist browsing, shuffle/repeat modes, and current track information. Uses Replit's Spotify connector for automatic OAuth and token management.
- **YouTube Integration:** Intelligent video search, auto-play (with multiple fallback methods), and direct video opening.
- **Enhanced Email Sending:** Supports simple text, HTML, and templated emails with attachments, multiple recipients, CC/BCC, and integration with Gmail via SMTP.
- **Weather & News Service (`weather_news_service.py`):** Get real-time weather information for any city, 3-day forecasts, and news headlines by category. Weather uses free wttr.in API; news requires NEWS_API_KEY environment variable.
- **Translation Service (`translation_service.py`):** Translate text between 28+ languages, detect language, and view supported languages using Google Translate API.
- **Advanced Calculator (`advanced_calculator.py`):** Perform complex calculations with safety validation, convert between units (length, weight, temperature, volume), and get real-time currency exchange rates.
- **Pomodoro Timer (`pomodoro_timer.py`):** Focus timer with customizable work/break intervals, pause/resume functionality, and productivity statistics tracking.
- **Password Vault (`password_vault.py`):** Encrypted password storage using Fernet encryption, strong password generation, strength checking, and secure retrieval. Note: Basic file-based security with chmod 600 protection.
- **Quick Notes (`quick_notes.py`):** Fast note-taking with categories, tags, search functionality, pinning, and export capabilities.
- **Calendar Manager (`calendar_manager.py`):** Event scheduling with natural date parsing (today/tomorrow), reminders, search, and upcoming events view.
- **Web Tools Launcher (`web_tools_launcher.py`):** Launches and manages the In-One-Box Streamlit web app, providing access to 500+ comprehensive tools. Features port management, app status checking, automatic browser opening, and seamless integration with desktop automation.
- **Tools Mapper (`tools_mapper.py`):** Intelligent natural language processing to map user commands to specific web tools. Supports 15 tool categories with keyword-based routing, auto-suggestions, and tool descriptions. Handles commands like "generate QR code", "convert image", "open color picker" and routes them to appropriate web tools.

### Safety & Error Handling
- PyAutoGUI failsafe for emergency stops.
- Graceful degradation in headless environments and a demo mode for testing.
- Detailed error messages, input validation, and structural validation of AI responses.

## External Dependencies
- **google-genai:** For Gemini AI SDK integration.
- **PyAutoGUI:** For GUI automation.
- **pyperclip:** For clipboard operations.
- **psutil:** For process management and system monitoring.
- **python-dotenv:** For managing environment variables.
- **streamlit:** For running the In-One-Box web tools application (500+ tools).
- **Twilio:** For SMS messaging (requires `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`).
- **Gmail SMTP:** For email sending (requires `GMAIL_USER`, `GMAIL_APP_PASSWORD`).
- **watchdog:** For real-time file system watching (download organizer).
- **speechrecognition:** For voice commands.
- **pyttsx3:** For text-to-speech responses.
- **cryptography:** For encrypted credential storage.
- **requests:** For HTTP API calls (Spotify integration, web tools status).
- **Replit Spotify Connector:** For OAuth and token management with Spotify API.
- **NEWS_API_KEY (optional):** For news headlines feature. Get free key from newsapi.org.

## Web Tools Integration (In-One-Box)
The project integrates with the user's In-One-Box Streamlit repository (https://github.com/VATSALVARSHNEY108/In-One-Box-.git) to provide access to 500+ web-based tools through natural language commands. The hybrid integration allows the desktop automation to launch and control the web app, providing a seamless experience where users can access comprehensive toolsets via AI-powered commands.

### Tool Categories (15):
1. **Text Tools** (50+ tools): QR codes, Base64, hashes, word counter, case converter, lorem ipsum, password generator
2. **Image Tools** (40+ tools): Format conversion, resizing, compression, watermarks, filters, background remover
3. **File Tools** (45+ tools): Compression, encryption, bulk renaming, duplicate finder
4. **Coding Tools** (35+ tools): Code formatter, minifier, JSON validator, regex tester, API tester
5. **Color Tools** (20+ tools): Color picker, palette generator, gradient maker, converter, contrast checker
6. **CSS Tools** (25+ tools): CSS generator, box shadow, border radius, flexbox/grid generators
7. **Data Tools** (30+ tools): CSV converter, JSON editor, XML parser, data validator, SQL formatter
8. **Security/Privacy Tools** (25+ tools): Password generator, hash generator, encryptor, security scanner
9. **Math/Science Tools** (30+ tools): Calculator, unit converter, equation solver, statistics, graph plotter
10. **SEO/Marketing Tools** (35+ tools): Keyword research, meta tags, sitemap creator, backlink checker
11. **Social Media Tools** (30+ tools): Post scheduler, analytics, hashtag generator, caption creator
12. **Audio/Video Tools** (35+ tools): Audio/video converter, trimmer, compressor
13. **Web Developer Tools** (40+ tools): HTML/CSS/JS formatters, performance tester, SEO analyzer
14. **AI Tools** (30+ tools): Text generation, image analysis, content creation, language translation
15. **News & Events Tools** (20+ tools): News aggregator, RSS reader, event calendar, weather forecast

### Usage Examples:
- "Generate QR code" → Opens Text Tools with QR code generator
- "Convert image to PNG" → Opens Image Tools with format converter
- "Open color picker" → Opens Color Tools
- "Launch web tools" → Starts the full Streamlit application
- "List web tools" → Shows all available tool categories