# 🔊☀️ Volume & Brightness Control Features

## Overview

Kai AI Assistant now includes comprehensive system-level volume and brightness controls that work seamlessly with voice commands and the GUI. Control your computer's volume and screen brightness using natural language!

## ✅ Features Added

### Volume Control 🔊
- **Set Volume**: Set system volume to any level (0-100%)
- **Increase Volume**: Raise volume by specified amount (default: 10%)
- **Decrease Volume**: Lower volume by specified amount (default: 10%)
- **Mute**: Silence all system audio
- **Unmute**: Restore system audio
- **Toggle Mute**: Switch between muted and unmuted
- **Check Volume**: Get current volume level

### Brightness Control ☀️
- **Set Brightness**: Set screen brightness to any level (0-100%)
- **Increase Brightness**: Raise brightness by specified amount (default: 10%)
- **Decrease Brightness**: Lower brightness by specified amount (default: 10%)
- **Get Brightness**: Check current brightness level
- **Auto Brightness**: Automatically adjust based on time of day

## 🗣️ Voice Commands

### Volume Commands

```
# Basic Volume Control
"Kai, increase volume"
"Hey Watson, decrease volume"
"Kai, volume up"
"Watson, volume down"
"Kai, louder"
"Hey Kai, quieter"

# Set Specific Volume
"Kai, set volume to 50"
"Watson, volume 75 percent"
"Hey Kai, set volume to 30%"

# Mute/Unmute
"Kai, mute"
"Watson, mute volume"
"Kai, unmute"
"Hey Watson, unmute volume"
"Kai, toggle mute"

# Check Volume
"Kai, what's the volume?"
"Watson, check volume"
"Hey Kai, current volume"

# Custom Amount
"Kai, increase volume by 20"
"Watson, decrease volume by 5"
"Kai, raise volume 15"
```

### Brightness Commands

```
# Basic Brightness Control
"Kai, increase brightness"
"Watson, decrease brightness"
"Hey Kai, brighten screen"
"Watson, dim screen"
"Kai, make screen brighter"
"Hey Watson, make screen darker"

# Set Specific Brightness
"Kai, set brightness to 80"
"Watson, brightness 50 percent"
"Hey Kai, set brightness to 25%"

# Check Brightness
"Kai, what's the brightness?"
"Watson, check brightness"
"Hey Kai, current brightness"

# Auto Brightness
"Kai, auto brightness"
"Watson, enable auto brightness"

# Custom Amount
"Kai, increase brightness by 20"
"Watson, decrease brightness by 15"
```

## 💻 Platform Support

### Windows
- ✅ Volume control via `nircmd.exe`
- ✅ Brightness control via WMI PowerShell
- ✅ Full mute/unmute support

### macOS
- ✅ Volume control via `osascript`
- ✅ Brightness control via `brightness` command
- ✅ Full mute/unmute support

### Linux
- ✅ Volume control via `pactl` (PulseAudio)
- ✅ Brightness control via `xrandr`
- ✅ Full mute/unmute support

## 🛠️ Technical Implementation

### System Control Module
Location: `modules/system/system_control.py`

**Volume Methods:**
- `set_volume(level)` - Set volume 0-100
- `increase_volume(amount=10)` - Increase by amount
- `decrease_volume(amount=10)` - Decrease by amount
- `get_volume()` - Get current level
- `mute_volume()` - Mute audio
- `unmute_volume()` - Unmute audio
- `toggle_mute()` - Toggle mute state
- `get_volume_info()` - Get volume details

**Brightness Methods:**
- `set_brightness(level)` - Set brightness 0-100
- `increase_brightness(amount=10)` - Increase by amount
- `decrease_brightness(amount=10)` - Decrease by amount
- `get_brightness()` - Get current level
- `auto_brightness()` - Auto-adjust based on time

### Command Integration
Location: `modules/core/command_executor.py`

**Available Actions:**
```python
# Volume Actions
- set_volume
- increase_volume / volume_up
- decrease_volume / volume_down
- mute_volume
- unmute_volume
- toggle_mute
- get_volume

# Brightness Actions
- set_brightness
- increase_brightness
- decrease_brightness
- get_brightness
- auto_brightness
```

### AI Command Parser
Location: `modules/core/gemini_controller.py`

The Gemini AI automatically recognizes natural language commands and converts them to appropriate actions.

## 📝 Usage Examples

### Via Voice Commands

