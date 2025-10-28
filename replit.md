# AI Desktop Automation Controller

## Overview
The AI Desktop Automation Controller is an intelligent desktop automation tool powered by Google's Gemini AI. It interprets natural language commands to execute a wide range of tasks on desktop computers. The project offers a unified ecosystem with over 300+ features, including smart Desktop RAG for file intelligence, 9 Smart Automation & AI features, and 8 Communication Enhancement features. Its core purpose is to be a comprehensive productivity powerhouse, integrating advanced AI for code generation, screen analysis, natural language understanding, professional-grade data analysis, and various utility modules.

## User Preferences
- **Chat Monitoring:** User prefers visual/screen-based chat monitoring where AI controls the real Gmail/WhatsApp interface on screen, rather than background API calls. This allows them to watch the AI work in real-time.

## System Architecture
The AI Desktop Automation Controller is built with Python 3.11 and utilizes a modular architecture.

### UI/UX Decisions
The primary interface is a GUI application (`gui_app.py`) featuring a modern, dark-themed, tabbed design (Version 2.0.0 - VATSAL Edition) with over 50 functions organized across 10 categories. Key UI elements include a 1400x900 window, Segoe UI fonts, a live clock, card-based design with gradient effects, quick-access buttons, and a real-time color-coded output console. It's built with `tkinter` and uses threading for non-blocking execution. A CLI interface (`main.py`) offers an interactive command-line alternative.

**Feature Toggles:** The GUI header includes two prominent toggle buttons:
- **🤖 VATSAL Mode Toggle:** Switches between VATSAL's sophisticated personality mode and standard direct responses
- **🎮 Self-Operating Toggle:** Enables/disables the self-operating computer feature, allowing users to control when AI can autonomously control the desktop. When disabled, attempts to use self-operating features show a clear warning message guiding users to re-enable it from the header.

The Advanced Smart Screen Monitor is integrated into the GUI's AI Features tab, providing one-click access to 8 specialized AI analysis modes and analytics reporting.

The VATSAL AI Assistant (`vatsal_assistant.py`) is an intelligent AI companion with a sophisticated, British-inspired personality, contextual awareness, conversation memory, time-aware greetings, and proactive suggestions. A simple, powerful intelligent chatbot (`vatsal_ai.py`) and a streamlined, beginner-friendly Simple VATSAL Chatbot (`simple_chatbot.py`) powered by Google Gemini 2.5 Flash are also available. All three chatbot systems are unified in the GUI App under the "💬 VATSAL Chat" tab.

