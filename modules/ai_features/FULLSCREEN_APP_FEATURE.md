# AI Fullscreen App Feature

## Overview
The Screenshot Analysis module now includes AI-powered fullscreen app functionality that can:
- **Take screenshots** of the current screen
- **Detect applications** using AI vision
- **Open apps in fullscreen mode** automatically or manually

## Features

### 1. Auto-Detect and Open
Automatically takes a screenshot, detects the app, and opens it in fullscreen:
```python
from modules.ai_features.screenshot_analysis import detect_app_and_open_fullscreen

# Auto-detect from current screen
result = detect_app_and_open_fullscreen()
print(result)

# Or use an existing screenshot
result = detect_app_and_open_fullscreen("path/to/screenshot.png")
print(result)
```

### 2. Open Specific App
Open any supported app directly in fullscreen mode:
```python
from modules.ai_features.screenshot_analysis import open_app_in_fullscreen

# Open Chrome in fullscreen
result = open_app_in_fullscreen("chrome")
print(result)

# Open without forcing fullscreen
result = open_app_in_fullscreen("notepad", force_fullscreen=False)
print(result)
```

### 3. Manual Control
Fine-grained control over the process:
```python
from modules.ai_features.screenshot_analysis import ScreenshotAnalyzer

analyzer = ScreenshotAnalyzer()

# Take a screenshot
screenshot_path = analyzer.take_screenshot("screenshots/current.png")

# Detect which app is visible
app_info = analyzer.detect_app_from_screenshot(screenshot_path)
print(f"App: {app_info['app_name']}")
print(f"Fullscreen: {app_info['is_fullscreen']}")

# Open the detected app
result = analyzer.open_app_fullscreen(app_info['app_name'])
print(result)
```

## Supported Applications

### Browsers
- Chrome (`chrome`)
- Firefox (`firefox`)
- Microsoft Edge (`edge`)
- Safari (`safari`) - macOS only

### Editors
- VS Code (`code`)
- Notepad/TextEdit (`notepad`)

### Media
- VLC Media Player (`vlc`)
- Spotify (`spotify`)

### Office
- Microsoft Word (`word`)
- Microsoft Excel (`excel`)
- Microsoft PowerPoint (`powerpoint`)

### Utilities
- Calculator (`calculator`)

## How It Works

1. **Screenshot Capture**: Uses PyAutoGUI to capture the current screen
2. **AI Analysis**: Sends the screenshot to Google Gemini AI for analysis
3. **App Detection**: AI identifies the application name and type
4. **App Launch**: Opens the application using platform-specific commands
5. **Fullscreen Mode**: Presses F11 (or Cmd+Ctrl+F on macOS) to enable fullscreen

## Cross-Platform Support

The feature works across:
- **Windows**: Uses `start` commands and F11 for fullscreen
- **Linux**: Uses direct app commands and F11 for fullscreen
- **macOS**: Uses `open -a` commands and Cmd+Ctrl+F for fullscreen

## Command Line Usage

Run the module directly from command line:

```bash
# Analyze a screenshot
python modules/ai_features/screenshot_analysis.py analyze screenshot.png

# Detect app from screenshot
python modules/ai_features/screenshot_analysis.py detect-app screenshot.png

# Open an app in fullscreen
python modules/ai_features/screenshot_analysis.py open chrome

# Auto-detect and open
python modules/ai_features/screenshot_analysis.py auto-open

# Take a screenshot
python modules/ai_features/screenshot_analysis.py screenshot custom_path.png
```

## Requirements

- `pyautogui` - for screenshot capture and keyboard control
- `google-genai` - for AI-powered app detection
- `GEMINI_API_KEY` - environment variable with your Gemini API key

## Control Apps Before Automation

### NEW: Ensure Apps Are Fullscreen Before Controlling Them

When automating apps like Notepad, browsers, or YouTube, you should **first ensure they're open in fullscreen** before sending commands:

#### Control Notepad in Fullscreen
```python
from modules.ai_features.screenshot_analysis import control_notepad_fullscreen
import pyautogui

# First, open Notepad in fullscreen
control_notepad_fullscreen()

# Now control it - it's already fullscreen!
pyautogui.write("This text appears in fullscreen Notepad")
pyautogui.hotkey('ctrl', 's')  # Save
```

