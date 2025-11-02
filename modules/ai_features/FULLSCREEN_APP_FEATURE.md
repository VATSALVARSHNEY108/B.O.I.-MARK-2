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

### Use Case 3: Workflow Automation
```python
# Analyze and auto-open as part of workflow
result = detect_app_and_open_fullscreen()
# Result includes app name, detection status, and launch result
```

## Demo

Run the demo file to see all features in action:
```bash
python demo_fullscreen_app_feature.py 1  # Open specific app
python demo_fullscreen_app_feature.py 2  # Auto-detect and open
python demo_fullscreen_app_feature.py 3  # Manual detection
python demo_fullscreen_app_feature.py 4  # List supported apps
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
