# 🎬 Automation Recording & Macro System - User Guide

## Overview

VATSAL's Macro Recording System lets you **record your mouse and keyboard actions** and **replay them automatically**. It's perfect for repetitive tasks, testing, data entry, and automation workflows!

### ✨ Key Features

1. **🔴 Action Recording** - Capture every mouse click, movement, and keyboard press
2. **▶️ Accurate Playback** - Replay with precise timing and speed control  
3. **💾 Save & Manage** - Store macros for later use
4. **🔁 Loop Support** - Repeat actions multiple times automatically
5. **📋 Pre-built Templates** - Ready-made macros for common tasks
6. **⚡ Speed Control** - Play faster (2x) or slower (0.5x) as needed

---

## 🚀 Quick Start Guide

### Installation Check

The macro system requires `pynput` library (already installed):
```bash
pip install pynput
```

### Basic Usage (Command Line)

```bash
# Run the macro recorder
python macro_recorder.py
```

You'll see:
```
🎬 VATSAL Macro Recorder
==================================================
pynput available: True
PyAutoGUI available: True

Commands:
  1. Record macro
  2. Play last recording
  3. List macros
  4. Play saved macro
  5. Exit
```

---

## 📝 Recording Your First Macro

### Step-by-Step:

1. **Start the macro recorder:**
   ```bash
   python macro_recorder.py
   ```

2. **Choose option 1** (Record macro)

3. **Perform your actions:**
   - Click buttons
   - Type text
   - Move mouse
   - Scroll
   - Press keyboard shortcuts
   
4. **Press ENTER** when done

5. **Give it a name:**
   ```
   Save as (leave empty to skip): my_first_macro
   ```

6. **Done!** Your macro is saved in the `macros/` folder

---

## ▶️ Playing Back Macros

### Play the Last Recording:

```
Select option: 2
```

The macro will replay exactly as you recorded it!

### Play a Saved Macro:

```
Select option: 4
Macro name: my_first_macro
```

### Advanced Playback (Python):

```python
from macro_recorder import macro_recorder

# Play once at normal speed
macro_recorder.play_macro(macro_name="my_first_macro")

# Play 5 times
macro_recorder.play_macro(macro_name="my_first_macro", repeat=5)

# Play at 2x speed
macro_recorder.play_macro(macro_name="my_first_macro", speed=2.0)

# Play at half speed
macro_recorder.play_macro(macro_name="my_first_macro", speed=0.5)
```

---

## 💾 Managing Macros

### List All Saved Macros:

```
Select option: 3
```

Output:
```
Saved Macros:
  - my_first_macro: 45 events, 12.3s
  - form_filler: 120 events, 8.5s
  - test_sequence: 30 events, 5.0s
```

### Delete a Macro:

```python
from macro_recorder import macro_recorder

macro_recorder.delete_macro("my_first_macro")
# Output: ✅ Deleted macro: my_first_macro
```

### Load Macro Data:

```python
from macro_recorder import macro_recorder

# Load macro events
events = macro_recorder.load_macro("my_first_macro")
print(f"Loaded {len(events)} events")
```

---

## 🎯 Pre-Built Templates

VATSAL includes ready-made templates for common automation tasks:

### 1. Multi-Click Sequence

Automatically click multiple positions:

```python
from macro_recorder import macro_templates

# Create click sequence macro
positions = [(100, 200), (300, 400), (500, 600)]
events = macro_templates.generate_click_sequence(positions, delay=1.0)

# Save and play
macro_recorder.events = events
macro_recorder.save_macro("multi_click")
macro_recorder.play_macro(macro_name="multi_click")
```

### 2. Form Auto-Fill

Fill multiple form fields with text:

```python
from macro_recorder import macro_templates

# Define fields: (x, y, text, tab_after)
fields = [
    (300, 200, "John Doe", True),       # Name field
    (300, 250, "john@example.com", True),  # Email field
    (300, 300, "1234567890", False)     # Phone field
```

---

## 🔧 Advanced Usage

### Recording with Custom Callback:

```python
from macro_recorder import macro_recorder

def on_event(event):
    print(f"Recorded: {event['type']} at {event['time']:.2f}s")

macro_recorder.start_recording(callback=on_event)
input("Press ENTER to stop...")
macro_recorder.stop_recording("with_callbacks")
```

### Playing with Completion Callback:

```python
def on_complete(message):
    print(f"Playback finished: {message}")

macro_recorder.play_macro(
    macro_name="my_macro",
    repeat=3,
    speed=1.5,
    callback=on_complete
)
```

