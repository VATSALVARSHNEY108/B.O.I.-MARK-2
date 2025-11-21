
# Spotify Quick Start Guide 🎵

## ✅ Spotify Integration is Ready!

Your BOI AI has full Spotify integration with batch files and song playing!

## Quick Commands

### Voice Commands (Easiest!)

**Play a song:**
```
"Play Bohemian Rhapsody on Spotify"
"Play Shape of You"
"Play song Blinding Lights"
```

**Control playback:**
```
"Spotify play"
"Spotify pause"
"Next song"
"Previous track"
```

**Get info:**
```
"What's playing on Spotify?"
"Current song"
```

### Windows Batch Files

**Interactive menu:**
```batch
scripts\windows_controls\spotify_control.bat
```

**Quick commands:**
```batch
scripts\quick_spotify.bat play
scripts\quick_spotify.bat pause
scripts\quick_spotify.bat next
scripts\quick_spotify.bat prev
```

### Python Test Script

```bash
python scripts/test_spotify_play.py
```

## How It Works

### API Mode (For playing specific songs)
- ✅ Search and play any song
- ✅ Full playback control
- ✅ Get track information
- ⚠️ Requires Spotify Premium
- ⚠️ Needs Replit connector setup

### Desktop Mode (Basic control)
- ✅ Play/pause/next/previous
- ✅ Works with free Spotify
- ✅ No setup needed
- ❌ Can't search for songs

### Batch Files (Windows only)
- ✅ Quick command-line access
- ✅ Media key shortcuts
- ✅ Works independently

## What's Been Created

### Batch Files:
1. `scripts/windows_controls/spotify_control.bat` - Interactive menu with all controls
2. `scripts/quick_spotify.bat` - Quick commands (play, pause, next, prev, open)

### Python Enhancements:
1. Added `play_song()` method to SpotifyAutomation
2. Enhanced command executor with multiple action aliases:
   - `play_song`
   - `play_spotify_song`
   - `spotify_play_track`

### Documentation:
1. `docs/SPOTIFY_INTEGRATION_GUIDE.md` - Complete 300+ line guide
2. `SPOTIFY_QUICK_START.md` - This file!

### Test Script:
1. `scripts/test_spotify_play.py` - Interactive Spotify testing

## Try It Now!

### Option 1: Use Voice
Just say: **"Play Wonderwall on Spotify"**

### Option 2: Use Batch File
```batch
scripts\quick_spotify.bat play
```

### Option 3: Test with Python
```bash
python scripts/test_spotify_play.py
```

## Command Reference

| What You Say | What It Does |
|--------------|--------------|
| "Play [song name] on Spotify" | Searches and plays the song |
| "Spotify play" | Resumes playback |
| "Spotify pause" | Pauses playback |
| "Next song" | Skips to next track |
| "Previous track" | Goes back |
| "What's playing?" | Shows current song |
| "Spotify volume 75" | Sets volume to 75% |
| "Shuffle on Spotify" | Enables shuffle |

## Troubleshooting

**"No active Spotify device found"**
- Solution: Open Spotify app and start playing something

**"Failed to get access token"**
- Solution: Spotify connector needs setup via Replit interface
- Alternative: Use desktop mode (basic controls only)

**"Can't search for songs"**
- Solution: You're in desktop mode. Either:
  1. Set up Spotify API connector, OR
  2. Manually open Spotify and search, then use voice to control playback

## Full Documentation

For complete details, see: `docs/SPOTIFY_INTEGRATION_GUIDE.md`

---

**Status:** ✅ Fully Integrated  
**Date:** November 2025  
**Batch Files:** ✅ Created  
**Song Playing:** ✅ Implemented  
**Integration:** ✅ Complete