### Technical Implementations
- **AI Command Parser (`gemini_controller.py`):** Integrates with Gemini API for natural language processing, converting commands into structured JSON actions.
- **GUI Automation Module (`gui_automation.py`):** Utilizes PyAutoGUI for cross-platform desktop control, including folder navigation and file manager integration.
- **Messaging Service (`messaging_service.py`):** Handles SMS, email, and WhatsApp Desktop integration.
- **Code Generation & Execution Modules:** AI-powered code generation, explanation, debugging, and safe execution for Python/JavaScript.
- **AI Vision Module (`screenshot_analyzer.py`):** Uses Gemini Vision for OCR, UI element identification, and screen analysis.
- **Desktop RAG System (`desktop_rag.py`):** Indexes desktop files for semantic search, AI-powered Q&A, and folder summarization.
- **Smart Automation & AI Module (`smart_automation.py`):** Includes 9 AI-powered features like Auto-Bug Fixer, Meeting Scheduler AI, and Smart File Recommendations.
- **Visual Chat Monitor (`visual_chat_monitor.py`):** AI-powered visual email/WhatsApp monitoring that controls the real browser interface using AI Vision.
- **System Monitoring (`system_monitor.py`):** Monitors CPU, RAM, disk, network, and battery.
- **Advanced File Operations (`advanced_file_operations.py`):** Includes searching, duplicate finding, and organization.
- **Workflow Management (`workflow_templates.py`):** For saving, reusing, and tracking custom automation workflows.
- **Voice Commands (`voice_assistant.py`):** Basic speech recognition and text-to-speech framework.
- **Voice Commander (`voice_commander.py`):** Enhanced comprehensive voice commanding system with push-to-talk and continuous listening modes. Features Google Speech Recognition for voice input, pyttsx3 for text-to-speech output, background threading for non-blocking operation, smart audio management with queuing, and wake word detection capabilities. Fully integrated into GUI with dedicated voice control buttons (🎤 push-to-talk, 🔊 continuous listening), automatic execution of spoken commands, and text-to-speech responses from VATSAL. Supports all 300+ features via voice control with visual feedback and status indicators.
- **Productivity Tracking (`productivity_monitor.py`):** Monitors screen time and blocks distractions.
- **AI Features Module (`ai_features.py`):** Provides 80+ AI capabilities across 17 categories (e.g., Chatbots, Text/Image Generation, Data Analysis).
- **Data Analysis Suite (`data_analysis.py`):** Professional-grade toolkit with 100+ features covering Data Import/Export, Cleaning, Analysis, Visualization, and Machine Learning.
- **Behavioral Learning Engine (`behavioral_learning.py`):** AI-powered habit tracking and pattern prediction.
- **AI Workspace Management (`workspace_manager.py`):** Offers virtual work environments, smart clipboard history, and intelligent notifications.
- **Voice & Multimodal Control (`multimodal_control.py`):** Enhanced voice interaction with custom phrase training and gesture mapping.
- **Advanced AI Automation (`advanced_ai_automation.py`):** Features email summarization, AI document generation, code review assistance, and visual workflow builder.
- **Data Intelligence Extensions (`data_intelligence.py`):** Includes anomaly detection, interactive dashboard creation, and AI-powered query builder.
- **Communication & Collaboration (`collaboration_tools.py`):** Provides meeting transcript recording and AI presentation generation.
- **Communication Enhancements (`communication_enhancements.py`):** Advanced communication features including smart replies, email priority ranking, follow-up reminders, meeting notes auto-sender, chat summarization, multilingual replies, and voice-to-task conversion.
- **Desktop File Controller (`desktop_controller_integration.py`, `desktop_file_controller.bat`):** Cross-platform desktop file management system with Windows batch file and Python integration.
- **Creative Utilities (`creative_utilities.py`):** Offers text-to-image generation, voice model creation, and AI scriptwriting.
- **Security Enhancements (`security_enhancements.py`):** Features smart access control and real-time threat detection.
- **Human-like Interaction (`human_interaction.py`):** Incorporates conversation context recall and adaptive AI tone.
- **Cloud & Extension Ecosystem (`cloud_ecosystem.py`):** Supports multi-item cloud sync, a custom plugin framework, and mobile device connectivity.
- **Intelligent Task Automator (`intelligent_task_automator.py`):** Comprehensive intelligent automation system for mouse, keyboard, and screen control, including a Natural Language Task Parser, AI Vision Screen Understanding, and Website-Specific Automation Controllers (LeetCode, GitHub, YouTube, etc.).
- **Comprehensive Desktop Controller (`comprehensive_desktop_controller.py`):** Advanced 3-phase automation system featuring Deep Prompt Understanding (analyzes intent, complexity, requirements), Intelligent Task Breakdown (creates detailed execution plans with checkpoints), and Real-Time Screen Monitoring (captures before/during/after states, AI verification of outcomes, adaptive execution with error recovery). Fully integrated into the GUI with dedicated "🎯 Smart Control" tab featuring visual phase indicators, quick action buttons, real-time output display, and comprehensive help system.
- **Virtual Language Model (`virtual_language_model.py`):** Self-learning AI system that observes the screen, builds knowledge about the desktop environment, and controls it intelligently. Features: Screen observation with AI vision, knowledge base building (UI patterns, application knowledge, workflows), intelligent decision making, autonomous learning sessions, persistent memory (`vlm_memory.json`). Fully integrated into GUI with dedicated "🧠 Learning AI" tab featuring real-time stats, observation controls, decision engine, and knowledge query interface.
- **VATSAL Desktop Automator (`vatsal_desktop_automator.py`, `vatsal_enhanced_modules.py`):** Intelligent desktop automator that combines local automation scripts with minimal Gemini API support. Uses Gemini ONLY for natural language understanding and task decomposition - all execution happens locally via Python modules (pyautogui, psutil, subprocess, OpenCV). Features: Application control (open, close, switch), file/folder management (create, delete, move, organize), input automation (keyboard, mouse, clipboard), screen operations (screenshots, analysis, monitoring), system monitoring (CPU, RAM, disk, processes), and safety confirmations for destructive actions. Accessible via CLI (`python vatsal_desktop_automator.py`) and GUI app's "⚡ VATSAL Auto" tab with quick actions, concise responses, and risk-based operation approval.
- **Self-Operating Computer (`self_operating_computer.py`):** Enhanced autonomous AI computer control powered by Gemini Vision (Gemini 2.0 Flash Exp). AI views the screen like a human, analyzes with vision AI, and autonomously performs mouse/keyboard actions. **Enhanced Features (v2.0):** Advanced action types (click_element, click_position, type_text, press_key, hotkey, scroll, drag, screenshot_analysis), improved decision making with confidence scoring, OCR capabilities for text extraction, element detection and clicking, log callback support for GUI integration, enhanced error recovery and fallback strategies. **Integration Features:** Seamless integration with all VATSAL modules via SelfOperatingIntegrationHub, intelligent task routing, progress tracking, session history. Fully integrated into GUI with dedicated "🎮 Self-Operating" tab featuring objective input, auto-control toggle button, status indicators, real-time colored output display, control buttons, and screenshot gallery. Use cases: Visual UI navigation, interactive exploration, autonomous task completion from high-level goals. Accessible via CLI (`python self_operating_computer.py`) and GUI app's "🎮 Self-Operating" tab. Max 30 iterations per session for safety.
- **Self-Operating Integration Hub (`self_operating_integrations.py`):** Advanced integration system that bridges self-operating computer with all VATSAL modules (comprehensive controller, VLM, command executor). **Features:** Task complexity analysis, intelligent module routing (self_operating/comprehensive/vlm/hybrid), context sharing and memory, progress tracking across modules, error recovery and fallback strategies, session history and logging. SmartTaskRouter analyzes tasks and routes to the best execution method based on task characteristics (visual navigation, structured commands, learning tasks, complex multi-step workflows). Enables seamless collaboration between autonomous vision-based control and traditional automation.
- **Task Coordinator (`self_operating_coordinator.py`):** Orchestrates complex multi-step tasks across all VATSAL modules with AI-powered planning and execution. **Features:** Intelligent task decomposition using Gemini AI, automatic module selection for each step, support for sequential/parallel/hybrid execution strategies, progress tracking with callbacks, comprehensive error recovery, execution logging and analytics. Plans tasks by analyzing complexity, estimating duration, identifying dependencies, and creating detailed execution plans. Integrates with SelfOperatingIntegrationHub for unified task execution across the entire VATSAL ecosystem.
- **Enhanced Command Executor (`command_executor_integration.py`):** Intelligent command router that enables natural language commands to automatically trigger self-operating mode when appropriate. **Features:** Automatic task analysis and mode selection, smart routing between self-operating and traditional execution, learning from execution patterns, execution statistics and analytics, CommandInterceptor for pre-execution analysis and recommendations. Supports auto mode (analyzes each command), prefer mode (favors self-operating), and force mode (manual override). Provides unified interface for all command types with seamless fallback between execution modes.
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
- **opencv-python:** For screen monitoring and image analysis in VATSAL Automator.
- **Data Science Libraries:** pandas, numpy, scikit-learn, matplotlib, seaborn, statsmodels, nltk, openpyxl.