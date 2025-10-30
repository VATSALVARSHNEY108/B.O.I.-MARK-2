# AI Desktop Automation Controller

## Overview
The AI Desktop Automation Controller is an intelligent desktop automation tool powered by Google's Gemini AI. It interprets natural language commands to execute a wide range of tasks on desktop computers. The project offers a unified ecosystem with over 300+ features, including smart Desktop RAG for file intelligence, 9 Smart Automation & AI features, 8 Communication Enhancement features, and **real-time WebSocket dashboard** for live monitoring. Its core purpose is to be a comprehensive productivity powerhouse, integrating advanced AI for code generation, screen analysis, natural language understanding, professional-grade data analysis, various utility modules, and real-time remote monitoring capabilities.

## User Preferences
- **Chat Monitoring:** User prefers visual/screen-based chat monitoring where AI controls the real Gmail/WhatsApp interface on screen, rather than background API calls. This allows them to watch the AI work in real-time.

## System Architecture
The AI Desktop Automation Controller is built with Python 3.11 and utilizes a modular architecture.

### UI/UX Decisions
The primary interface is a GUI application (`gui_app.py`) featuring a modern, dark-themed, tabbed design (Version 2.0.0 - VATSAL Edition) with over 50 functions organized across 10 categories. Key UI elements include a 1400x900 window, Segoe UI fonts, a live clock, card-based design with gradient effects, quick-access buttons, and a real-time color-coded output console. It's built with `tkinter` and uses threading for non-blocking execution. A CLI interface (`main.py`) offers an interactive command-line alternative.

The GUI includes toggle buttons for "VATSAL Mode" (personality mode vs. direct responses) and "Self-Operating Mode" (enables/disables autonomous desktop control). The Advanced Smart Screen Monitor is integrated into the GUI's AI Features tab.

The system includes a sophisticated AI assistant (`vatsal_assistant.py`) with contextual awareness and conversation memory, alongside simpler chatbot options, all unified under the "💬 VATSAL Chat" tab in the GUI.

### Technical Implementations
- **AI Command Parser (`gemini_controller.py`):** Integrates Gemini AI for natural language processing and action conversion.
- **GUI Automation Module (`gui_automation.py`):** Uses PyAutoGUI for cross-platform desktop control.
- **Messaging Service (`messaging_service.py`):** Handles SMS, email, and WhatsApp Desktop integration.
- **Code Generation & Execution:** AI-powered code generation, explanation, debugging, and safe execution.
- **AI Vision Module (`screenshot_analyzer.py`):** Uses Gemini Vision for OCR, UI element identification, and screen analysis.
- **Desktop RAG System (`desktop_rag.py`):** Indexes desktop files for semantic search and Q&A.
- **Smart Automation & AI Module (`smart_automation.py`):** Provides 9 AI-powered features like Auto-Bug Fixer and Meeting Scheduler AI.
- **Visual Chat Monitor (`visual_chat_monitor.py`):** AI-powered visual email/WhatsApp monitoring via real browser interface control.
- **System Control (`system_control.py`):** System-level automation including:
  - **Lock Screen:** Cross-platform screen locking for Windows, macOS, and Linux
  - **Shutdown System:** Configurable delayed shutdown with cancellation support (default 10 seconds on Windows, 1 minute on Unix)
  - **Restart System:** Configurable delayed restart with cancellation support
  - **Power Action Management:** Automatic cancellation of previous power actions when scheduling new ones
  - Brightness/volume control, microphone muting, sleep scheduling, and disk cleanup
