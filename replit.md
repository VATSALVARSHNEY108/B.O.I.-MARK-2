# AI Desktop Automation Controller

## Overview
The AI Desktop Automation Controller is an intelligent desktop automation tool powered by Google's Gemini AI. It interprets natural language commands to execute a wide range of tasks on desktop computers. Its core purpose is to provide a unified ecosystem with over 150 features, including system control, voice commands, productivity monitoring, smart typing, auto-organization, file management, web automation, advanced AI capabilities, and integrations with over 500 web tools via an In-One-Box Streamlit application. The project aims to be a comprehensive productivity powerhouse by integrating advanced AI for code generation, screen analysis, natural language understanding, and comprehensive AI-powered features across 7 categories: Chatbots, Text Generation, Language Processing, Image Generation, Data Analysis, Computer Vision, and Voice & Audio. Key capabilities include Spotify music control and utility modules: Weather & News, Translation, Calculator, Password Vault, Quick Notes, and Calendar Manager.

## User Preferences
None specified yet.

## System Architecture
The AI Desktop Automation Controller is built with Python 3.11 and utilizes a modular architecture to ensure scalability and maintainability.

### UI/UX Decisions
- **GUI Application (`gui_app.py`):** Features a modern dark-themed, tabbed interface, organizing over 50 functions across 10 categories including a dedicated AI Features tab. It includes quick-access buttons, a text input field, real-time color-coded output, status indicators, and comprehensive help documentation. Built with `tkinter`, it uses threading for non-blocking execution and is designed for graceful degradation in headless environments.
- **CLI Interface (`main.py`):** Provides an interactive command-line alternative with user-friendly prompts.
- **WhatsApp Desktop Integration:** Supports dual-mode operation for messaging via PyWhatKit or web-based fallback using WhatsApp Web URLs.

### Technical Implementations & Feature Specifications
- **AI Command Parser (`gemini_controller.py`):** Integrates with the Gemini API (gemini-2.0-flash-exp) for natural language processing, converting commands into structured JSON actions, providing AI suggestions, and managing multi-step workflows.
- **GUI Automation Module (`gui_automation.py`):** Wraps PyAutoGUI for cross-platform desktop control (mouse, keyboard, applications, clipboard), including headless environment handling.
- **Command Execution Engine (`command_executor.py`):** Maps and executes parsed commands, handles feedback, and manages errors.
- **Contact Management System (`contact_manager.py`):** Manages contact information in a JSON-based persistent storage (`contacts.json`).
- **Messaging Service (`messaging_service.py`):** Handles SMS (Twilio), email (Gmail), and file sending, with demo mode support.
- **Code Generation Module (`code_generator.py`):** AI-powered system for generating, explaining, improving, and debugging code across 10+ programming languages.
- **Code Execution Module (`code_executor.py`):** Safely executes Python and JavaScript code with validation, timeouts, and output capture.
- **Conversation Memory (`conversation_memory.py`):** Stores conversation history, commands, results, and usage statistics.
- **AI Vision Module (`screenshot_analyzer.py`):** Uses Gemini Vision for OCR, UI element identification, image comparison, and AI-driven screen analysis.
- **System Monitoring (`system_monitor.py`):** Monitors CPU, RAM, disk, network, and battery, generating system health reports.
- **Advanced File Operations (`advanced_file_operations.py`):** Features for searching, finding duplicates, calculating directory sizes, and file organization.
- **Workflow Management (`workflow_templates.py`):** Enables saving, reusing, and tracking custom automation workflows.
- **System Control Module (`system_control.py`):** Manages microphone, display brightness, sleep schedules, temporary file cleanup, and recycle bin.
- **App Automation Module (`app_scheduler.py`):** Schedules app openings, manages heavy app usage, and launches multiple websites.
- **Download Organization (`download_organizer.py`):** Automatically organizes downloads by category using real-time file system watching.
- **Voice Commands (`voice_assistant.py`):** Provides speech recognition, text-to-speech responses, and continuous listening for hands-free control.
- **Smart Typing Assistant (`smart_typing.py`):** Offers text snippet expansion, email template generation, form filling, auto-correction, and password generation.
- **Productivity Tracking (`productivity_monitor.py`):** Monitors screen time, blocks distractions, implements focus modes, and provides productivity insights.
- **Fun Features (`fun_features.py`):** Includes random compliments, task celebrations, mood themes, a mini chatbot, and playlist suggestions.
- **Spotify Integration (`spotify_automation.py`):** Full Spotify playback control via natural language commands, utilizing Replit's Spotify connector.
- **YouTube Integration:** Intelligent video search, auto-play, and direct video opening.
- **Weather & News Service (`weather_news_service.py`):** Provides real-time weather and news headlines.
- **Translation Service (`translation_service.py`):** Translates text between 28+ languages using Google Translate API.
- **Advanced Calculator (`advanced_calculator.py`):** Performs complex calculations, unit conversions, and currency exchange.
- **Pomodoro Timer (`pomodoro_timer.py`):** Customizable focus timer with work/break intervals and productivity statistics.
- **Password Vault (`password_vault.py`):** Encrypted password storage, generation, and strength checking using Fernet encryption.
- **Quick Notes (`quick_notes.py`):** Fast note-taking with categories, tags, search, pinning, and export.
- **Calendar Manager (`calendar_manager.py`):** Event scheduling with natural date parsing, reminders, and event viewing.
- **Web Tools Launcher (`web_tools_launcher.py`):** Manages and launches the In-One-Box Streamlit web app, providing access to 500+ tools.
- **Tools Mapper (`tools_mapper.py`):** Intelligently maps natural language commands to specific web tools across 15 categories, supporting commands like "generate QR code" or "convert image."
- **AI Features Module (`ai_features.py`):** Comprehensive AI capabilities organized into 7 categories with 30+ features:
  - **Chatbots:** Conversational AI, customer service bot, educational assistant, domain expert
  - **Text Generation:** Story writer, content creator, article generator, copywriting assistant, technical writer
  - **Language Processing:** Text translator, sentiment analysis, text summarizer, language detector, content moderator
  - **Image Generation:** AI art prompt generator, style transfer descriptions
  - **Data Analysis:** Pattern recognition, trend analysis, predictive modeling, data insights, statistical analysis
  - **Computer Vision:** Image recognition guide, object detection guide, scene analysis guide
  - **Voice & Audio:** Speech text generator, audio analysis guide
- **Ecosystem Manager:** Connects all modules, enabling cross-feature workflows, smart suggestions, unified dashboards, and context-aware automation. Features include smart dashboards, morning/evening briefings, cross-module search, auto-organization, custom workflows, smart suggestions, and productivity insights.

## External Dependencies
- **google-genai:** Gemini AI SDK.
- **PyAutoGUI:** GUI automation.
- **pyperclip:** Clipboard operations.
- **psutil:** System monitoring.
- **python-dotenv:** Environment variable management.
- **streamlit:** For the In-One-Box web tools application.
- **Twilio:** SMS messaging.
- **Gmail SMTP:** Email sending.
- **watchdog:** Real-time file system monitoring.
- **speechrecognition:** Voice commands.
- **pyttsx3:** Text-to-speech.
- **cryptography:** Encryption.
- **requests:** HTTP API calls.
- **Replit Spotify Connector:** Spotify API OAuth and token management.
- **wttr.in API:** Weather data.
- **Google Translate API:** Language translation.
- **NEWS_API_KEY (optional):** For news headlines (from newsapi.org).