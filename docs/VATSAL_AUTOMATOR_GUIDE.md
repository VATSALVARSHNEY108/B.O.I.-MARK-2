# BOI Desktop Automator Guide

## Overview

**BOI** is an intelligent desktop automator that combines local automation scripts with minimal Gemini API support. Unlike other automation tools, BOI uses AI **only** for natural language understanding and task decomposition - all execution happens locally via Python modules.

## Purpose

- 🧠 **Interpret user commands** using Gemini for natural language understanding
- 💻 **Plan tasks** intelligently by breaking complex requests into simple steps
- ⚡ **Execute locally** using Python modules (no external APIs for actions)
- ✅ **Safe operation** with confirmations for destructive actions

## Core Abilities (Local Execution Only)

### Application Control
- ✓ Open, close, or switch between applications
- ✓ Control windows (minimize, maximize, switch)
- ✓ Launch specific programs by name

### File & Folder Management
- ✓ Create, delete, move, and rename files
- ✓ Open folders (Desktop, Documents, Downloads, custom paths)
- ✓ Search for files and organize by type
- ✓ Get file information and directory sizes

### Input Automation
- ✓ Simulate keyboard inputs (type text, press keys, hotkeys)
- ✓ Simulate mouse inputs (click, move, drag)
- ✓ Clipboard operations (copy, paste, clear)

### Screen Operations
- ✓ Take screenshots (full screen or regions)
- ✓ Analyze screen with OpenCV
- ✓ Monitor for screen changes
- ✓ Detect colors and regions

### System Monitoring
- ✓ CPU, RAM, disk, battery status
- ✓ Running processes and resource usage
- ✓ Network information
- ✓ System health reports

## Rules & Safety

### 1. AI Usage Boundary
- ✅ **Gemini API used for**: Understanding intent, reasoning, task decomposition
- ❌ **Gemini API NOT used for**: Direct action execution, system control, file operations

### 2. Local Execution Only
All execution happens via local Python modules:
- `pyautogui` - GUI automation
- `psutil` - System monitoring
- `subprocess` - Application launching
- `os` / `pathlib` - File operations
- `cv2` (OpenCV) - Screen analysis
- `pyperclip` - Clipboard operations

### 3. Safety Confirmations
- ⚠️ **Destructive actions** (file deletion, process termination) require user confirmation
- 🔒 Actions are categorized by risk level: `safe`, `moderate`, `destructive`
- 👤 User approves all high-risk operations before execution

### 4. Clarity First
- ❓ **Unclear commands** trigger clarification requests
- 🚫 **Unsafe commands** are blocked with explanation
- 💬 Brief, concise responses focused on execution results

## Usage

### CLI Mode

```bash
python vatsal_desktop_automator.py
```

**Example Commands:**
```
🎯 Command: Open notepad and type Hello World
🎯 Command: Take a screenshot and save it
🎯 Command: Show me system information
🎯 Command: Open Desktop folder
```

### GUI Mode

1. Launch the GUI app: `python gui_app.py`
2. Navigate to the **⚡ BOI Auto** tab
3. Enter commands in natural language
4. Use quick action buttons for common tasks

**Quick Actions:**
- 💻 System Info - Display CPU, RAM, disk status
- 📸 Screenshot - Capture current screen
- 📂 Open Desktop - Open Desktop folder
- 📝 Notepad - Launch Notepad application
- 🧹 Clear Output - Clear the output display

## Example Workflows

### Example 1: Simple Task
**User:** "Open notepad and type Hello"

**BOI Process:**
1. 🧠 Gemini understands: Open app + type text
2. ⚡ Local execution:
   - Launch notepad.exe via subprocess
   - Wait 1 second
   - Type "Hello" via pyautogui
3. ✅ Result: "✓ Opened notepad\n✓ Typed: Hello"

### Example 2: System Optimization
**User:** "Optimize my workspace and show system info"

**BOI Process:**
1. 🧠 Gemini decomposes: Multiple tasks
2. ⚡ Local execution:
   - Get system information (CPU, RAM, disk)
   - Minimize windows
   - Clear clipboard
   - Display report
3. ✅ Result: Concise system report with metrics

### Example 3: Destructive Action (with confirmation)
**User:** "Delete the old_files folder"

**BOI Process:**
1. 🧠 Gemini identifies: Destructive action
2. ⚠️ Confirmation prompt: "This action is destructive: Delete folder with files. Continue? (yes/no)"
3. 👤 User approves or cancels
4. ⚡ If approved, execute deletion locally
5. ✅ Result: "✓ Deleted folder: old_files" (or "❌ Cancelled")

## Key Differentiators

| Feature | BOI | Traditional Automation |
|---------|--------|----------------------|
| Command Input | Natural language | Scripted commands |
| AI Role | Understanding only | Often both understanding AND execution |
| Execution | 100% local | May use external APIs |
| Safety | Automatic confirmations | Manual checks needed |
| Responses | Brief, focused | Often verbose |

## Advanced Features

### Screen Monitoring (via vatsal_enhanced_modules.py)
- Capture and analyze screen content
- Detect changes over time
- Find specific colors/regions
- Save screen regions

### File Operations
- Search files by pattern
- Find large files
- Organize by extension
- Calculate directory sizes
- Find duplicates

### System Control
- List running processes
- Get top resource consumers
- Network statistics
- Complete system health reports
- Battery monitoring

### Automation Workflows
- Pre-built common workflows
- Workspace optimization
- Quick screenshot analysis
- System health checks

## Technical Architecture

```
User Command
     ↓
[Gemini API] ← Only for NLU & Task Decomposition
     ↓
Intent + Action Plan (JSON)
     ↓
[Local Execution Engine]
     ↓
Python Modules (pyautogui, psutil, os, cv2, etc.)
     ↓
System Actions
     ↓
Brief, Focused Result
```

## Configuration

Requires only:
- `GEMINI_API_KEY` environment variable (for command understanding)
- Python packages: See `requirements.txt`

No additional API keys or services needed for execution.

## Best Practices

### ✅ DO:
- Use natural language commands
- Be specific about what you want
- Trust the confirmation prompts
- Review destructive actions before approving

### ❌ DON'T:
- Try to execute network/cloud actions (not supported)
- Bypass safety confirmations
- Expect verbose AI chat (designed for brevity)
- Use for tasks requiring external services

## Troubleshooting

**Issue:** "GEMINI_API_KEY not found"
- **Solution:** Add `GEMINI_API_KEY` to your environment variables or `.env` file

**Issue:** "Could not understand command"
- **Solution:** Rephrase more clearly or break into smaller steps

**Issue:** "Action failed to execute"
- **Solution:** Check if the target app/file exists and you have permissions

**Issue:** "Confirmation not appearing"
- **Solution:** GUI confirmations appear in console for CLI mode; ensure terminal is visible

## Security & Privacy

- ✅ All execution is local - no data sent to external services except command text to Gemini for understanding
- ✅ No storage of sensitive information
- ✅ Destructive actions require explicit approval
- ✅ Open source - inspect the code yourself

## Future Enhancements

Planned improvements:
- 🔄 Voice command support
- 📱 Mobile companion app
- 🤖 Learning from user patterns
- 🎨 Custom action templates
- 📊 Usage analytics dashboard

## Support

For issues or questions:
- Check this guide first
- Review error messages carefully
- Ensure all dependencies are installed
- Verify GEMINI_API_KEY is configured

---

**BOI** - Intelligent desktop automation, thoughtfully designed with AI understanding and local execution.
