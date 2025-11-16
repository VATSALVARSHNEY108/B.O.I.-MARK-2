# 🎵 Spotify in Your GUI App - Complete Guide

## ⚡ What Works NOW (Desktop Mode)

Your GUI app currently uses **keyboard shortcuts** to control Spotify.

### ✅ Available Commands RIGHT NOW:
```
Play Spotify          → Toggles play/pause
Pause music          → Toggles play/pause
Next song            → Skip to next
Previous song        → Go back
```

**These work immediately** - no setup needed! Just type them in your GUI app.

---

## 🚀 Upgrade to Full API Control

To use **ALL** the commands (search, playlists, volume, etc.), you need to switch to API mode:

### Step 1: Update Your GUI App Import

Find this in your `modules/core/command_executor.py`:
```python
from modules.utilities.spotify_desktop_automation import create_spotify_desktop_automation
self.spotify = create_spotify_desktop_automation()
```

**Change to:**
```python
from modules.utilities.spotify_local import SpotifyLocal
self.spotify = SpotifyLocal()
self.spotify.authenticate()  # One-time authentication
```

### Step 2: After This Change, ALL Commands Work! ✨

Once upgraded, you can use:

#### 🎵 Play Specific Songs
```
Play Bohemian Rhapsody on Spotify
Play Shape of You by Ed Sheeran
Play Despacito by Luis Fonsi on Spotify
```

#### 🔊 Volume Control
```
Set volume to 50
Volume 80
Turn volume down to 30
```

#### ℹ️ Track Info
```
What's playing?
Current song
Show current track
```

#### 🔍 Search
```
Search Spotify for rock music
Find Taylor Swift songs
Search for workout music
```

#### 📚 Playlists
```
Show my playlists
List my Spotify playlists
Display my playlists
```

#### 🔀 Advanced Controls
```
Shuffle on/off
Repeat on/off
Next song
Previous song
Pause/Play
```

---

## 📝 Quick Code Update

### Option A: Add Both (Recommended)

Keep desktop mode as fallback, add API mode:

```python
# In command_executor.py
from modules.utilities.spotify_desktop_automation import create_spotify_desktop_automation
from modules.utilities.spotify_local import SpotifyLocal

class CommandExecutor:
    def __init__(self):
        # Try API mode first
        try:
            self.spotify = SpotifyLocal()
            if os.getenv('SPOTIFY_CLIENT_ID'):
                self.spotify_mode = "api"
            else:
                self.spotify_mode = "desktop"
                self.spotify = create_spotify_desktop_automation()
        except:
            # Fallback to desktop mode
            self.spotify_mode = "desktop"
            self.spotify = create_spotify_desktop_automation()
```

### Option B: API Only (Full Features)

Replace completely:

```python
# In command_executor.py
from modules.utilities.spotify_local import SpotifyLocal

class CommandExecutor:
    def __init__(self):
        self.spotify = SpotifyLocal()
        # Authenticate on first use
        if os.getenv('SPOTIFY_CLIENT_ID'):
            self.spotify.authenticate()
```

---

## 🎯 Full Command List for GUI App

Once upgraded to API mode, copy-paste any of these:

### Playback
- `Play Spotify`
- `Pause music`
- `Next song`
- `Previous song`

### Play Songs
- `Play [song name] on Spotify`
- `Play [song] by [artist]`

### Volume
- `Set volume to [0-100]`

### Information
- `What's playing?`
- `Show my playlists`

### Search
- `Search Spotify for [query]`

### Modes
- `Shuffle on/off`
- `Repeat on/off`

---

## 📖 Complete Prompt List

See **`docs/SPOTIFY_PROMPTS_FOR_GUI.txt`** for full list with examples!

---

## ⚙️ Current Status

**Your Setup:**
- ✅ Spotify Client ID - Set
- ✅ Spotify Client Secret - Set
- ✅ Redirect URI - `https://open.spotify.com/`
- ⚠️  GUI App - Currently using **desktop mode** (limited features)

**To unlock all features:**
1. Update the import in `command_executor.py`
2. Restart your GUI app
3. Use any command from the list!

---

## 🐛 Troubleshooting

**"Desktop mode can't [do something]"**
→ Upgrade to API mode (see Step 1 above)

**"Not authenticated"**
→ Make sure you run `spotify.authenticate()` once

**"No active device"**
→ Open Spotify and start playing music first

---

✨ **Ready to upgrade? The API version gives you full control!** ✨