### Stopping Playback Mid-Execution:

```python
# Start playback in background
macro_recorder.play_macro(macro_name="long_macro")

# Stop it anytime
macro_recorder.stop_playback()
# Output: ⏹️ Playback stopped
```

---

## 📂 Macro File Format

Macros are stored as JSON files in the `macros/` folder:

```json
{
  "name": "my_first_macro",
  "description": "Example macro",
  "created": "2025-10-30T15:30:00",
  "event_count": 45,
  "duration": 12.3,
  "events": [
    {
      "type": "move",
      "time": 0.123,
      "x": 500,
      "y": 300
    },
    {
      "type": "click",
      "time": 0.543,
      "x": 500,
      "y": 300,
      "button": "Button.left",
      "pressed": true
    },
    {
      "type": "key_press",
      "time": 1.234,
      "key": "'h'"
    }
  ]
}
```

### Event Types:

- **move**: Mouse movement (`x`, `y`)
- **click**: Mouse click (`x`, `y`, `button`, `pressed`)
- **scroll**: Mouse scroll (`x`, `y`, `dx`, `dy`)
- **key_press**: Keyboard key press (`key`)
- **key_release**: Keyboard key release (`key`)

---

## 🎯 Common Use Cases

### 1. Form Data Entry

**Record once:**
1. Click first field
2. Type data
3. Press Tab
4. Repeat for all fields

**Replay 100x:**
```python
macro_recorder.play_macro("form_entry", repeat=100)
```

### 2. Automated Testing

**Record test steps:**
1. Click "Login"
2. Enter username
3. Enter password
4. Click "Submit"
5. Verify success

**Run tests:**
```python
macro_recorder.play_macro("login_test", repeat=50, speed=2.0)
```

### 3. Repetitive Clicks

**For games/automation:**
```python
# Click every second at same position
positions = [(500, 500)] * 60  # 60 clicks
events = macro_templates.generate_click_sequence(positions, delay=1.0)
macro_recorder.events = events
macro_recorder.play_macro()
```

### 4. Multi-Application Workflow

**Record:**
1. Open Excel
2. Copy data
3. Switch to browser
4. Paste data
5. Submit form

**Automate:**
```python
macro_recorder.play_macro("data_transfer", repeat=10)
```

---

## ⚙️ Configuration & Tips

### Recording Tips:

1. **Go Slow**: Record at a comfortable pace - you can speed up playback later
2. **Test First**: Do a quick test run before recording the full macro
3. **Minimize Moves**: Excessive mouse movements make large files - click precisely
4. **Use Keyboard**: Keyboard shortcuts (Ctrl+C, Alt+Tab) work better than mouse
5. **Plan Ahead**: Think through your steps before recording

### Playback Tips:

1. **Start Position**: Make sure you're at the same screen/app when playing back
2. **Screen Resolution**: Macros recorded at one resolution may not work on another
3. **Speed Adjust**: If actions fail, try slower speed (0.5x or 0.7x)
4. **Test with Repeat=1**: Always test once before doing large repeats
5. **Have a Kill Switch**: Know how to stop - use `macro_recorder.stop_playback()`

### Performance:

- **Mouse Movements**: Recorded every 100ms to reduce file size
- **File Size**: Typical 1-minute macro = ~50KB
- **Memory**: Minimal - events stored as simple dictionaries
- **CPU**: Low impact during recording, moderate during high-speed playback

---

## 🐛 Troubleshooting

### "pynput not available"

```bash
# Install pynput
pip install pynput

# On Linux, you may need:
sudo apt-get install python3-xlib
```

### "PyAutoGUI not available"

```bash
pip install pyautogui
```

### Macro Doesn't Replay Correctly

1. **Check screen resolution** - Did you change resolution?
2. **Slow down playback** - Try `speed=0.5`
3. **Re-record** - Start from the same initial state
4. **Add delays** - Manually edit JSON to add pauses

### Clicks Miss Targets

- **Resolution mismatch**: Absolute positions don't translate across resolutions
- **Window position changed**: Ensure windows are in same position
- **Use keyboard instead**: Tab + Enter is more reliable than clicking

### Recording Stops Immediately

- **Permission issue**: On macOS, grant Accessibility permissions
- **Library issue**: Check that pynput installed correctly

---

## 🔐 Security & Privacy

### Important Notes:

⚠️ **Macros can record passwords and sensitive data!**

- Never share macros that contain sensitive information
- Review macro JSON files before sharing
- Consider using templates instead of recording for sensitive workflows
- Macros execute with your user permissions - be careful what you automate

### Best Practices:

✅ Use macros for safe, repetitive tasks  
✅ Test in isolated environment first  
✅ Review recorded data before saving  
❌ Don't record login credentials  
❌ Don't run untrusted macros  
❌ Don't use for financial transactions without review  

---

## 🚀 Integration with VATSAL

### Using in VATSAL Commands:

```python
from macro_recorder import macro_recorder

# In your VATSAL integration
def execute_macro_command(macro_name):
    result = macro_recorder.play_macro(macro_name=macro_name)
    return result
```

### Voice Command Integration:

```python
# Example VATSAL voice command
"VATSAL, play the form filler macro 5 times"
# → macro_recorder.play_macro("form_filler", repeat=5)
```

---

## 📚 API Reference

### MacroRecorder Class

```python
from macro_recorder import MacroRecorder

recorder = MacroRecorder()
```

#### Methods:

- `start_recording(callback=None)` - Start recording user actions
- `stop_recording(name=None)` - Stop recording and optionally save
- `play_macro(macro_name, repeat=1, speed=1.0, callback=None)` - Play a macro
- `stop_playback()` - Stop current playback
- `save_macro(name, description="")` - Save current recording
- `load_macro(name)` - Load macro events from file
- `list_macros()` - List all saved macros
- `delete_macro(name)` - Delete a saved macro

### MacroTemplates Class

```python
from macro_recorder import MacroTemplates

templates = MacroTemplates()
```

#### Methods:

- `get_templates()` - Get all available templates
- `generate_click_sequence(positions, delay=1.0)` - Multi-click macro
- `generate_form_fill(fields)` - Form filling macro
- `generate_screenshot_sequence(count=5, interval=2.0)` - Screenshot macro
- `generate_window_switch(switches=3)` - Alt+Tab macro

---

## 🎓 Examples

### Example 1: Automated Screenshot Taker

```python
from macro_recorder import macro_templates, macro_recorder

# Create macro to take 10 screenshots, 3 seconds apart
events = macro_templates.generate_screenshot_sequence(count=10, interval=3.0)
macro_recorder.events = events
macro_recorder.save_macro("auto_screenshots", "Takes 10 screenshots every 3 seconds")

# Run it
macro_recorder.play_macro("auto_screenshots")
```

### Example 2: Browser Form Filler

```python
# Record manually:
# 1. python macro_recorder.py
# 2. Select "1" to record
# 3. Navigate to form
# 4. Fill all fields
# 5. Press ENTER to stop
# 6. Save as "browser_form"

# Then replay:
macro_recorder.play_macro("browser_form", repeat=20, speed=1.5)
```

### Example 3: Custom Window Workflow

```python
from macro_recorder import macro_templates

# Switch between 5 windows
events = macro_templates.generate_window_switch(switches=5)
macro_recorder.events = events
macro_recorder.play_macro()
```

---

## 💡 Pro Tips

1. **Combine with AI**: Use VATSAL's AI to generate custom templates
2. **Error Recovery**: Add `try/except` blocks when integrating
3. **Batch Processing**: Use repeat parameter instead of separate macros
4. **Modular Macros**: Record small reusable pieces, combine them programmatically
5. **Version Control**: Keep macro JSON files in git for team sharing

---

## 🆘 Support & Resources

- **Documentation**: This file (`MACRO_SYSTEM_GUIDE.md`)
- **Source Code**: `macro_recorder.py`
- **Examples**: See "Examples" section above
- **Templates**: See "Pre-Built Templates" section

---

## ✅ Feature Summary

| Feature | Status | Notes |
|---------|--------|-------|
| Mouse Click Recording | ✅ | Left, right, middle buttons |
| Mouse Movement Recording | ✅ | Optimized (100ms intervals) |
| Mouse Scroll Recording | ✅ | Horizontal and vertical |
| Keyboard Recording | ✅ | All keys, special keys, combos |
| Accurate Timing | ✅ | Millisecond precision |
| Loop Playback | ✅ | Repeat 1-∞ times |
| Speed Control | ✅ | 0.1x to 10x speed |
| Save/Load Macros | ✅ | JSON format |
| Macro Management | ✅ | List, delete, organize |
| Pre-built Templates | ✅ | 4 ready templates |
| Stop/Cancel | ✅ | Stop recording or playback anytime |
| Cross-Platform | ✅ | Windows, macOS, Linux |
| GUI Integration | 🚧 | Coming soon |
| Visual Workflow Builder | 🚧 | Planned feature |

---

**Happy Automating! 🎬**

For questions or issues, check the source code or create an issue in the project repository.
