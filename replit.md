# AI Desktop Automation Controller

## Overview
An intelligent desktop automation tool powered by Google's Gemini AI that interprets natural language commands and executes them on desktop computers. Built with Python 3.11 and designed to make computer automation accessible to non-technical users.

## Project Architecture

### Core Components

1. **gemini_controller.py** - AI Command Parser
   - Integrates with Gemini API (gemini-2.0-flash-exp model)
   - Parses natural language into structured JSON actions
   - Provides AI suggestions and help
   - Handles single actions and multi-step workflows

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

4. **main.py** - CLI Interface
   - Interactive command-line interface
   - User-friendly prompts and help system
   - Environment validation (checks for API key)
   - Special commands (help, position, exit)

## Features Implemented

### Natural Language Processing
- AI-powered command interpretation using Gemini
- Support for single commands and multi-step workflows
- Context-aware error handling with AI suggestions

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

### Safety & Error Handling
- PyAutoGUI failsafe (emergency stop)
- Graceful degradation in headless environments
- Demo mode for testing without GUI
- Detailed error messages
- Input validation

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

### Usage Notes
- Application runs in **DEMO MODE** in Replit's cloud environment (no GUI available)
- Designed to be deployed on user's local desktop for full functionality
- In demo mode, all commands are simulated and logged for testing
- Full automation requires a desktop environment with display

## Example Commands

Simple actions:
- "Open notepad"
- "Type Hello World"
- "Take a screenshot"
- "Press enter"

Multi-step workflows:
- "Open notepad and type my name"
- "Search Google for Python tutorials"

Utility commands:
- `help` - Show features
- `position` - Display mouse coordinates
- `exit` - Stop controller

## Future Enhancements (Not Yet Implemented)
- Voice control with speech recognition
- Task scheduling and reminders
- Persistent workflow storage
- Visual workflow builder GUI
- Data extraction from screenshots
- Adaptive error recovery
- Activity logging and history

## User Preferences
None specified yet.
