# AI Desktop Automation Controller

## Overview
An intelligent desktop automation tool powered by Google's Gemini AI, designed to interpret natural language commands and execute them on desktop computers. The project aims to make computer automation accessible to non-technical users by providing over 80 features, including system control, voice commands, productivity monitoring, smart typing, auto-organization, file management, web automation, and fun features. It integrates advanced AI capabilities for code generation, screen analysis, and natural language understanding to streamline various desktop tasks and enhance user interaction.

## User Preferences
None specified yet.

## System Architecture
The AI Desktop Automation Controller is built with Python 3.11 and features a modular architecture.

### UI/UX Decisions
- **Enhanced GUI Application (`gui_app.py`):** Features a modern dark theme with a tabbed interface organizing 50+ functions into 6 categories (Code Generation, Desktop Automation, Messaging, System Control, Productivity, and Fun Features). Includes quick-access buttons for all major functions, text input field, real-time color-coded output display, status indicators, and comprehensive help documentation. Utilizes `tkinter` with scrollable panels and threading for non-blocking command execution. Fully functional in cloud/headless environments with graceful degradation.
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
- **YouTube Integration:** Intelligent video search, auto-play (with multiple fallback methods), and direct video opening.
- **Enhanced Email Sending:** Supports simple text, HTML, and templated emails with attachments, multiple recipients, CC/BCC, and integration with Gmail via SMTP.

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
- **Twilio:** For SMS messaging (requires `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`).
- **Gmail SMTP:** For email sending (requires `GMAIL_USER`, `GMAIL_APP_PASSWORD`).
- **watchdog:** For real-time file system watching (download organizer).
- **speechrecognition:** For voice commands.
- **pyttsx3:** For text-to-speech responses.
- **cryptography:** For encrypted credential storage.