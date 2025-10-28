# 🎮 Self-Operating Computer - Complete Guide

**Autonomous AI Computer Control powered by Gemini Vision**

Inspired by [OthersideAI's self-operating-computer](https://github.com/OthersideAI/self-operating-computer), this feature enables AI to autonomously control your computer by viewing the screen and performing mouse/keyboard actions to accomplish objectives.

---

## 🌟 What It Does

The Self-Operating Computer is an AI agent that:
- **Views your screen** like a human would (takes screenshots)
- **Analyzes what it sees** using Gemini Vision AI
- **Decides the next action** based on the objective and current screen state
- **Executes mouse/keyboard actions** automatically
- **Repeats until the objective is complete** or max iterations reached

---

## 🚀 How to Use

### Option 1: GUI Interface (Recommended)

1. **Open VATSAL GUI App**
   ```bash
   python gui_app.py
   ```

2. **Navigate to the "🎮 Self-Operating" tab**

3. **Enter your objective** in the text box, for example:
   - "Open Google Chrome and search for Python tutorials"
   - "Open Calculator and calculate 25 × 47"
   - "Create a new folder on Desktop named 'AI Projects'"

4. **Choose input mode:**
   - **▶️ Start (Text)**: Uses the objective you typed
   - **🎤 Start (Voice)**: Listen for spoken objective

5. **Watch the AI work!**
   - Real-time output shows what the AI is thinking and doing
   - Status indicator shows current state
   - Screenshots are saved to `screenshots/` folder

6. **Stop if needed**
   - Click **⏹️ Stop** button to interrupt
   - Or move mouse to screen corner (PyAutoGUI failsafe)

### Option 2: CLI Interface

```bash
python self_operating_computer.py
```

Then choose:
1. **Text input** - Type your objective
2. **Voice input** - Speak your objective
3. **Exit**

---

## 💡 Example Objectives

### Simple Tasks (Best for starting)
```
• Open Notepad and write "Hello World"
• Open Calculator and calculate 123 + 456
• Take a screenshot
• Open Desktop folder
```

### Web Navigation
```
• Open Google Chrome and search for Python tutorials
• Go to YouTube and play a video about AI
• Open Gmail in browser
• Search Google for weather in New York
```

### File Operations
```
• Create a new folder on Desktop named "AI Projects"
• Open a text file and write today's date
• Rename a file on Desktop
```

### Multi-Step Tasks
```
• Open Chrome, navigate to GitHub, and take a screenshot
• Search Google for Python tutorials, open first result
• Open Spotify and play jazz music
```

---

## 🎯 How It Works

### The AI Decision Loop

```
1. 📸 Take Screenshot
   └─> AI sees your current screen
   
2. 🧠 Analyze with Gemini Vision
   └─> AI understands what's on screen
       - Buttons, text, windows, applications
       - Current state vs. desired objective
   
3. 💭 Decide Next Action
   └─> AI thinks: "What should I do next?"
       - Move mouse to X, Y
       - Click button
       - Type text
       - Press keyboard key
       - Scroll page
   
4. ⚡ Execute Action
   └─> PyAutoGUI performs the action
   
5. 🔄 Repeat
   └─> Loop until objective complete
       - Max 30 iterations per session
       - AI marks "completed" when done
```

### Available Actions

The AI can perform these actions:

| Action | Description | Parameters |
|--------|-------------|-----------|
| `move_mouse` | Move cursor to position | x, y coordinates |
| `click` | Click mouse button | button (left/right/middle), x, y, clicks |
| `type_text` | Type text at cursor | text string |
| `press_key` | Press keyboard key | key name (enter, tab, etc.) |
| `hotkey` | Press key combination | keys (["ctrl", "c"]) |
| `scroll` | Scroll screen | direction (up/down), amount |
| `wait` | Pause execution | seconds |
| `complete` | Mark as complete | summary message |

---

## 🎤 Voice Input Mode

The voice mode uses speech recognition to capture your objective:

1. Click **🎤 Start (Voice)** button
2. Wait for "Listening..." message
3. Clearly state your objective (10-15 seconds max)
4. AI processes your speech and starts working

**Requirements:**
- Microphone access
- `SpeechRecognition` package (already installed)
- Clear, quiet environment

**Tips:**
- Speak clearly and slowly
- State complete objective in one sentence
- Avoid background noise

---

## 📊 Understanding Output

### Status Indicators

| Status | Meaning | Color |
|--------|---------|-------|
| Ready | Idle, waiting for objective | Green |
| Running... | AI is working | Yellow |
| Listening... | Waiting for voice input | Blue |
| Completed ✅ | Objective achieved | Green |
| Stopped | User interrupted | Red |
| Incomplete | Max iterations reached | Yellow |
| Error | Something went wrong | Red |

### Real-Time Output Tags

- **🔍 Analyzing screen...** - AI is viewing screenshot
- **💭 Thought:** - AI's reasoning about what to do
- **⚡ Action:** - The action AI is taking
- **📊 Progress:** - Completion percentage
- **✅ COMPLETE** - Objective achieved
- **❌ Error** - Something failed
- **⚠️ Warning** - Non-critical issue

---

## 🛡️ Safety Features

### Built-in Protections

1. **PyAutoGUI Failsafe**
   - Move mouse to screen corner to stop immediately
   - Prevents runaway automation

2. **Maximum Iterations**
   - Limited to 30 iterations per session
   - Prevents infinite loops

3. **Screenshot History**
   - All screenshots saved to `screenshots/` folder
   - Review what AI saw and did

4. **User Control**
   - Stop button always available
   - Real-time output shows every action

5. **No Destructive Actions**
   - AI avoids file deletion without context
   - Safe for normal use

### Best Practices

✅ **Do:**
- Start with simple objectives
- Supervise the AI as it works
- Review screenshots after completion
- Use clear, specific objectives

❌ **Don't:**
- Leave it unattended with sensitive data visible
- Give vague or ambiguous objectives
- Expect it to handle very complex multi-step tasks
- Use for critical system operations

---

## 🔧 Configuration

### Adjusting Settings

Edit `self_operating_computer.py` to customize:

```python
# Maximum iterations (default: 30)
self.max_iterations = 30

# PyAutoGUI pause between actions (default: 0.5s)
pyautogui.PAUSE = 0.5

# Gemini model (default: gemini-2.0-flash-exp)
model = 'gemini-2.0-flash-exp'

# Temperature (default: 0.3)
temperature = 0.3
```

### Screenshot Location

Screenshots are saved to: `screenshots/`

Format: `screen_YYYYMMDD_HHMMSS_microseconds.png`

---

## 📖 Comparison with Original

| Feature | OthersideAI Original | VATSAL Edition |
|---------|---------------------|----------------|
| Vision AI | GPT-4o, Claude, Gemini | Gemini Vision |
| Interface | CLI only | GUI + CLI |
| Voice Input | ✅ Supported | ✅ Supported |
| Platform | Mac, Windows, Linux | Mac, Windows, Linux |
| Integration | Standalone | Part of VATSAL ecosystem |
| Real-time Output | Terminal only | Rich GUI display |
| Screenshot Management | Basic | Organized folder view |

---

## ❓ Troubleshooting

### "Gemini API key not found"
**Solution:** Set `GEMINI_API_KEY` in `.env` file

### "Voice input failed"
**Causes:**
- No microphone detected
- Poor audio quality
- Too quiet or too noisy

**Solution:** Check microphone settings, speak clearly

### "Max iterations reached"
**Cause:** Objective too complex or AI got stuck

**Solution:**
- Simplify the objective
- Break into smaller steps
- Check screenshots to see what went wrong

### AI keeps clicking wrong element
**Cause:** Screen resolution or UI element positioning

**Solution:**
- Ensure screen elements are visible and clear
- Try simpler UI navigation
- Check screen resolution matches

### Actions too fast/slow
**Solution:** Adjust `pyautogui.PAUSE` in code:
```python
pyautogui.PAUSE = 1.0  # Slower
pyautogui.PAUSE = 0.2  # Faster
```

---

## 🎓 Advanced Usage

### Session Logs

Save detailed session logs:

```python
# In CLI mode, you'll be asked:
# "Save session log? (y/n)"

# Logs saved as:
# session_log_YYYYMMDD_HHMMSS.json
```

Log contains:
- Objective
- All iterations
- AI thoughts and actions
- Completion status
- Duration

### Programmatic Use

```python
from self_operating_computer import SelfOperatingComputer

# Initialize
computer = SelfOperatingComputer(verbose=True)

# Run with text objective
result = computer.operate("Open Calculator and calculate 5 + 7")

# Run with voice objective
result = computer.operate_with_voice()

# Check result
if result.get("completed"):
    print(f"✅ Success! Took {result['duration_seconds']}s")
    print(f"Iterations: {result['iterations']}")
else:
    print("⚠️ Incomplete")
```

---

## 📚 Resources

### Related Documentation
- [VATSAL AI Guide](VATSAL_GUIDE.md)
- [Comprehensive Desktop Controller](DESKTOP_CONTROL_COMPLETE.md)
- [Virtual Language Model](VIRTUAL_LANGUAGE_MODEL_COMPLETE.md)

### External Links
- [OthersideAI's Original Project](https://github.com/OthersideAI/self-operating-computer)
- [Gemini Vision API](https://ai.google.dev/gemini-api/docs/vision)
- [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/)

---

## 🎉 Tips for Best Results

1. **Start Simple**
   - Test with basic tasks first
   - Learn how AI interprets objectives

2. **Be Specific**
   - "Open Chrome and go to google.com" 
   - Better than: "Search the web"

3. **One Goal at a Time**
   - Complex multi-step tasks may fail
   - Break into smaller objectives

4. **Watch and Learn**
   - Observe how AI navigates
   - Adjust future objectives based on behavior

5. **Review Screenshots**
   - Understand AI's "vision"
   - Debug failed attempts

6. **Provide Context**
   - "Click the blue Submit button on the right"
   - Better than: "Click submit"

---

## 🆚 When to Use Each Automation Type

VATSAL has multiple automation systems. Here's when to use each:

### 🎮 Self-Operating Computer
**Best for:**
- Visual navigation tasks
- Interactive UI exploration
- When you want AI to "figure it out"
- Learning from screen content

### ⚡ VATSAL Automator
**Best for:**
- Quick system commands
- File operations
- System info queries
- Local execution

### 🎯 Comprehensive Controller
**Best for:**
- Complex multi-step workflows
- Planned automation sequences
- When you need progress tracking
- Reproducible tasks

### 🧠 Virtual Language Model
**Best for:**
- Learning your desktop patterns
- Autonomous decision making
- Building desktop knowledge base
- Long-term automation

---

**Ready to let AI operate your computer? Start with something simple like "Open Notepad" and see the magic happen!** ✨

---

*Powered by Google Gemini Vision • Built with ❤️ for VATSAL*
*Based on OthersideAI's self-operating-computer framework*