```bash
# Start the GUI with voice enabled
python modules/core/gui_app.py

# Enable continuous listening (click 🔊 button)
# Say wake word + command:
"Kai, increase volume"
"Watson, set brightness to 60"
"Hey Kai, mute"
```

### Via Text Commands

Type in the command input box:
```
increase volume by 20
set brightness to 75
mute volume
check current brightness
```

### Via Python Code

```python
from modules.system.system_control import SystemController

controller = SystemController()

# Volume control
controller.set_volume(50)
controller.increase_volume(10)
controller.decrease_volume(5)
controller.mute_volume()
controller.unmute_volume()
volume = controller.get_volume()
print(f"Current volume: {volume}%")

# Brightness control
controller.set_brightness(80)
controller.increase_brightness(10)
controller.decrease_brightness(15)
brightness = controller.get_brightness()
print(f"Current brightness: {brightness}%")
controller.auto_brightness()
```

## 🎯 Smart Features

### Context-Aware Commands
The AI understands context and chooses between system volume and Spotify volume:

```
"increase volume" → System volume
"increase Spotify volume" → Spotify volume only
"volume up" → System volume (default)
"louder" → System volume
```

### Auto-Brightness
Automatically adjusts brightness based on time of day:
- **Daytime (6 AM - 6 PM)**: Higher brightness (default: 80%)
- **Nighttime (6 PM - 6 AM)**: Lower brightness (default: 30%)

Configure in `system_config.json`:
```json
{
  "brightness_schedule": {
    "enabled": true,
    "day_brightness": 80,
    "night_brightness": 30
  }
}
```

## 🚀 Quick Start

1. **Start the GUI**:
   ```bash
   python modules/core/gui_app.py
   ```

2. **Enable Voice**:
   - Click the 🔊 button to enable continuous listening
   - Make sure 💬 button is green (wake word enabled)

3. **Test Volume Control**:
   ```
   "Kai, set volume to 50"
   "Kai, increase volume"
   "Kai, mute"
   ```

4. **Test Brightness Control**:
   ```
   "Kai, set brightness to 70"
   "Kai, increase brightness"
   "Kai, dim screen"
   ```

## ⚙️ Configuration

### Windows Setup
For full functionality on Windows, ensure `nircmd.exe` is available:
1. Download NirCmd from https://www.nirsoft.net/utils/nircmd.html
2. Place `nircmd.exe` in your system PATH or project directory

### macOS Setup
Install brightness control utility:
```bash
brew install brightness
```

### Linux Setup
Ensure PulseAudio is installed:
```bash
sudo apt-get install pulseaudio
sudo apt-get install pulseaudio-utils
```

## 🔧 Troubleshooting

### Volume Control Not Working

**Windows:**
- Ensure `nircmd.exe` is accessible
- Check if audio drivers are properly installed

**macOS:**
- Ensure System Preferences → Security & Privacy allows Terminal/Python to control audio

**Linux:**
- Check if PulseAudio is running: `pulseaudio --check`
- Restart PulseAudio: `pulseaudio -k && pulseaudio --start`

### Brightness Control Not Working

**Windows:**
- Some monitors don't support software brightness control
- Check if WMI service is running

**macOS:**
- Install brightness utility: `brew install brightness`
- Check if brightness command is in PATH

**Linux:**
- Ensure X11 is running
- Check if xrandr is available: `which xrandr`
- Some displays may not support software brightness

## 📊 Response Messages

### Volume
- ✅ `🔊 Volume set to 50%`
- ✅ `🔊 Volume increased by 10%`
- ✅ `🔉 Volume decreased by 10%`
- ✅ `🔇 Volume muted`
- ✅ `🔊 Volume unmuted`
- ✅ `🔊 Current Volume: 65%`

### Brightness
- ✅ `✅ Brightness set to 75%`
- ✅ `✅ Brightness increased by 10%`
- ✅ `✅ Brightness decreased by 15%`
- ✅ `☀️ Current brightness: 60%`

## 🎉 Benefits

- ✅ **Hands-Free Control** - Adjust volume/brightness with voice
- ✅ **Cross-Platform** - Works on Windows, macOS, and Linux
- ✅ **Natural Language** - Use conversational commands
- ✅ **Fine-Grained Control** - Set exact levels or adjust incrementally
- ✅ **Smart Context** - AI understands system vs app-specific controls
- ✅ **Wake Word Support** - Use "Kai" or "Watson" to activate

---

**Created:** November 4, 2025  
**Version:** 2.1.0 - Kai Edition  
**Status:** ✅ Fully Implemented & Tested