#### Control Browser in Fullscreen
```python
from modules.ai_features.screenshot_analysis import control_browser_fullscreen

# Open Chrome in fullscreen
control_browser_fullscreen("chrome")

# Now control the browser with selenium/pyautogui
# Browser is already fullscreen and ready!
```

#### Control YouTube in Fullscreen
```python
from modules.ai_features.screenshot_analysis import control_youtube_fullscreen

# Open YouTube in fullscreen browser
control_youtube_fullscreen("chrome", "https://youtube.com/watch?v=dQw4w9WgXcQ")

# Now control playback, search, etc.
# YouTube is already open in fullscreen!
```

#### Control Any App in Fullscreen
```python
from modules.ai_features.screenshot_analysis import ensure_app_fullscreen

# Open Calculator in fullscreen
ensure_app_fullscreen("calculator")

# Open VS Code in fullscreen
ensure_app_fullscreen("code")

# Open Spotify in fullscreen
ensure_app_fullscreen("spotify")

# Now control any of these apps - they're all fullscreen!
```

## Example Use Cases

### Use Case 1: Quick App Launcher
```python
# Open your favorite apps quickly in fullscreen
open_app_in_fullscreen("spotify")
open_app_in_fullscreen("chrome")
```

### Use Case 2: Smart Screen Management
```python
# Detect what's on screen and maximize it
analyzer = ScreenshotAnalyzer()
screenshot = analyzer.take_screenshot()
app_info = analyzer.detect_app_from_screenshot(screenshot)

if not app_info['is_fullscreen']:
    analyzer.open_app_fullscreen(app_info['app_name'])
```

### Use Case 3: Workflow Automation with Fullscreen Control
```python
from modules.ai_features.screenshot_analysis import control_notepad_fullscreen
import pyautogui
import time

# 1. Ensure Notepad is fullscreen
control_notepad_fullscreen()
time.sleep(1)

# 2. Write automated content
pyautogui.write("Meeting Notes - " + str(datetime.now()))
pyautogui.press('enter')
pyautogui.write("- Discussed project timeline")
pyautogui.press('enter')
pyautogui.write("- Reviewed budget")

# 3. Save the file
pyautogui.hotkey('ctrl', 's')
```

### Use Case 4: YouTube Automation
```python
from modules.ai_features.screenshot_analysis import control_youtube_fullscreen
import time
import pyautogui

# Open YouTube in fullscreen
control_youtube_fullscreen("chrome", "https://youtube.com")
time.sleep(3)

# Search for a video
pyautogui.click(x=500, y=100)  # Click search box
pyautogui.write("Python tutorial")
pyautogui.press('enter')
```

## Demo

### Demo 1: Fullscreen App Features
Run the demo file to see all features in action:
```bash
python demo_fullscreen_app_feature.py 1  # Open specific app
python demo_fullscreen_app_feature.py 2  # Auto-detect and open
python demo_fullscreen_app_feature.py 3  # Manual detection
python demo_fullscreen_app_feature.py 4  # List supported apps
```

### Demo 2: Control Apps in Fullscreen
Run the control demo to see how to control apps:
```bash
python demo_control_apps_fullscreen.py 1         # Control Notepad
python demo_control_apps_fullscreen.py 2         # Control Browser
python demo_control_apps_fullscreen.py 3         # Open YouTube
python demo_control_apps_fullscreen.py 4         # Control Any App
python demo_control_apps_fullscreen.py 5         # Complete Workflow
python demo_control_apps_fullscreen.py examples  # Show code examples
```

## Error Handling

The feature includes comprehensive error handling:
- Missing GEMINI_API_KEY → Returns error message
- Unknown app → Lists supported apps
- Screenshot failure → Returns error with details
- App launch failure → Returns platform-specific error

## Future Enhancements

Potential improvements:
- Support for more applications
- Window positioning and sizing controls
- Multi-monitor support
- Custom keyboard shortcuts for fullscreen
- App-specific fullscreen commands
