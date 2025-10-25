# AI Desktop Automation Controller

## Overview
The AI Desktop Automation Controller is an intelligent desktop automation tool powered by Google's Gemini AI. Its core purpose is to interpret natural language commands to execute a wide range of tasks on desktop computers, offering a unified ecosystem with over 280+ features including smart Desktop RAG for file intelligence. This includes advanced behavioral learning, workspace management, multimodal control, AI automation, data intelligence, collaboration tools, creative utilities, security enhancements, human-like interaction, cloud ecosystem integration, system control, voice commands, productivity monitoring, smart typing, auto-organization, file management, web automation, and comprehensive AI-powered features across 17 categories (Chatbots, Text Generation, Image Generation, Data Analysis, Computer Vision, Voice & Audio, Audio/Video Conversion, Editing, Compression, Analysis, Streaming, Subtitle Tools, Metadata Editors, Audio/Video Enhancement, Media Utilities). The project aims to be a comprehensive productivity powerhouse, integrating advanced AI for code generation, screen analysis, natural language understanding, professional-grade data analysis (with ML, statistical testing, and visualization), and utility modules like Spotify control, Weather & News, Translation, Calculator, Password Vault, Quick Notes, and Calendar Manager.

## User Preferences
- **Chat Monitoring:** User prefers visual/screen-based chat monitoring where AI controls the real Gmail/WhatsApp interface on screen, rather than background API calls. This allows them to watch the AI work in real-time.

## System Architecture
The AI Desktop Automation Controller is built with Python 3.11 and utilizes a modular architecture for scalability and maintainability.

### UI/UX Decisions
The primary interface is a GUI application (`gui_app.py`) featuring a modern, dark-themed, tabbed design (Version 2.0.0 - VATSAL Edition) with over 50 functions organized across 10 categories. Key UI elements include: a 1400x900 window with improved spacing, Segoe UI fonts, a live clock, card-based design with gradient effects and hover animations, quick-access buttons, a real-time color-coded output console, and a VATSAL Mode toggle. It's built with `tkinter` and uses threading for non-blocking execution. A CLI interface (`main.py`) offers an interactive command-line alternative.

**Recent Update:** The Advanced Smart Screen Monitor has been fully integrated into the GUI's AI Features tab, providing one-click access to 8 specialized AI analysis modes (Comprehensive Analysis, Security Scan, Performance Audit, UX Review, Accessibility Audit, Code Review, Design Critique, Automation Discovery), analytics reporting, and continuous monitoring with configurable triggers.

The VATSAL AI Assistant (`vatsal_assistant.py`) is an intelligent AI companion (Virtual Assistant To Serve And Learn) with a sophisticated, British-inspired personality, contextual awareness, conversation memory (last 10 exchanges), time-aware greetings, proactive suggestions, and professional acknowledgments. It addresses the user politely and offers toggle-able personality and memory persistence.

**NEW:** The JARVIS AI System (`jarvis_ai.py`) is an advanced conversational assistant inspired by JARVIS and FRIDAY from Marvel. Unlike standard command executors, JARVIS initiates conversations, asks clarifying questions before executing tasks, maintains sophisticated multi-turn dialogue with full context awareness, learns user preferences and habits, provides proactive time-based suggestions, and features a dedicated GUI chat interface. It has a polite, formal British butler-like personality, remembers the last 20 conversation exchanges, confirms important actions before execution, and continuously learns from interactions to improve service.

