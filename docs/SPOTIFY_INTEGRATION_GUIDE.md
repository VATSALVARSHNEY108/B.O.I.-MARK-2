# Spotify Integration Guide

## Overview

VATSAL AI offers comprehensive Spotify control through multiple methods:
1. **Spotify Web API** (Recommended) - Full control including song search and play
2. **Desktop Automation** - Keyboard shortcuts for local Spotify app
3. **Windows Batch Files** - Quick command-line control

## Setup Methods

### Method 1: Spotify Web API (Recommended) ⭐

**Benefits:**
- ✅ Play specific songs by name
- ✅ Search Spotify catalog
- ✅ Full playback control
- ✅ Get current track info
- ✅ Manage playlists
- ✅ Works from anywhere

**Setup:**
The Spotify connector is already available in your project. It needs to be set up through the Replit interface.

**Status:** Available but needs setup (connector:ccfg_spotify_01K49R1M6S088SR66BS9A0V4R7)

### Method 2: Desktop Automation

**Benefits:**
- ✅ Works without API setup
- ✅ Fast keyboard shortcuts
- ✅ No internet required

**Limitations:**
- ❌ Cannot search or play specific songs
- ❌ Requires Spotify desktop app running
- ❌ Basic controls only

**How it works:** Uses PyAutoGUI to send keyboard shortcuts to Spotify app

### Method 3: Windows Batch Files

**Benefits:**
- ✅ Quick command-line access
- ✅ Works independently
- ✅ Can be called from any script

**Files:**
- `scripts/windows_controls/spotify_control.bat` - Interactive menu
- `scripts/quick_spotify.bat` - Quick commands

## Voice Commands

### Playing Songs (Requires API)

```
"Play Shape of You on Spotify"
"Play song Blinding Lights"
"Play Bohemian Rhapsody by Queen"
"Search and play Despacito on Spotify"
```

### Playback Control

```
"Spotify play"
"Spotify pause"
"Next song on Spotify"
"Previous track on Spotify"
"Skip this song"
```

### Volume Control

```
"Spotify volume 50"
"Set Spotify volume to 80"
"Increase Spotify volume"
"Decrease Spotify volume"
```

### Information

```
"What's playing on Spotify?"
"Current Spotify song"
"Show Spotify track info"
```

### Playlists & Search

```
"Search Spotify for Imagine Dragons"
"Show my Spotify playlists"
"Play my Discover Weekly playlist"
```

### Advanced Controls

```
"Spotify shuffle on"
"Spotify shuffle off"
"Spotify repeat track"
"Spotify repeat playlist"
"Spotify repeat off"
```

## Command Line Usage

### Using Batch Files (Windows)

**Interactive Menu:**
```batch
scripts\windows_controls\spotify_control.bat
```

**Quick Commands:**
```batch
scripts\quick_spotify.bat play
scripts\quick_spotify.bat pause
scripts\quick_spotify.bat next
scripts\quick_spotify.bat prev
scripts\quick_spotify.bat open
```

**Spotify Control Commands:**
```batch
scripts\windows_controls\spotify_control.bat play
scripts\windows_controls\spotify_control.bat pause
scripts\windows_controls\spotify_control.bat next
scripts\windows_controls\spotify_control.bat prev
scripts\windows_controls\spotify_control.bat volup
scripts\windows_controls\spotify_control.bat voldown
scripts\windows_controls\spotify_control.bat shuffle
scripts\windows_controls\spotify_control.bat repeat
scripts\windows_controls\spotify_control.bat open
```

### Using Python API

```python
from modules.utilities.spotify_automation import SpotifyAutomation

spotify = SpotifyAutomation()

# Play a specific song
spotify.play_song("Bohemian Rhapsody")

# Or use play_track
spotify.play_track("Shape of You Ed Sheeran")

# Control playback
spotify.play()
spotify.pause()
spotify.next_track()
spotify.previous_track()

# Volume control (0-100)
spotify.set_volume(75)

# Get current track
track_info = spotify.get_current_track()
print(track_info['message'])

# Search
results = spotify.search("Queen", search_type='artist', limit=5)

# Playlists
playlists = spotify.get_playlists()

# Shuffle and repeat
spotify.shuffle(True)  # or False
spotify.repeat('track')  # or 'context' or 'off'
```