- **System Monitoring (`system_monitor.py`):** Monitors system resources.
- **Advanced File Operations (`advanced_file_operations.py`):** Includes searching, duplicate finding, and organization.
- **Workflow Management (`workflow_templates.py`):** For saving and reusing automation workflows.
- **Voice Assistant (`voice_assistant.py`):** ULTRA-INTELLIGENT interactive voice commanding system with advanced AI capabilities. Features include:
  - **Wake Words:** Multiple wake words including Simple ("Hello", "Open", "Search") and Hindi ("Bhai", "Bhaiya", "Bhaisahb") with ultra-fast "bhai" detection (0.3s response time)
  - **Natural Language Understanding (NLU):** 100% accuracy with 10+ intent synonym groups - understands variations like "launch"="open"="fire up"="start"
  - **Context Awareness:** Remembers last command for "do it again" and "repeat that" functionality
  - **Entity Extraction:** Auto-extracts numbers (digits and words), times, and app names from commands
  - **Learning Capability:** Tracks command frequency and usage patterns, provides smart suggestions
  - **Conversation History:** Stores last 20 commands with timestamps for pattern analysis
  - **Fuzzy Matching:** 80%+ similarity threshold for handling typos and variations
  - **Voice Changing:** 8 voice presets (male, female, robot, chipmunk, deep, funny, fast, slow) with 6 speed settings
  - **130+ Commands:** Across 19 categories with natural language variations
  - **Perfect Test Score:** 100% accuracy (23/23 intelligent tests passed)
  - Uses Google Speech Recognition with ultra-high sensitivity (energy threshold: 100) and pyttsx3 for text-to-speech
  - 421 total features with 20 new intelligent NLP capabilities
- **Productivity Tracking (`productivity_monitor.py`):** Monitors screen time and blocks distractions.
- **AI Features Module (`ai_features.py`):** Provides 80+ AI capabilities across 17 categories.
- **Data Analysis Suite (`data_analysis.py`):** Professional-grade toolkit for data import/export, cleaning, analysis, visualization, and machine learning.
- **Behavioral Learning Engine (`behavioral_learning.py`):** AI-powered habit tracking and pattern prediction.
- **AI Workspace Management (`workspace_manager.py`):** Offers virtual work environments, smart clipboard history, and intelligent notifications.
- **Voice & Multimodal Control (`multimodal_control.py`):** Enhanced voice interaction with custom phrase training and gesture mapping.
- **Advanced AI Automation (`advanced_ai_automation.py`):** Features email summarization, AI document generation, code review assistance, and visual workflow builder.
- **Data Intelligence Extensions (`data_intelligence.py`):** Includes anomaly detection, interactive dashboard creation, and AI-powered query builder.
- **Communication & Collaboration (`collaboration_tools.py`):** Provides meeting transcript recording and AI presentation generation.
- **Communication Enhancements (`communication_enhancements.py`):** Advanced communication features including smart replies, email priority ranking, and chat summarization.
- **Desktop File Controller (`desktop_controller_integration.py`):** Cross-platform desktop file management.
- **Creative Utilities (`creative_utilities.py`):** Offers text-to-image generation, voice model creation, and AI scriptwriting.
- **Security Enhancements (`security_enhancements.py`):** Features smart access control and real-time threat detection.
- **Human-like Interaction (`human_interaction.py`):** Incorporates conversation context recall and adaptive AI tone.
- **Cloud & Extension Ecosystem (`cloud_ecosystem.py`):** Supports multi-item cloud sync, a custom plugin framework, and mobile device connectivity.
- **Intelligent Task Automator (`intelligent_task_automator.py`):** Intelligent automation for mouse, keyboard, and screen control, including a Natural Language Task Parser and Website-Specific Automation Controllers.
- **Comprehensive Desktop Controller (`comprehensive_desktop_controller.py`):** Advanced 3-phase automation system with Deep Prompt Understanding, Intelligent Task Breakdown, and Real-Time Screen Monitoring. Integrated into the GUI's "🎯 Smart Control" tab.
- **Virtual Language Model (`virtual_language_model.py`):** Self-learning AI system that observes the screen, builds a knowledge base, and controls the desktop intelligently. Features persistent memory (`vlm_memory.json`). Integrated into GUI's "🧠 Learning AI" tab.
- **VATSAL Desktop Automator (`vatsal_desktop_automator.py`):** Intelligent desktop automator using local scripts for execution and Gemini AI for natural language understanding and task decomposition. Accessible via CLI and GUI app's "⚡ VATSAL Auto" tab.
- **Self-Operating Computer (`self_operating_computer.py`):** Enhanced autonomous AI computer control using Gemini Vision (Gemini 2.0 Flash Exp) for screen analysis and autonomous mouse/keyboard actions. Features improved decision making, OCR, error recovery, and log callback support. Integrated into GUI's "🎮 Self-Operating" tab.
- **Self-Operating Integration Hub (`self_operating_integrations.py`):** Bridges the self-operating computer with other VATSAL modules through task complexity analysis and intelligent module routing.
- **Task Coordinator (`self_operating_coordinator.py`):** Orchestrates complex multi-step tasks across all VATSAL modules with AI-powered planning, automatic module selection, and comprehensive error recovery.
- **Enhanced Command Executor (`command_executor_integration.py`):** Intelligent command router that automatically triggers self-operating mode when appropriate, with options for auto, prefer, and force modes.
- **Real-Time WebSocket System:**
  - **WebSocket Server (`websocket_server.py`):** Flask-SocketIO based server providing real-time bidirectional communication on port 5000
  - **WebSocket Client (`websocket_client.py`):** Integrated client for broadcasting events from GUI to connected dashboards
  - **Live Dashboard (`templates/dashboard.html`):** Modern web-based dashboard with real-time system monitoring, command execution tracking, and activity feed
  - **System Stats Broadcasting:** CPU, memory, and disk usage updated every 2 seconds
  - **Command Event Broadcasting:** Real-time updates for command start, completion, and failure
  - **Multi-client Support:** Unlimited simultaneous connections with synchronized updates
  - **Remote Access:** Access dashboard from any browser on the network
  - **Beautiful UI:** Dark-themed, responsive design with smooth animations and notifications
