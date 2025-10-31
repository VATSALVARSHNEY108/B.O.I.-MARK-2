# 🔊 Voice Sound Effects Guide

## Overview

Your voice commanding system now has **dynamic WAV file playback** that plays sound effects during voice command interactions! This provides audio feedback for a more engaging user experience.

## 🎵 Sound Effects Events

The system automatically plays sounds at these key moments:

### 1. **Wake Word Detected** 🎯
- **Sound:** `wake_word.wav`
- **When:** A wake word like "bhai", "vatsal", or "hey computer" is detected
- **Purpose:** Confirms the system heard the wake word

### 2. **Listening** 👂
- **Sound:** `listening.wav`
- **When:** The system is waiting for your command after detecting the wake word
- **Purpose:** Indicates the system is ready to receive your command

### 3. **Processing** ⚙️
- **Sound:** `processing.wav`
- **When:** The system is processing your voice command
- **Purpose:** Confirms the command was received and is being executed

### 4. **Success** ✅
- **Sound:** `success.wav`
- **When:** A command is successfully executed
- **Purpose:** Confirms successful command execution

### 5. **Error** ❌
- **Sound:** `error.wav`
- **When:** The system couldn't understand your command or an error occurred
- **Purpose:** Alerts you to try again

### 6. **Thinking** 🤔
- **Sound:** `thinking.wav`
- **When:** The system is processing complex requests
- **Purpose:** Indicates the AI is working on your request

## 📁 Sound Files Location

All sound effects are stored in:
```
voice_sounds/
├── wake_word.wav
├── listening.wav
├── processing.wav
├── success.wav
├── error.wav
└── thinking.wav
```

## 🎨 Customizing Sound Effects

### Default Sounds
The system automatically creates simple beep sounds if custom WAV files don't exist. Each sound has a different frequency:
- Wake word: 800 Hz (high beep)
- Listening: 600 Hz (mid beep)
- Processing: 700 Hz (quick beep)
- Success: 1000 Hz (success tone)
- Error: 400 Hz (low error tone)
- Thinking: 650 Hz (thinking tone)

### Adding Custom Sounds

#### Option 1: Replace Default Files
Simply replace the WAV files in the `voice_sounds/` directory with your own custom sounds. Make sure they're named correctly:
- `wake_word.wav`
- `listening.wav`
- `processing.wav`
- `success.wav`
- `error.wav`
- `thinking.wav`

#### Option 2: Programmatically Add Custom Sounds
```python
from voice_commander import create_voice_commander

commander = create_voice_commander()

# Add a custom sound effect
commander.add_custom_sound('wake_word', '/path/to/your/custom_beep.wav')
```

## 🎛️ Controlling Sound Effects

### Enable/Disable Sounds

```python
# Disable sound effects
commander.disable_sound_effects()

# Enable sound effects
commander.enable_sound_effects()

# Toggle sound effects on/off
commander.toggle_sound_effects()
```

### Adjust Volume

```python
# Set volume (0.0 to 1.0)
commander.set_sound_volume(0.7)  # 70% volume
commander.set_sound_volume(0.5)  # 50% volume
commander.set_sound_volume(1.0)  # 100% volume
```

### List Available Sounds

```python
# Get information about all sound effects
result = commander.list_sound_effects()
print(result['sounds'])
```

## 🎤 Example Usage

```python
from voice_commander import create_voice_commander

def handle_command(command):
    print(f"Executing: {command}")

# Create voice commander with sound effects
commander = create_voice_commander(command_callback=handle_command)

# Start listening with automatic sound feedback
commander.start_continuous_listening()

# Say: "bhai open notepad"
# You'll hear:
# 1. Wake word sound (beep!)
# 2. Processing sound (quick beep)
# 3. Success sound (higher beep)
```

## 🔧 Technical Details

### Audio Format Requirements
- **Format:** WAV (Waveform Audio File Format)
- **Sample Rate:** 22050 Hz (default)
- **Bit Depth:** 16-bit PCM
- **Channels:** Mono or Stereo

### Creating Custom Sounds

You can create custom WAV files using:
1. **Audacity** (free audio editor)
2. **Online tools** like Online-Convert.com
3. **Python** with libraries like `numpy` and `wave`
4. **AI sound generators** like ElevenLabs or other text-to-sound tools

### Example: Creating a Custom Beep with Python

```python
import numpy as np
import wave

def create_custom_beep(filename, frequency=440, duration=0.2):
    """Create a custom beep sound"""
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Generate sine wave
    wave_data = np.sin(2 * np.pi * frequency * t)
    
    # Convert to 16-bit PCM
    wave_data = (wave_data * 32767).astype(np.int16)
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())

# Create a pleasant notification sound
create_custom_beep('voice_sounds/wake_word.wav', frequency=880, duration=0.15)
```

## 🎯 Best Practices

1. **Keep sounds short** - 0.1 to 0.3 seconds is ideal
2. **Use distinct frequencies** - Different sounds should be easily distinguishable
3. **Avoid loud sounds** - Keep volumes comfortable
4. **Test thoroughly** - Make sure sounds don't overlap with speech recognition
5. **Consider accessibility** - Provide visual feedback as well for hearing-impaired users

## ⚙️ Configuration

### Sound Effects Settings

```python
# Check if sound effects are enabled
status = commander.get_status()
print(f"Sound effects enabled: {status['sound_effects_enabled']}")

# Get detailed sound information
sounds = commander.list_sound_effects()
for name, info in sounds['sounds'].items():
    print(f"{name}: {info['path']} (exists: {info['exists']})")
```

## 🐛 Troubleshooting

### No Sound Playing?

1. **Check if pygame is installed:**
   ```bash
   pip install pygame
   ```

2. **Verify sound files exist:**
   ```python
   import os
   print(os.listdir('voice_sounds'))
   ```

3. **Check system audio:**
   - Ensure your system's audio is not muted
   - Test with other applications

4. **Enable sound effects:**
   ```python
   commander.enable_sound_effects()
   ```

### Sound Effects Too Loud/Quiet?

```python
# Adjust volume
commander.set_sound_volume(0.5)  # 50% volume
```

### Sounds Not Playing at Right Time?

The sound effects are played asynchronously (in the background) to avoid blocking the voice recognition. If you notice timing issues, check that:
- Sound files are short (< 0.5 seconds)
- System is not overloaded
- Audio drivers are up to date

## 🚀 Advanced Features

### Custom Sound Events

You can add your own custom sound events:

```python
# Add a custom celebration sound
commander.add_custom_sound('celebration', 'sounds/party.wav')

# Play it manually when needed
commander.sound_effects.play_sound('celebration')
```

### Multiple Sound Profiles

Create different sound profiles for different moods or contexts:

```python
# Professional profile (subtle beeps)
professional_sounds = {
    'wake_word': 'sounds/professional/wake.wav',
    'success': 'sounds/professional/success.wav'
}

# Fun profile (playful sounds)
fun_sounds = {
    'wake_word': 'sounds/fun/boing.wav',
    'success': 'sounds/fun/yay.wav'
}
```

## 📝 Notes

- Sound effects are **enabled by default** when voice commander is initialized
- Sounds play **asynchronously** (don't block voice recognition)
- If WAV files don't exist, the system **auto-generates simple beeps**
- All sounds are played through **pygame.mixer** for reliable cross-platform support

## 🎉 Enjoy Your Voice Commanding Experience!

Your voice assistant now provides rich audio feedback for a more engaging and intuitive user experience. Customize the sounds to match your preferences and workflow!