## Integration with Command Executor

The Spotify functionality is fully integrated with the command executor. Available actions:

| Action | Description | Parameters |
|--------|-------------|------------|
| `spotify_play` | Resume playback | - |
| `spotify_pause` | Pause playback | - |
| `spotify_next` | Next track | - |
| `spotify_previous` | Previous track | - |
| `spotify_play_track` | Search and play song | `query` |
| `play_song` | Search and play song (alias) | `song` or `query` |
| `spotify_volume` | Set volume | `volume` (0-100) |
| `spotify_current_track` | Get current song info | - |
| `spotify_search` | Search Spotify | `query`, `type` |
| `spotify_playlists` | Get playlists | - |
| `spotify_shuffle` | Toggle shuffle | `state` (true/false) |
| `spotify_repeat` | Set repeat mode | `state` (track/context/off) |
| `spotify_open` | Open Spotify | - |

## Examples

### Example 1: Play a specific song

**Voice:**
```
"Play Wonderwall on Spotify"
```

**What happens:**
1. VATSAL searches Spotify for "Wonderwall"
2. Finds the first matching track
3. Plays it immediately
4. Returns: "🎵 Playing: Wonderwall - Oasis"

### Example 2: Control playback

**Voice:**
```
"Pause Spotify"
```

**Batch file:**
```batch
scripts\quick_spotify.bat pause
```

**Python:**
```python
spotify.pause()
```

### Example 3: Get current song

**Voice:**
```
"What's playing?"
```

**Response:**
```
▶️ Playing: Bohemian Rhapsody by Queen
Album: A Night at the Opera
```

## Troubleshooting

### Error: "No active Spotify device found"

**Solutions:**
1. Open Spotify app on your computer or phone
2. Start playing any song to activate the device
3. Try the command again

### Error: "Failed to get Spotify access token"

**Solutions:**
1. Spotify connector needs to be set up
2. Connect Spotify through Replit integrations
3. Or use desktop automation mode instead (limited features)

### Songs won't play

**Check:**
1. Is Spotify app open?
2. Are you logged into Spotify?
3. Do you have Spotify Premium? (Required for API control)
4. Is there an active playback device?

### Batch files don't work

**Solutions:**
1. Make sure you're on Windows
2. Run Command Prompt as Administrator
3. Check if Spotify is running
4. Media keys must be enabled in Windows

## Spotify Premium Requirement

**Note:** The Spotify Web API requires a Spotify Premium account for playback control. Free accounts can browse but cannot control playback via API.

**What works with Free:**
- ✅ Search songs/artists/albums
- ✅ Browse playlists
- ✅ Get track information

**What requires Premium:**
- ⚠️ Play/pause control
- ⚠️ Skip tracks
- ⚠️ Volume control
- ⚠️ Play specific songs

**Desktop automation works with both Free and Premium** (but has limitations).

## Tips for Best Experience

1. **Keep Spotify open** - Ensures fast response
2. **Be specific** - "Play Despacito by Luis Fonsi" works better than just "Play Despacito"
3. **Use natural language** - VATSAL understands various phrasings
4. **Check device status** - Make sure Spotify is active on a device
5. **Use API mode** - For full control and song selection

## API Mode vs Desktop Mode

| Feature | API Mode | Desktop Mode |
|---------|----------|--------------|
| Play specific songs | ✅ | ❌ |
| Search catalog | ✅ | ❌ |
| Get current track | ✅ | ❌ |
| Play/Pause | ✅ | ✅ |
| Next/Previous | ✅ | ✅ |
| Volume control | ✅ (exact) | ✅ (steps) |
| Shuffle | ✅ | ✅ |
| Repeat | ✅ | ✅ |
| Requires Premium | ✅ | ❌ |
| Requires setup | ✅ | ❌ |

## Next Steps

1. **For full control**: Set up Spotify connector via Replit
2. **For basic control**: Use desktop automation (already working)
3. **For quick access**: Use batch files on Windows

---

**Version:** 1.0  
**Last Updated:** November 2025  
**Status:** ✅ Fully Integrated