- **Mobile Companion System (`mobile_companion_server.py`):** Complete mobile control solution for VATSAL desktop automation
  - **Mobile API (`mobile_api.py`):** REST API with endpoints for command execution, system monitoring, and quick actions
  - **Mobile Web Interface (`templates/mobile.html`):** Touch-optimized responsive interface for phone/tablet control
  - **Authentication System (`mobile_auth.py`):** PIN-based authentication with token management and API key support
  - **Push Notifications (`notification_service.py`):** Multi-channel notifications via SMS (Twilio), Email, and Webhooks
  - **Remote Screenshot Viewing:** Live screenshot capture with compression and caching for mobile viewing
  - **Quick Action Shortcuts:** 16+ pre-configured one-tap actions (lock, shutdown, volume, media control, etc.)
  - **Voice Command Forwarding:** Execute voice commands from mobile to desktop
  - **Real-Time Updates:** WebSocket integration for live system stats and command status
  - **Security Features:** Session management, token expiration (24h), IP tracking, and activity logging
  - **System Monitoring:** Real-time CPU, memory, disk, and battery status from mobile
  - **Mobile-First Design:** Progressive Web App support, add-to-homescreen, touch gestures
- **Automation Recording & Macro System (`macro_recorder.py`):** Professional macro recording and playback system for desktop automation
  - **Action Recording:** Captures mouse clicks, movements, scrolls, and keyboard events with precise timing
  - **Accurate Playback:** Replays recorded sequences with millisecond precision and timing accuracy
  - **Macro Management:** Save, load, list, and delete macros stored as JSON files
  - **Loop Support:** Repeat macros 1-∞ times for batch automation
  - **Speed Control:** Adjust playback speed from 0.1x to 10x (slow motion to ultra-fast)
  - **Pre-built Templates:** Ready-made macros for multi-click sequences, form filling, screenshots, window switching
  - **Event System:** Comprehensive event types (move, click, scroll, key_press, key_release)
  - **Thread-Safe Execution:** Non-blocking recording and playback with callbacks
  - **Cross-Platform:** Works on Windows, macOS, and Linux via pynput and PyAutoGUI
  - **Smart Recording:** Optimizes mouse movements (100ms intervals) to reduce file size
  - **Stop Controls:** Cancel recording or playback anytime with stop methods
- **Utility Modules:** Spotify Integration, YouTube Integration, Weather & News, Translation, Calculator, Password Vault, Quick Notes, and Calendar Manager.

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
- **cryptography:** For encryption.
- **requests:** For HTTP API calls.
- **Replit Spotify Connector:** For Spotify API integration.
- **wttr.in API:** For weather data.
- **Google Translate API:** For language translation.
- **opencv-python:** For screen monitoring and image analysis.
- **Data Science Libraries:** pandas, numpy, scikit-learn, matplotlib, seaborn, statsmodels, nltk, openpyxl.