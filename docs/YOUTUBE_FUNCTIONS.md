# YouTube Automation Functions

## Overview
The YouTube automation module provides intelligent video search and playback capabilities with multiple methods for maximum reliability.

## Available Functions

### 1. `search_only(query)`
**Purpose**: Search YouTube without auto-playing any videos  
**Use Case**: When you want to browse search results manually  

**Example Commands**:
- "Search YouTube for funny cats"
- "Search for cooking tutorials"

**Python API**:
```python
youtube.search_only("funny cats")
```

---

### 2. `play_first_result(wait_time=3, tab_count=6)`
**Purpose**: Play the first video from the current YouTube search results page  
**Use Case**: After searching manually or with `search_only()`, play the top result  

**Example Commands**:
- "Play the first video"
- "Play first result"
- "Play the top video"

**Python API**:
```python
# First search
youtube.search_only("funny cats")
# Then play first result
youtube.play_first_result()

# Or customize timing
youtube.play_first_result(wait_time=5, tab_count=8)
```

**Parameters**:
- `wait_time`: Seconds to wait for page load (default: 3)
- `tab_count`: Number of Tab key presses to reach first video (default: 6)

---

### 3. `search_and_play(query, wait_time=3, tab_count=6)`
**Purpose**: Search YouTube and immediately play the first result  
**Use Case**: One-step search and play action  

**Example Commands**:
- "Search and play funny cats"
- "Find and play cooking tutorial"

**Python API**:
```python
youtube.search_and_play("funny cats")

# With custom parameters
youtube.search_and_play("tutorial", wait_time=4, tab_count=7)
```

---

### 4. `smart_play_video(query, method="auto")`
**Purpose**: Intelligently play video using 3 different fallback methods  
**Use Case**: Most reliable way to search and auto-play videos  

**Example Commands**:
- "Play video funny cats"
- "Watch cooking tutorial"
- "Show me python videos"
- "Play music"

**Python API**:
```python
# Auto-select best method
youtube.smart_play_video("funny cats")

# Force specific method
youtube.smart_play_video("tutorial", method="method1")
youtube.smart_play_video("music", method="method2")
youtube.smart_play_video("cats", method="method3")
```

**Methods**:
- **Method 1**: Homepage → Search → Navigate → Play (Most reliable)
- **Method 2**: Direct search URL → Navigate → Play (Faster)
- **Method 3**: Search URL → Keyboard shortcuts → Play (Alternative)

---

### 5. `open_video_url(url)`
**Purpose**: Open a specific YouTube video by URL  
**Use Case**: When you have the exact video URL  

**Example Commands**:
- "Open YouTube video https://youtube.com/watch?v=..."
- "Play this video [URL]"

**Python API**:
```python
youtube.open_video_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

---

## Workflow Examples

### Simple Search and Play
```python
# One command does it all
youtube.smart_play_video("funny cats")
```

### Two-Step Approach
```python
# Step 1: Search to see results
youtube.search_only("funny cats")

# Step 2: User decides to play
youtube.play_first_result()
```

### Alternative Search and Play
```python
# Single function for search + play
youtube.search_and_play("cooking tutorial")
```

### Custom Parameters
```python
# Adjust timing for slower internet
youtube.search_and_play("tutorial", wait_time=5, tab_count=8)
```

---

## AI Command Recognition

The AI understands various phrasings:

**Auto-play commands** (uses `play_youtube_video` / `smart_play_video`):
- "play video X"
- "play X"
- "watch X"
- "show me X"
- "play song X"
- "play music"

**Search only** (uses `search_youtube` / `search_only`):
- "search YouTube for X"
- "find videos about X"

**Play first result** (uses `play_first_result`):
- "play the first video"
- "play first result"
- "play the top video"

---

## Technical Details

### Navigation Strategy
All methods use keyboard navigation (Tab keys + Enter) to:
1. Wait for page to load (3-5 seconds)
2. Navigate to first video thumbnail (4-8 Tab presses)
3. Press Enter to play

### Browser Compatibility
Works across all major browsers:
- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- Safari (macOS)

### Reliability Features
- Multiple fallback methods
- Configurable wait times
- Adjustable Tab key counts
- Error handling and reporting

---

## Best Practices

1. **Use `smart_play_video()` by default** - It's the most reliable
2. **Adjust timing on slow connections** - Increase `wait_time` parameter
3. **Fine-tune tab count** - If video doesn't play, adjust `tab_count`
4. **Use specific methods** - If one doesn't work, try another via `method` parameter

---

## Integration Example

```python
from youtube_automation import create_youtube_automation
from gui_automation import GUIAutomation

# Initialize
gui = GUIAutomation()
youtube = create_youtube_automation(gui)

# Use any function
youtube.smart_play_video("funny cats")
youtube.search_and_play("cooking tutorial")
youtube.play_first_result()
```

---

## Troubleshooting

**Video doesn't play?**
- Increase `wait_time` (slower internet needs more time)
- Adjust `tab_count` (different browsers need different counts)
- Try different methods (`method1`, `method2`, `method3`)

**Wrong video plays?**
- First video in search results always plays
- Refine your search query for better results

**Page doesn't load?**
- Check internet connection
- Ensure YouTube isn't blocked
- Try increasing wait times
