# AI Desktop Automation Controller

## Overview
An intelligent desktop automation tool powered by Google's Gemini AI that interprets natural language commands and executes them on desktop computers. Now enhanced with **advanced messaging capabilities** to send SMS, emails, and files to contacts using natural language. Built with Python 3.11 and designed to make computer automation accessible to non-technical users.

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

## Features Implemented

### **NEW** AI Code Generation (Comprehensive)
- **Intelligent Code Writing**: Describe what you want in plain English
- **Auto-Language Detection**: Automatically detects language from description
- **10+ Languages**: Python, JavaScript, Java, C, C++, C#, Ruby, Go, HTML, CSS
- **Auto-Type to Editor**: Opens notepad/editor and types the code
- **Educational Output**: Includes detailed comments and best practices
- **Code Explanation**: Explain what any code does
- **Code Improvement**: Get better versions of existing code
- **Code Debugging**: Fix errors in broken code
- **Clean Output**: Automatically removes markdown formatting
- Examples: "Write code for checking palindrome", "Generate bubble sort"

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
- **YouTube Integration**: Search and play videos
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

### Recent Changes (October 22, 2025)
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
- ✅ **NEW**: Updated Gemini AI prompt to understand YouTube commands

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
- "Search YouTube for funny cats"
- "Play music video on YouTube"
- "Open YouTube video [URL]"

### **NEW** Messaging Commands
- "Send this photo to John"
- "Text Sarah that I'm running late"
- "Email my boss about the meeting"
- "Send report.pdf to my manager"
- "Add contact Mom with phone 555-1234 and email mom@example.com"

### Utility Commands
- `help` - Show features
- `contacts` - List all contacts
- `position` - Display mouse coordinates
- `exit` - Stop controller

## Future Enhancements (Not Yet Implemented)
- Voice control with speech recognition
- Task scheduling and reminders
- Persistent workflow storage
- Visual workflow builder GUI
- Data extraction from screenshots using Gemini vision
- Adaptive error recovery
- Activity logging and history
- WhatsApp integration
- Slack/Discord messaging
- Calendar integration

## User Preferences
None specified yet.
