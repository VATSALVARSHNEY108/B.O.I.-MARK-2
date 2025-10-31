# 🎵 Spotify Integration Guide

## Overview
The AI Desktop Automation Controller now includes full Spotify integration, allowing you to control your music playback using natural language commands through the Gemini AI.

## Setup
✅ Spotify is already connected to your application! You can start using it immediately.

## Features

### 🎵 Playback Control
Control your Spotify playback with simple voice commands:

- **Play/Resume**: Start or resume playback
  - "Play Spotify"
  - "Resume music"
  - "Continue playing"

- **Pause**: Pause current playback
  - "Pause music"
  - "Pause Spotify"
  - "Stop the music"

- **Next Track**: Skip to the next song
  - "Next song"
  - "Skip"
  - "Next track"

- **Previous Track**: Go back to the previous song
  - "Previous song"
  - "Previous track"
  - "Go back"

### 🔍 Search & Play
Search for and play music directly:

- **Play a specific song**:
  - "Play Shape of You on Spotify"
  - "Play Bohemian Rhapsody"
  - "Play despacito by Luis Fonsi on Spotify"

- **Search for music**:
  - "Search Spotify for rock music"
  - "Find Taylor Swift songs"
  - "Search for playlists with jazz"

### 📊 Track Information
Get information about what's playing:

- "What's playing?"
- "Current song"
- "What song is this?"
- "Show me the current track"

### 🎚️ Volume Control
Adjust your Spotify volume:

- "Set volume to 50"
- "Volume 80"
- "Turn volume down to 30"

### 📚 Playlist Management
Browse and access your playlists:

- "Show my playlists"
- "List my Spotify playlists"
- "What playlists do I have?"

### 🔀 Playback Modes

**Shuffle**:
- "Shuffle on"
- "Turn on shuffle"
- "Shuffle off"
- "Disable shuffle"

**Repeat**:
- "Repeat on" (repeats playlist/album)
- "Repeat this track" (repeats single song)
- "Repeat off"

## Example Commands

### Basic Playback
```
You: Play Spotify
✅ Resumed playback

You: Pause music
⏸️ Paused playback

You: Next song
⏭️ Skipped to next track

You: What's playing?
▶️ Playing: Blinding Lights by The Weeknd
Album: After Hours
```

### Search & Play
```
You: Play Perfect by Ed Sheeran on Spotify
🎵 Playing: Perfect - Ed Sheeran

You: Search Spotify for workout music
🔍 Found 5 track(s):
  1. Eye of the Tiger - Survivor
  2. Stronger - Kanye West
  3. Lose Yourself - Eminem
  4. Till I Collapse - Eminem
  5. Remember the Name - Fort Minor
```

### Advanced Features
```
You: Set volume to 60
🔊 Volume set to 60%

You: Shuffle on
🔀 Shuffle on

You: Show my playlists
📚 Your playlists (10):
  1. My Favorites (42 tracks)
  2. Workout Mix (28 tracks)
  3. Chill Vibes (35 tracks)
  ...
```

## Tips & Tricks

1. **Be specific with song searches**: Include both song name and artist for best results
   - ✅ "Play Imagine by John Lennon on Spotify"
   - ❌ "Play that song I like"

2. **Natural language works**: You can use casual phrases
   - "Skip this song"
   - "Turn it up to 80"
   - "What am I listening to?"

3. **Quick actions**: Short commands work great
   - "Next"
   - "Pause"
   - "Play"

4. **Combine with workflows**: Use Spotify commands in multi-step workflows
   - "Play my workout playlist and set a timer for 30 minutes"

## Troubleshooting

### "Failed to get Spotify access token"
**Solution**: The Spotify connection may need to be refreshed. The integration handles this automatically, but if it persists, reconnect Spotify in your integrations.

### "Track not found"
**Solution**: Try being more specific with your search:
- Include the artist name
- Check spelling
- Try searching first: "Search Spotify for [song name]"

### "No active device"
**Solution**: Make sure Spotify is open and playing on at least one device (desktop app, phone, web player, etc.)

## Integration Details

The Spotify integration uses:
- **Replit Connector**: Automatic OAuth and token management
- **Spotify Web API**: Full access to playback, playlists, and search
- **Natural Language Processing**: Gemini AI interprets your commands

## Permissions
The integration has access to:
- ✅ Read your playlists
- ✅ Control playback
- ✅ Read currently playing track
- ✅ Modify playback state
- ✅ Search Spotify catalog
- ✅ Read your library

## Support
For issues or questions about Spotify integration, the connection is managed automatically by Replit. Commands are processed through the main AI automation system.

---

Enjoy controlling your music with your voice! 🎵
