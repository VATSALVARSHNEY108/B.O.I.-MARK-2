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

6. **main.py** - CLI Interface
   - Interactive command-line interface
   - User-friendly prompts and help system
   - Environment validation (checks for API key)
   - Special commands (help, position, contacts, exit)
   - **NEW**: Added contacts command for quick contact listing

## Features Implemented

### **NEW** AI Code Generation
- **Intelligent Code Writing**: Describe what you want in plain English
- **Multi-Language Support**: Python, JavaScript, Java, C++, and more
- **Auto-Type to Editor**: Opens notepad/editor and types the code
- **Educational Output**: Includes comments and best practices
- Examples: "Write code for checking palindrome", "Generate bubble sort in Python"

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
- **Name**: Automation Controller
- **Command**: `python main.py`
- **Type**: Console application
- **Status**: Running in demo mode (headless environment)

## Current State

### Recent Changes (October 21, 2025)
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
