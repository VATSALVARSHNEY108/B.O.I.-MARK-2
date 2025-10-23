# AI Desktop Automation Controller

## Overview
An intelligent desktop automation tool powered by Google's Gemini AI that interprets natural language commands and executes them on desktop computers. Now enhanced with **80+ features** including system control, voice commands, productivity monitoring, smart typing, auto-organization, file management, web automation, and fun features. Built with Python 3.11 and designed to make computer automation accessible to non-technical users.

## Project Architecture

### Core Components

1. **gemini_controller.py** - AI Command Parser
   - Integrates with Gemini API (gemini-2.0-flash-exp model)
   - Parses natural language into structured JSON actions
   - Provides AI suggestions and help
   - Handles single actions and multi-step workflows
   - **NEW**: Extended with messaging and contact management commands

2. **gui_automation.py** - GUI Automation Module
   - Wraps PyAutoGUI for desktop control
   - Gracefully handles headless environments with demo mode
   - Supports mouse, keyboard, application, and clipboard operations
   - Cross-platform support (Windows, macOS, Linux)

3. **command_executor.py** - Command Execution Engine
   - Maps parsed commands to automation functions
   - Executes single actions and complex workflows
   - Provides detailed feedback on success/failure
   - Error handling and validation
   - **NEW**: Integrated with messaging service and contact manager

4. **contact_manager.py** - Contact Management System
   - **NEW**: Stores and manages contact information
   - JSON-based persistent storage (contacts.json)
   - Add, update, delete, search, and list contacts
   - Case-insensitive name lookups

5. **messaging_service.py** - Messaging Service
   - **NEW**: Handles SMS, email, and file sending
   - Integrates with Twilio for SMS
   - Supports Gmail for email with attachments
   - Demo mode for testing without real credentials
   - Automatically uses available contact methods

6. **code_generator.py** - Comprehensive Code Generation Module
   - **NEW**: Advanced AI code generation system
   - Auto-detects programming language from description
   - Supports 10+ languages (Python, JavaScript, Java, C++, etc.)
   - Clean code output with markdown removal
   - Additional features: explain_code, improve_code, debug_code
   - Language templates with file extensions and editors
   - Robust error handling and validation

7. **code_executor.py** - Code Execution Module
   - **NEW**: Safely execute generated code
   - Run Python and JavaScript code
   - Safety validation before execution
   - Timeout protection
   - Capture output and errors

8. **conversation_memory.py** - Memory & Context System
   - **NEW**: Tracks conversation history
   - Remembers previous commands and results
   - Searchable history
   - Usage statistics
   - Persistent storage

9. **screenshot_analyzer.py** - AI Vision Module
   - **NEW**: Analyze screenshots with Gemini Vision
   - Extract text from images (OCR)
   - Find UI elements
   - Compare screenshots
   - Image understanding

10. **system_monitor.py** - System Monitoring
    - **NEW**: Monitor CPU, RAM, disk usage
    - Network statistics
    - Battery information
    - Process management
    - System health reports

11. **advanced_file_operations.py** - File Management
    - **NEW**: Advanced file operations
    - Search files by pattern
    - Find large files
    - Calculate directory sizes
    - Find duplicates
    - Organize files by extension

12. **workflow_templates.py** - Workflow Management
    - **NEW**: Save and reuse workflows
    - Template system
    - Usage tracking
    - Default templates
    - Persistent storage

13. **gui_app.py** - Graphical User Interface (Primary Interface)
   - **NEW**: Beautiful modern GUI with dark theme
   - Text input field with quick example buttons
   - Real-time output display with color-coded messages
   - Status indicators and help system
   - Threading for non-blocking command execution
   - Built with tkinter

14. **main.py** - CLI Interface (Alternative)
   - Interactive command-line interface
   - User-friendly prompts and help system
   - Environment validation (checks for API key)
   - Special commands (help, position, contacts, exit)
   - **NEW**: Added contacts command for quick contact listing

15. **system_control.py** - System Control Module
   - **NEW**: Auto-mute/unmute microphone
   - **NEW**: Brightness control (auto-adjust based on time)
   - **NEW**: Sleep/wake scheduling
   - **NEW**: Auto-cleanup temp files and recycle bin
   - **NEW**: Disk space monitoring

16. **app_scheduler.py** - App Automation Module
   - **NEW**: Schedule app opening at specific times
   - **NEW**: Detect idle time and close heavy apps
   - **NEW**: Heavy app monitoring
   - **NEW**: Launch multiple websites

17. **download_organizer.py** - Download Organization
   - **NEW**: Auto-organize downloads into folders
   - **NEW**: Real-time file system watching
   - **NEW**: Categorize by file type
   - **NEW**: Statistics and configuration

