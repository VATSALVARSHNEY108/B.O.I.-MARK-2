# 🚀 Macro Recording System - Quick Start

## What Is This?

The VATSAL Macro Recording System lets you **record your mouse and keyboard actions** and **replay them automatically**. Perfect for automating repetitive tasks!

---

## ⚡ 30-Second Quick Start

### 1. Run the Macro Recorder

```bash
python macro_recorder.py
```

### 2. Record Your First Macro

```
Select option: 1
```

- Perform your actions (click, type, move mouse)
- Press **ENTER** when done
- Give it a name: `my_first_macro`

### 3. Play It Back

```
Select option: 4
Macro name: my_first_macro
```

Done! Your actions replay automatically! 🎉

---

## 🎯 Common Use Cases

### Automate Form Filling

1. Record: Click fields → Type data → Tab between fields
2. Replay: `macro_recorder.play_macro("form_filler", repeat=100)`

### Automated Testing

1. Record: Your test steps (login → navigate → verify)
2. Replay: Run 50 tests at 2x speed

### Repetitive Clicking

```python
from macro_recorder import macro_templates

# Click same spot 100 times, 1 second apart
positions = [(500, 500)] * 100
events = macro_templates.generate_click_sequence(positions, delay=1.0)
macro_recorder.events = events
macro_recorder.play_macro()
```

---

## 📋 Pre-Built Templates

### Multi-Click Sequence

```python
from macro_recorder import macro_templates, macro_recorder

positions = [(100, 200), (300, 400), (500, 600)]
events = macro_templates.generate_click_sequence(positions, delay=1.0)
macro_recorder.events = events
macro_recorder.play_macro()
```

### Form Auto-Fill

```python
fields = [
    (300, 200, "John Doe", True),       # x, y, text, tab_after
    (300, 250, "john@email.com", True),
    (300, 300, "1234567890", False)
]
events = macro_templates.generate_form_fill(fields)
macro_recorder.events = events
macro_recorder.play_macro()
```

### Screenshot Sequence

```python
# Take 10 screenshots, 3 seconds apart
events = macro_templates.generate_screenshot_sequence(count=10, interval=3.0)
macro_recorder.events = events
macro_recorder.play_macro()
```

### Window Switcher

```python
# Switch between 5 windows using Alt+Tab
events = macro_templates.generate_window_switch(switches=5)
macro_recorder.events = events
macro_recorder.play_macro()
```

---

## 🔧 Advanced Playback

### Repeat Multiple Times

```python
macro_recorder.play_macro("my_macro", repeat=10)
```

### Speed Control

```python
# 2x faster
macro_recorder.play_macro("my_macro", speed=2.0)

# Half speed (more reliable)
macro_recorder.play_macro("my_macro", speed=0.5)
```

### Completion Callback

```python
def done(msg):
    print(f"Finished: {msg}")

macro_recorder.play_macro("my_macro", callback=done)
```

---

## 💾 Managing Macros

### List All Macros

```bash
python macro_recorder.py
Select option: 3
```

### Delete a Macro

```python
from macro_recorder import macro_recorder

macro_recorder.delete_macro("old_macro")
```

### Load Macro Data

```python
events = macro_recorder.load_macro("my_macro")
print(f"This macro has {len(events)} events")
```

---

## ⚙️ Pro Tips

1. **Record Slowly** - You can speed up playback later
2. **Use Keyboard Shortcuts** - More reliable than mouse clicks
3. **Test with Repeat=1** - Always test once before bulk repeats
4. **Same Starting Position** - Start playback from same screen/app
5. **Slow Down if Fails** - Use `speed=0.5` for reliability

---

## 🐛 Troubleshooting

### "pynput not available"

```bash
pip install pynput
```

### Macro Doesn't Work

1. Check you're on the same screen
2. Try slower speed: `speed=0.5`
3. Re-record from same starting position

### Clicks Miss Targets

- Screen resolution changed?
- Windows in different positions?
- Use keyboard shortcuts instead of mouse

---

## 📚 Full Documentation

See **MACRO_SYSTEM_GUIDE.md** for complete documentation including:
- Full API reference
- Security best practices
- File format specifications
- Advanced examples
- Integration guides

---

## ✅ Quick Reference

| Task | Command |
|------|---------|
| Run CLI | `python macro_recorder.py` |
| Record | Option 1 in CLI |
| Play last | Option 2 in CLI |
| List macros | Option 3 in CLI |
| Play saved | Option 4 in CLI |
| Repeat 10x | `play_macro(name, repeat=10)` |
| 2x speed | `play_macro(name, speed=2.0)` |
| Slow motion | `play_macro(name, speed=0.5)` |
| Delete | `delete_macro(name)` |

---

**Happy Automating! 🎬**

For detailed documentation, see `MACRO_SYSTEM_GUIDE.md`
