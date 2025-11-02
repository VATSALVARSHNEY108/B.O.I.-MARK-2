# 🤖 Smart App Automation with AI Screenshot Analysis

## Overview
Advanced automation system that opens applications in fullscreen mode and uses AI to analyze what's happening on screen.

## Features

### 📱 Fullscreen Automation (`modules/automation/fullscreen_automation.py`)
- Open any application in fullscreen mode
- Cross-platform support (Windows, macOS, Linux)
- Automated keyboard and mouse control
- Screenshot capture
- Window management

### 🧠 AI Screenshot Analysis (`modules/ai_features/screenshot_analysis.py`)
- Analyze screenshots with Google Gemini AI Vision
- Detect errors and bugs
- Analyze code on screen
- UI/UX improvement suggestions
- Design analysis
- Text extraction (OCR)

### 🎯 Smart App Automation (`modules/automation/smart_app_automation.py`)
Combines both features for intelligent app automation:
- Opens apps in fullscreen
- Captures screenshots
- Analyzes with AI
- Performs automated actions
- Continuous monitoring mode

## Quick Start

### 1. Basic Usage - Analyze Any App

```bash
python modules/automation/smart_app_automation.py chrome
```

### 2. Analyze with Specific Focus

```bash
# Check for errors
python modules/automation/smart_app_automation.py vscode errors

# Analyze code
python modules/automation/smart_app_automation.py vscode code

# Get improvement suggestions
python modules/automation/smart_app_automation.py chrome improvements

# Design analysis
python modules/automation/smart_app_automation.py figma design
```

### 3. Python API

```python
from modules.automation.smart_app_automation import SmartAppAutomation

# Initialize
automation = SmartAppAutomation()

# Open app and analyze
result = automation.automate_app("notepad", analysis_type="general")
print(result['analysis'])

# Perform automated actions
actions = [
    {"type": "type", "text": "Hello World!"},
    {"type": "key", "key": "enter"},
    {"type": "screenshot", "filename": "result.png"}
]
result = automation.automate_with_actions("notepad", actions)

# Continuous monitoring
automation.continuous_monitoring("chrome", interval=10, duration=60)
```

## Available Analysis Types

| Type | Description |
|------|-------------|
| `general` | Overall analysis of the application |
| `errors` | Detect errors, warnings, and bugs |
| `code` | Analyze code quality and suggest improvements |
| `design` | UI/UX and design analysis |
| `improvements` | Specific improvement suggestions |
| `tips` | Quick actionable tips |

## Action Types

When using `automate_with_actions()`:

```python
# Type text
{"type": "type", "text": "Hello!"}

# Press a key
{"type": "key", "key": "enter"}

# Hotkey combination
{"type": "hotkey", "keys": ["ctrl", "s"]}

# Click at coordinates
{"type": "click", "x": 100, "y": 200}

# Wait
{"type": "wait", "seconds": 2}

# Screenshot
{"type": "screenshot", "filename": "capture.png"}
```

## Examples

### Example 1: Open Browser and Check for Errors
```python
from modules.automation.smart_app_automation import SmartAppAutomation

automation = SmartAppAutomation()
result = automation.automate_app("chrome", analysis_type="errors")

if result['success']:
    print(result['analysis'])
```

### Example 2: Automated Note Taking
```python
automation = SmartAppAutomation()

actions = [
    {"type": "type", "text": "Meeting Notes - 2024"},
    {"type": "key", "key": "enter"},
    {"type": "key", "key": "enter"},
    {"type": "type", "text": "- AI automation working"},
    {"type": "key", "key": "enter"},
    {"type": "type", "text": "- Screenshot analysis complete"},
    {"type": "wait", "seconds": 1},
    {"type": "screenshot", "filename": "notes.png"}
]

result = automation.automate_with_actions("notepad", actions)
```

### Example 3: Monitor Development Environment
```python
automation = SmartAppAutomation()

# Monitor VS Code for 5 minutes, checking every 30 seconds
result = automation.continuous_monitoring(
    app_name="code",
    interval=30,
    duration=300
)

print(f"Captured {result['count']} screenshots")
```

## Fullscreen Automation Features

```python
from modules.automation.fullscreen_automation import FullscreenAutomation

fs = FullscreenAutomation()

# Open app in fullscreen
fs.open_app_fullscreen("chrome")

# Maximize window
fs.maximize_window()

# Type text
fs.type_text("Hello World")

# Press keys
fs.press_key("enter")
fs.hotkey("ctrl", "s")  # Save

# Click
fs.click_at(500, 300)

# Screenshot
fs.take_screenshot("capture.png")

# Exit fullscreen
fs.exit_fullscreen()
```

## Screenshot Analysis Features

```python
from modules.ai_features.screenshot_analysis import ScreenshotAnalyzer

analyzer = ScreenshotAnalyzer()

# General analysis
result = analyzer.analyze("screenshot.png")

# Find errors
errors = analyzer.find_errors("screenshot.png")

# Analyze code
code_analysis = analyzer.analyze_code("screenshot.png")

# Get improvement suggestions
suggestions = analyzer.suggest_improvements("screenshot.png")

# Quick tips
tips = analyzer.get_quick_tips("screenshot.png")
```

## Requirements

- Python 3.8+
- PyAutoGUI (for automation)
- Google Gemini API key (for AI analysis)
- Cross-platform: Works on Windows, macOS, Linux

## Setup

1. Install dependencies:
```bash
pip install pyautogui google-genai
```

2. Set Gemini API key:
```bash
# In Replit Secrets or environment
export GEMINI_API_KEY="your_api_key_here"
```

3. Run automation:
```bash
python modules/automation/smart_app_automation.py <app_name>
```

## Platform-Specific Notes

### Windows
- Use application names like `notepad`, `chrome`, `code`
- F11 for fullscreen in most apps
- Win+Up to maximize

### macOS
- Use application names like `TextEdit`, `Safari`, `Visual Studio Code`
- Ctrl+Cmd+F for fullscreen
- May need accessibility permissions

### Linux
- Depends on your desktop environment
- F11 typically works for fullscreen
- Super+Up for maximize in most DEs

## Tips

1. **Wait for apps to load**: Always add a delay after opening apps
2. **Screenshot timing**: Take screenshots after UI updates complete
3. **Error handling**: Check result['success'] before proceeding
4. **Coordinates**: Use `pyautogui.position()` to get mouse coordinates
5. **API key**: Keep your Gemini API key secure in environment variables

## Troubleshooting

**App doesn't go fullscreen:**
- Try `maximize_window()` instead
- Some apps may not support F11
- Check app-specific fullscreen shortcuts

**Automation not working:**
- Verify PyAutoGUI is installed
- Check if running in a GUI environment
- May not work in headless/cloud environments

**AI analysis fails:**
- Verify GEMINI_API_KEY is set
- Check internet connection
- Ensure screenshot file exists

## Advanced Use Cases

- **Automated Testing**: Open app, perform actions, verify results
- **Productivity Monitoring**: Track application usage and activity
- **Code Review**: Analyze code screenshots for improvements
- **UI Testing**: Check for design inconsistencies
- **Documentation**: Auto-capture and annotate screenshots
- **Accessibility Audits**: Analyze UI for accessibility issues

## Contributing

Feel free to extend with:
- More analysis types
- Additional automation actions
- Platform-specific improvements
- Custom workflows