18. **voice_assistant.py** - Voice Commands
   - **NEW**: Speech recognition for hands-free control
   - **NEW**: Text-to-speech responses
   - **NEW**: Continuous listening mode
   - **NEW**: Voice command processing

19. **smart_typing.py** - Smart Typing Assistant
   - **NEW**: Text snippet expansion
   - **NEW**: Email template generation
   - **NEW**: Form filling automation
   - **NEW**: Auto-correct common typos
   - **NEW**: Password generation

20. **file_manager.py** - Advanced File Management
   - **NEW**: Auto-rename messy files
   - **NEW**: Duplicate file detection
   - **NEW**: Compress old files
   - **NEW**: Auto-backup folders
   - **NEW**: Backup history tracking

21. **web_automation.py** - Web Automation
   - **NEW**: Clipboard history manager
   - **NEW**: Encrypted credential storage
   - **NEW**: Web scraper shortcuts
   - **NEW**: Quick search shortcuts

22. **productivity_monitor.py** - Productivity Tracking
   - **NEW**: Screen time tracking
   - **NEW**: Distraction blocker
   - **NEW**: Focus mode
   - **NEW**: Productivity scoring
   - **NEW**: Smart reminders
   - **NEW**: Activity logging and daily summaries

23. **fun_features.py** - Fun & Motivation
   - **NEW**: Random compliments system
   - **NEW**: Task celebration messages
   - **NEW**: Mood themes
   - **NEW**: Mini chatbot companion
   - **NEW**: Playlist suggestions

## Features Implemented (80+ Features!)

### **NEW** AI Code Generation (Comprehensive)
- **Built-in Templates**: Instant code generation for common problems (works offline!)
- **Intelligent Code Writing**: Describe what you want in plain English
- **Auto-Language Detection**: Automatically detects language from description
- **10+ Languages**: Python, JavaScript, Java, C, C++, C#, Ruby, Go, HTML, CSS
- **Auto-Paste to Editor**: Opens notepad/editor and pastes perfect code
- **Educational Output**: Includes detailed comments and best practices
- **Code Explanation**: Explain what any code does
- **Code Improvement**: Get better versions of existing code
- **Code Debugging**: Fix errors in broken code
- **Clean Output**: Automatically removes markdown formatting
- **Template Library**: Palindrome, Reverse Number, Fibonacci, Factorial, Prime, Bubble Sort, Binary Search
- Examples: "Write code for checking palindrome", "Write code for reverse number"

### Natural Language Processing
- AI-powered command interpretation using Gemini
- Support for single commands and multi-step workflows
- Context-aware error handling with AI suggestions
- **NEW**: Understands messaging intent ("send to", "text", "email")
- **NEW**: Understands code generation requests ("write code for", "generate code")

### Desktop Automation Capabilities
- Application launching
- Text typing with configurable speed
- Mouse control (clicking, movement)
- Keyboard actions and hotkeys
- Screenshots
- Clipboard operations (copy/paste)
- Web search integration
- **Smart YouTube Integration**: Intelligent video search and auto-play with multiple fallback methods
- File creation
- Wait/pause functionality

### **NEW** Messaging & Communication
- **SMS Messaging**: Send text messages via Twilio
  - "Text Sarah that I'm running late"
  - "Message John about the meeting"
- **Email**: Send emails with Gmail
  - "Email my boss the report"
  - "Send email to sarah@example.com about dinner"
- **File Sharing**: Send photos and files to contacts
  - "Send this photo to John"
  - "Send report.pdf to my boss"
- **Contact Management**: Store contacts with phone/email
  - "Add contact Mom with phone 555-1234"
  - "List contacts"
  - Persistent storage in contacts.json

### Safety & Error Handling
- PyAutoGUI failsafe (emergency stop)
- Graceful degradation in headless environments
- Demo mode for testing without GUI or messaging credentials
- Detailed error messages
- Input validation
- Structural validation of AI responses

## Environment

### Dependencies
- Python 3.11
- google-genai (Gemini AI SDK)
- PyAutoGUI (GUI automation)
- pyperclip (clipboard operations)
- psutil (process management)
- python-dotenv (environment variables)

### Environment Variables
- `GEMINI_API_KEY` - Required for AI functionality
- `TWILIO_ACCOUNT_SID` - Optional for SMS (Twilio)
- `TWILIO_AUTH_TOKEN` - Optional for SMS (Twilio)
- `TWILIO_PHONE_NUMBER` - Optional for SMS (Twilio)
- `GMAIL_USER` - Optional for Email (your Gmail address)
- `GMAIL_APP_PASSWORD` - Optional for Email (Gmail app-specific password)

### Workflow
- **Name**: GUI App
- **Command**: `python gui_app.py`
- **Type**: GUI application (with VNC display)
- **Status**: Running in demo mode
- **Alternative**: `python main.py` (CLI version)

## Current State