### Technical Implementations
- **AI Command Parser (`gemini_controller.py`):** Integrates with Gemini API (gemini-2.0-flash-exp) for natural language processing, converting commands into structured JSON actions, and managing multi-step workflows.
- **GUI Automation Module (`gui_automation.py`):** Wraps PyAutoGUI for cross-platform desktop control (mouse, keyboard, applications, clipboard).
- **Command Execution Engine (`command_executor.py`):** Maps and executes parsed commands.
- **Contact Management System (`contact_manager.py`):** Manages contact information in `contacts.json`.
- **Messaging Service (`messaging_service.py`):** Handles SMS (Twilio), email (Gmail), and file sending, including WhatsApp Desktop integration.
- **Code Generation & Execution Modules (`code_generator.py`, `code_executor.py`):** AI-powered code generation/explanation/debugging and safe execution for Python/JavaScript.
- **Conversation Memory (`conversation_memory.py`):** Stores history, commands, results, and usage statistics.
- **AI Vision Module (`screenshot_analyzer.py`):** Uses Gemini Vision for OCR, UI element identification, and screen analysis.
- **System Monitoring (`system_monitor.py`):** Monitors CPU, RAM, disk, network, battery and generates reports.
- **Advanced File Operations (`advanced_file_operations.py`):** Includes searching, duplicate finding, directory sizing, and organization.
- **Workflow Management (`workflow_templates.py`):** For saving, reusing, and tracking custom automation workflows.
- **System Control Module (`system_control.py`):** Manages microphone, display, sleep, temporary files, and recycle bin.
- **App Automation Module (`app_scheduler.py`):** Schedules app openings, manages heavy app usage, and launches websites.
- **Download Organization (`download_organizer.py`):** Automatically organizes downloads by category.
- **Voice Commands (`voice_assistant.py`):** Provides speech recognition, text-to-speech, and continuous listening.
- **Smart Typing Assistant (`smart_typing.py`):** Offers text snippet expansion, email templates, form filling, auto-correction, and password generation.
- **Productivity Tracking (`productivity_monitor.py`):** Monitors screen time, blocks distractions, and provides insights.
- **Fun Features (`fun_features.py`):** Includes compliments, task celebrations, mood themes, and a mini chatbot.
- **Spotify Integration (`spotify_automation.py`):** Full Spotify playback control.
- **YouTube Integration:** Intelligent video search and auto-play.
- **Utility Modules:** Weather & News (`weather_news_service.py`), Translation (`translation_service.py`), Advanced Calculator (`advanced_calculator.py`), Pomodoro Timer (`pomodoro_timer.py`), Password Vault (`password_vault.py`), Quick Notes (`quick_notes.py`), and Calendar Manager (`calendar_manager.py`).
- **Web Tools Launcher & Mapper (`web_tools_launcher.py`, `tools_mapper.py`):** Manages and launches an In-One-Box Streamlit app for 500+ web tools, intelligently mapping natural language commands.
- **AI Features Module (`ai_features.py`):** Provides 80+ AI capabilities across 17 categories, including Chatbots, Text Generation, Language Processing, Image Generation, Data Analysis, Computer Vision, Voice & Audio, Audio/Video Conversion/Editing/Compression/Analysis, Streaming, Subtitle Tools, Metadata Editors, Audio/Video Enhancement, and Media Utilities.
- **Data Analysis Suite (`data_analysis.py`):** Professional-grade toolkit with 100+ features covering Data Import/Export, Cleaning, Analysis, Visualization, Transformation, Machine Learning (regression, classification, clustering), Text Analytics, Time Series, Statistical Tests, and Data Quality.
- **Behavioral Learning Engine (`behavioral_learning.py`):** AI-powered habit tracking and pattern prediction with action recording, habit summaries, and intelligent suggestions.
- **AI Workspace Management (`workspace_manager.py`):** Offers virtual work environments, smart clipboard history, intelligent notifications, window grouping, and focus triggers.
- **Voice & Multimodal Control (`multimodal_control.py`):** Enhanced voice interaction with custom phrase training, slang dictionary, whisper mode, gesture mapping, and adaptive reply modes.
- **Advanced AI Automation (`advanced_ai_automation.py`):** Features email content summarization, AI document generation, code review assistance, visual workflow builder, and macro suggestion engine.
- **Data Intelligence Extensions (`data_intelligence.py`):** Includes anomaly detection, interactive dashboard creation, AI-powered query builder, ML pipeline setup, and dataset encryption.
- **Communication & Collaboration (`collaboration_tools.py`):** Provides meeting transcript recording, optimal email scheduling, cross-app messaging, voice memo conversion, and AI presentation generation.
- **Creative Utilities (`creative_utilities.py`):** Offers text-to-image generation, voice model creation, AI scriptwriting, and audio file summarization.
- **Security Enhancements (`security_enhancements.py`):** Features smart access control, auto VPN activation, real-time threat detection, scheduled data wiping, and trusted device management.
- **Human-like Interaction (`human_interaction.py`):** Incorporates conversation context recall, adaptive AI tone, user stress detection, goal tracking, and a gamified productivity system.
- **Cloud & Extension Ecosystem (`cloud_ecosystem.py`):** Supports multi-item cloud sync, a custom plugin framework, a workflow marketplace, mobile device connectivity, and cloud backup/restore.
- **Ecosystem Manager:** Connects all modules for cross-feature workflows, smart suggestions, unified dashboards, and context-aware automation.
- **Visual Chat Monitor (`visual_chat_monitor.py`):** AI-powered visual email/WhatsApp monitoring that controls the real browser interface. Opens Gmail/WhatsApp Web, uses AI Vision to read messages from screenshots, generates intelligent replies, and types them with user approval. Everything happens visually on screen.
- **Chat Monitor API (`chat_monitor.py`):** Background chat monitoring using Gmail IMAP and Twilio SMS APIs. Reads unread emails and SMS messages, generates AI-powered replies, manages approval workflow. Requires Gmail App Password and Twilio credentials (optional - user declined Replit integrations, prefers environment variables).
- **Smart Screen Monitor (`smart_screen_monitor.py`):** AI-powered screen monitoring that continuously watches and analyzes the screen. Provides productivity insights, error detection, code analysis, design feedback, change detection over time, and can answer specific questions about what's visible on screen.
- **AI Screen Monitoring System (`ai_screen_monitoring_system.py`):** Next-generation screen intelligence system with real-time continuous monitoring, 8 AI analysis modes (Productivity, Security, Performance, Errors, UX, Accessibility, Code, Automation), intelligent triggers, automated actions, advanced analytics with trend analysis, pattern learning, change detection optimization, privacy controls, and comprehensive GUI integration.
- **Desktop RAG System (`desktop_rag.py`):** Retrieval Augmented Generation system for intelligent file interaction. Indexes all desktop files (40+ file types), provides semantic search, AI-powered Q&A about file contents, folder summarization, smart duplicate detection, and comprehensive analytics. Integrates with Gemini AI for natural language queries about desktop data.

## External Dependencies
- **google-genai:** For Gemini AI integration.
- **PyAutoGUI:** For GUI automation.
- **pyperclip:** For clipboard operations.
- **psutil:** For system monitoring.
- **python-dotenv:** For environment variable management.
- **streamlit:** For the In-One-Box web tools application.
- **Twilio:** For SMS messaging.
- **Gmail SMTP:** For email sending.
- **watchdog:** For real-time file system monitoring.
- **speechrecognition & pyttsx3:** For voice commands and text-to-speech.
- **cryptography:** For encryption (e.g., Password Vault).
- **requests:** For HTTP API calls.
- **Replit Spotify Connector:** For Spotify API integration.
- **wttr.in API:** For weather data.
- **Google Translate API:** For language translation.
- **Data Science Libraries:** pandas, numpy, scikit-learn, matplotlib, seaborn, statsmodels, nltk, openpyxl.