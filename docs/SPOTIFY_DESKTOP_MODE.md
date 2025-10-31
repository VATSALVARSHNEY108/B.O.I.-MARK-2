# 🎵 Spotify Desktop Automation Mode

## Overview
Your Spotify integration now uses **Desktop Automation Mode** - controlling Spotify through keyboard shortcuts instead of the API. This works with the Spotify desktop app installed on your computer!

## How It Works
Instead of using Spotify's API (which has registration requirements), we control the Spotify desktop application directly using:
- ⌨️ **Keyboard shortcuts** (Space, Ctrl+Right, Ctrl+Left, etc.)
- 🖱️ **GUI automation** for search and play features

## Requirements
- ✅ Spotify Desktop App installed on your computer
- ✅ PyAutoGUI (already installed)
- ✅ Spotify must be open to receive commands

## Available Commands

### Basic Playback
| Command | Keyboard Shortcut | Action |
|---------|------------------|--------|
| Play/Pause | Space | Toggle playback |
| Next | Ctrl+Right | Next track |
| Previous | Ctrl+Left | Previous track |
| Shuffle | Ctrl+S | Toggle shuffle |
| Repeat | Ctrl+R | Toggle repeat |
| Mute | Ctrl+M | Toggle mute |

### Volume Control
- **Volume Up**: Ctrl+Up (increases by steps)
- **Volume Down**: Ctrl+Down (decreases by steps)

### Natural Language Commands
You can use these natural language commands:

**Opening Spotify:**
- "Open Spotify"
- "Launch Spotify"

**Playback Control:**
- "Pause music"
- "Play Spotify"
- "Next song"
- "Previous track"
- "Skip"

**Search and Play:**
- "Play Shape of You on Spotify"
- "Play Bohemian Rhapsody"
- "Play despacito by Luis Fonsi on Spotify"

**Volume:**
- "Volume up"
- "Louder"
- "Volume down"
- "Quieter"
- "Mute Spotify"

**Playback Modes:**
- "Shuffle"
- "Repeat"

## Example Session

```
You: Open Spotify
🎵 Opening Spotify...

You: Play Shape of You on Spotify
🎵 Searching and playing: Shape of You

You: Volume up
🔊 Volume up (1 step)

You: Next song
⏭️ Next track

You: Pause music
⏯️ Toggled play/pause
```

## Limitations of Desktop Mode

❌ **Not Available:**
- Getting current track info (can't read from app)
- Browsing search results
- Listing playlists
- Setting exact volume percentage
- Reading playback state

✅ **Works Great:**
- Play/pause control
- Skipping tracks
- Volume control (up/down)
- Search and play songs
- Shuffle and repeat
- Opening Spotify app

## Tips for Best Results

1. **Keep Spotify Open**: The desktop app must be running for commands to work

2. **Focus**: Commands work even if Spotify is in the background

3. **Search and Play**: The search feature automatically:
   - Opens search (Ctrl+L)
   - Types your query
   - Presses Enter to search
   - Presses Enter again to play first result

4. **Volume Control**: Use "volume up" multiple times for bigger changes
   - "Volume up" = increase once
   - You can repeat the command for more volume

## Keyboard Shortcuts Reference

### Windows/Linux:
- Space: Play/Pause
- Ctrl+Right: Next
- Ctrl+Left: Previous
- Ctrl+Up: Volume Up
- Ctrl+Down: Volume Down
- Ctrl+S: Shuffle
- Ctrl+R: Repeat
- Ctrl+M: Mute
- Ctrl+L: Search

### macOS:
- Space: Play/Pause
- Cmd+Right: Next
- Cmd+Left: Previous
- Cmd+Up: Volume Up
- Cmd+Down: Volume Down
- Cmd+S: Shuffle
- Cmd+R: Repeat
- Cmd+M: Mute
- Cmd+L: Search

## Advantages of Desktop Mode

✅ **No API Registration**: Works immediately without Spotify Developer account
✅ **No Authentication Issues**: No OAuth or token management
✅ **Offline Control**: Works even without internet (for downloaded songs)
✅ **Universal**: Works on Windows, macOS, and Linux
✅ **Reliable**: Uses standard Spotify keyboard shortcuts

## Troubleshooting

### "Failed to toggle play/pause"
- Make sure Spotify desktop app is installed and running
- Check that PyAutoGUI is working (try other automation commands)

### Search doesn't work
- Ensure Spotify is open and not minimized
- The search bar must be accessible
- Try manually pressing Ctrl+L to test if search opens

### Volume commands don't work
- Some Spotify versions may have different shortcuts
- Check Spotify preferences for keyboard shortcuts
- Use the volume slider in Spotify app instead

## Switching Between Modes

If you want to switch back to API mode (once registration is fixed):
- Edit `command_executor.py`
- Change `from spotify_desktop_automation` to `from spotify_automation`
- Change `create_spotify_desktop_automation()` to `create_spotify_automation()`

---

**Enjoy controlling Spotify with your voice and natural language! 🎵**