### Recent Changes (October 23, 2025)
- ✅ **NEW**: Added 30+ new automation features across 7 categories
- ✅ **NEW**: System Control - Auto-mute, brightness, sleep scheduling, disk cleanup
- ✅ **NEW**: App Automation - Scheduled apps, idle detection, download organization
- ✅ **NEW**: Voice Commands - Hands-free control with speech recognition
- ✅ **NEW**: Smart Typing - Text snippets, email templates, auto-correct
- ✅ **NEW**: Advanced File Management - Auto-rename, duplicates, compression, backups
- ✅ **NEW**: Web Automation - Clipboard history, encrypted credentials, web scrapers
- ✅ **NEW**: Productivity Monitoring - Screen time, focus mode, distraction blocker
- ✅ **NEW**: Fun Features - Compliments, celebrations, mood themes, chatbot
- ✅ **NEW**: Updated gemini_controller.py with all new action types
- ✅ **NEW**: Updated command_executor.py with all new action handlers
- ✅ **NEW**: Created comprehensive NEW_FEATURES_GUIDE.md documentation
- ✅ **NEW**: Installed dependencies: watchdog, speechrecognition, pyttsx3, cryptography

### Previous Changes (October 22, 2025)
- ✅ Initial project setup with Python 3.11
- ✅ Integrated Gemini AI for natural language processing
- ✅ Implemented GUI automation module with PyAutoGUI
- ✅ Created command execution engine
- ✅ Built interactive CLI interface
- ✅ Added demo mode for headless environments
- ✅ Created comprehensive documentation (README.md)
- ✅ Configured .gitignore for Python projects
- ✅ **NEW**: Added contact management system
- ✅ **NEW**: Integrated Twilio for SMS messaging
- ✅ **NEW**: Added email support with attachments
- ✅ **NEW**: Extended Gemini prompts for messaging commands
- ✅ **NEW**: Added structural validation for AI responses
- ✅ **NEW**: Updated CLI with messaging examples
- ✅ **NEW**: Implemented AI Code Generation feature
- ✅ **NEW**: Auto-open editor and type generated code
- ✅ **NEW**: Support for multiple programming languages
- ✅ **NEW**: Created beautiful GUI application with tkinter
- ✅ **NEW**: Modern dark theme interface with quick examples
- ✅ **NEW**: Real-time output display and status indicators
- ✅ **NEW**: Created comprehensive code_generator.py module
- ✅ **NEW**: Auto-language detection from description
- ✅ **NEW**: Added explain_code, improve_code, debug_code functions
- ✅ **NEW**: Robust code cleaning and markdown removal
- ✅ **NEW**: Support for 10+ programming languages
- ✅ **NEW**: Added code_executor.py for safe code execution
- ✅ **NEW**: Added conversation_memory.py for context tracking
- ✅ **NEW**: Added screenshot_analyzer.py for AI Vision
- ✅ **NEW**: Added system_monitor.py for health monitoring
- ✅ **NEW**: Added advanced_file_operations.py for file management
- ✅ **NEW**: Added workflow_templates.py for reusable workflows
- ✅ **NEW**: Integrated 50+ new intelligent features
- ✅ **NEW**: Created comprehensive FEATURES_GUIDE.md documentation
- ✅ **NEW**: Added YouTube integration (search_youtube, open_youtube)
- ✅ **NEW**: YouTube search and auto-play first video functionality
- ✅ **NEW**: Added play_youtube_video action for auto-playing first search result
- ✅ **NEW**: "Play video X" command automatically searches and plays first video
- ✅ **NEW**: Updated Gemini AI prompt to understand YouTube commands
- ✅ **NEW**: Created code_templates.py with instant code generation
- ✅ **NEW**: Built-in templates for 7+ common algorithms (palindrome, fibonacci, etc.)
- ✅ **NEW**: Fallback system works even when Gemini API is down/overloaded
- ✅ **NEW**: Fixed code writing to use clipboard paste instead of typing
- ✅ **NEW**: Code now preserves perfect formatting and structure
- ✅ **NEW**: Created youtube_automation.py for intelligent video playback
- ✅ **NEW**: Smart YouTube player with 3 different fallback methods
- ✅ **NEW**: Enhanced AI understanding of video-related commands
- ✅ **NEW**: Automatic search, navigation, and playback in one command
- ✅ **NEW**: Added play_first_result() function to play first video from search page
- ✅ **NEW**: Added search_and_play() function for combined search + play action
- ✅ **NEW**: Support for "play the first video" command after searching

### Usage Notes
- Application runs in **DEMO MODE** in Replit's cloud environment (no GUI available)
- Designed to be deployed on user's local desktop for full functionality
- In demo mode, all commands (desktop + messaging) are simulated and logged
- Full automation requires a desktop environment with display
- **Messaging features** work in demo mode but require Twilio/Gmail credentials for real sending

## Example Commands

### **NEW** AI Code Generation
- "Write code for checking palindrome"
- "Generate Python code for bubble sort"
- "Create JavaScript code for form validation"
- "Write Java code for fibonacci sequence"
- "Generate C++ code for binary search"

### Desktop Automation
- "Open notepad"
- "Type Hello World"
- "Take a screenshot"
- "Press enter"
- "Search Google for Python tutorials"
- "Play video funny cats" (auto-plays first YouTube video)
- "Play video music" (searches and plays first result)
- "Search YouTube for tutorials" (just shows search results)
- "Open YouTube video [URL]"

### **NEW** Messaging Commands
- "Send this photo to John"
- "Text Sarah that I'm running late"
- "Email my boss about the meeting"
- "Send report.pdf to my manager"
- "Add contact Mom with phone 555-1234 and email mom@example.com"

### **NEW** Email Commands
- "Send email to john@example.com about the meeting"
- "Send HTML email with formatted content"
- "Send welcome email to newuser@example.com"
- "Email report.pdf to manager@example.com"
- "Send notification email about system update"

### **NEW** System Control Commands
- "Mute microphone" / "Unmute microphone"
- "Set brightness to 80%"
- "Auto-adjust brightness"
- "Schedule sleep at 11 PM"
- "Clear temp files"
- "Check disk space"
- "Empty recycle bin"

### **NEW** App Automation Commands
- "Open VS Code and Chrome at 9 AM"
- "Close heavy apps"
- "Show heavy apps"
- "Close Chrome"
- "Organize downloads"
- "Enable auto-organize downloads"

### **NEW** Voice & Typing Commands
- "Listen for voice commands"
- "Show my snippets"
- "Expand snippet //email"
- "Generate professional email template"

### **NEW** File Management Commands
- "Auto-rename files in Downloads"
- "Find duplicate files"
- "Compress old files"
- "Backup Documents folder"
- "List backups"

### **NEW** Productivity Commands
- "Show screen time"
- "Screen time dashboard"
- "Block distractions"
- "Enable focus mode for 2 hours"
- "Show my productivity score"
- "Remind me to drink water"
- "Remind me to take a break"
- "Show daily summary"

### **NEW** Fun Commands
- "Give me a compliment"
- "Celebrate this task"
- "Set mood to focused"
- "Chat with bot: Hello!"

### Utility Commands
- `help` - Show features
- `contacts` - List all contacts
- `position` - Display mouse coordinates
- `exit` - Stop controller

### **NEW** AI Screen Analysis & Suggestions (Smart Assistant)
- ✅ **Auto Screenshot + AI Analysis**: Takes screenshot and analyzes it
- ✅ **Improvement Suggestions**: AI suggests UI/UX, design, layout improvements
- ✅ **Error Detection**: Finds visible errors, bugs, broken elements
- ✅ **Quick Tips**: Get 3 instant actionable tips
- ✅ **Code Review**: AI reviews code on screen for quality, bugs, performance
- ✅ **Website Analysis**: Professional design review with specific recommendations
- ✅ **Voice Commands**: "Suggest improvements", "Check for errors", "Give me tips"
- ✅ **Standalone Tool**: Run `screen_suggester.py` for instant analysis

### WhatsApp Desktop Integration
- ✅ **Direct App Opening**: Opens installed WhatsApp Desktop (no browser needed)
- ✅ **Contact Chat Opening**: Opens specific contact chats directly
- ✅ **Message Pre-fill**: Opens chat with message ready to send
- ✅ **Cross-Platform**: Works on Windows, Mac, and Linux
- ✅ **HTML Launcher**: Simple web interface to open WhatsApp
- ✅ **URL Scheme Support**: Uses wa.me links for better compatibility

### **NEW** Enhanced Email Sending
- ✅ **Simple Text Emails**: Send plain text emails quickly
- ✅ **HTML Emails**: Send beautifully formatted HTML emails
- ✅ **Email Templates**: Pre-made templates (welcome, notification, report, invitation)
- ✅ **Attachments**: Send files with emails (multiple files supported)
- ✅ **Multiple Recipients**: Send to many people at once
- ✅ **CC & BCC Support**: Carbon copy and blind carbon copy
- ✅ **Contact Integration**: Send to saved contacts by name
- ✅ **Gmail Integration**: Uses Gmail SMTP (secure app passwords)
- ✅ **Quick Email Tool**: `quick_email.py` for instant email sending
- ✅ **Voice Commands**: "Send email to...", "Email with attachment..."

## Future Enhancements (Potential)
- Visual workflow builder GUI with drag-and-drop
- Adaptive error recovery with AI
- Slack/Discord messaging integration
- Calendar integration (Google Calendar, Outlook)
- Machine learning for task prediction
- Cross-device synchronization
- Plugin system for custom features

## User Preferences
None specified yet.
