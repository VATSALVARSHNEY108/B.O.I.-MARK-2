# 🎤 Voice Commanding Guide for BOI

## Overview

BOI now supports **comprehensive voice commanding** - speak your commands and hear BOI's responses! Control all 300+ features using your voice with advanced speech recognition and text-to-speech capabilities.

---

## ✨ Features

### 🎯 **Voice Input Modes**

1. **Push-to-Talk Mode** 🎤
   - Click the green microphone button
   - Speak your command (up to 10 seconds)
   - System automatically executes after recognizing speech
   - Perfect for single commands
   - No wake word required

2. **Continuous Listening Mode** 🔊
   - Click the speaker button to enable
   - System listens continuously in the background
   - Use wake words to activate commands
   - Automatically processes spoken commands
   - Say "stop listening" to disable
   - Ideal for hands-free operation

3. **Wake Word Detection** 💬 (NEW!)
   - **Enabled by default** in continuous mode
   - Multiple wake words supported:
     - "Hey BOI"
     - "BOI"
     - "OK BOI"
     - "Computer"
     - "Hey Computer"
     - "Bhiaya" (Hindi/Urdu: Brother)
     - "Bhaisahb" (Hindi/Urdu: Respected Brother)
   - Click 💬 button to toggle on/off
   - When enabled: Say wake word + command
   - When disabled: All speech is processed

### 🔊 **Voice Output**

- **BOI Speaks Back**: When BOI Mode is ON, all responses are spoken aloud
- **Natural Voice**: Human-like text-to-speech with personality
- **Smart Queueing**: Responses are queued and spoken in order
- **Background Processing**: Speech doesn't block other operations

---

## 🚀 How to Use

### Basic Voice Commands

1. **Push-to-Talk**:
   ```
   Click 🎤 button → Speak command → Listen for response
   ```

2. **Continuous Listening**:
   ```
   Click 🔊 button → Say "Hey BOI" → Then your command → Say "stop listening" to disable
   ```

3. **Wake Word Examples**:
   ```
   "Hey BOI, what time is it?"
   "BOI, take a screenshot"
   "OK BOI, check system information"
   "Computer, play lofi beats"
   "Bhiaya, open downloads folder"
   "Bhaisahb, show system report"
   ```

### Example Commands

You can speak **any command** that BOI understands:

**System Control:**
- "Take a screenshot"
- "Check system information"
- "Increase brightness"
- "Show CPU usage"

**File Management:**
- "Open downloads folder"
- "Search for Python files"
- "Organize downloads"

**Web & Search:**
- "Search Google for Python tutorials"
- "Play lofi beats on YouTube"
- "What's the weather today"

**Code Generation:**
- "Write Python code for bubble sort"
- "Generate a React component for login"
- "Explain this code"

**Productivity:**
- "Start Pomodoro timer"
- "Add note reminder for tomorrow"
- "Create calendar event"

**Communication:**
- "Send email to John"
- "Add contact with phone number"

**AI Features:**
- "Write a story about robots"
- "Analyze my last screenshot"
- "Generate creative ideas for app names"

**And 300+ more features!**

---

## 🎨 UI Controls

### Voice Buttons Location
Located next to the Execute button in the command input area:

- **🎤 Green Button** (Left): Push-to-Talk - Click to speak once
- **🔊 Gray Button** (Middle): Continuous Listening - Toggle on/off
- **💬 Yellow Button** (Right): Wake Word Toggle - Enable/disable wake word detection

### Visual Feedback

1. **Microphone Button States**:
   - 🟢 Green: Ready to listen
   - 🔴 Red: Currently listening
   - Returns to green after processing

2. **Continuous Listening Button**:
   - 🔘 Gray/Muted (🔊): Listening OFF
   - 🟢 Green (🔇): Listening ON

3. **Wake Word Button**:
   - 🟡 Yellow (💬): Wake word OFF (all speech processed)
   - 🟢 Green (💬): Wake word ON (requires wake word)

3. **Status Bar**:
   - "🎤 Listening...": System is capturing audio
   - "🎤 Voice Active": Continuous mode enabled
   - "✅ Ready": System ready for next command

4. **Output Console**:
   - Shows "🎤 Listening for voice command..."
   - Displays recognized speech
   - Shows BOI's response

---

## ⚙️ Technical Details

### Requirements

- **Microphone Access**: System needs microphone permissions
- **Internet Connection**: Google Speech Recognition API requires internet
- **Audio Output**: Speakers or headphones for voice responses

### Voice Recognition

- **Engine**: Google Speech Recognition
- **Language**: English (default)
- **Timeout**: 10 seconds for push-to-talk
- **Continuous**: 1-second intervals with auto-renewal
- **Noise Handling**: Automatic ambient noise adjustment

### Text-to-Speech

- **Engine**: pyttsx3 (offline TTS)
- **Speed**: 165 words per minute
- **Volume**: 95%
- **Voice**: System default (configurable)

### Performance

- **Latency**: 1-3 seconds for recognition
- **Accuracy**: 90%+ with clear speech
- **Multi-threading**: Non-blocking operation
- **Resource Usage**: Minimal CPU/memory impact

---

## 🔧 Tips for Best Results

### For Voice Recognition

✅ **Do:**
- Speak clearly and at normal pace
- Use natural language (BOI understands context)
- Wait for the "listening" indicator
- Minimize background noise
- Position microphone properly

❌ **Avoid:**
- Speaking too fast or mumbling
- Background music/TV during recognition
- Very long commands (break them up)
- Speaking before "listening" indicator shows

### For Voice Output

✅ **Do:**
- Enable BOI Mode for personality responses
- Adjust system volume to comfortable level
- Let BOI finish speaking before next command

❌ **Avoid:**
- Interrupting speech output (may cause issues)
- Muting audio - you won't hear responses

---

## 🐛 Troubleshooting

### "Voice commander not available" Error

**Cause**: Speech recognition library not initialized
**Fix**: 
1. Check microphone permissions
2. Restart the application
3. Verify `speechrecognition` and `pyttsx3` are installed

### "No speech detected (timeout)"

**Cause**: Microphone not picking up audio or silence
**Fix**:
1. Check microphone connection
2. Test microphone in system settings
3. Speak louder or closer to microphone
4. Reduce timeout period if too sensitive

### "Could not understand audio"

**Cause**: Speech unclear or background noise
**Fix**:
1. Speak more clearly
2. Reduce background noise
3. Move closer to microphone
4. Try again with simpler command

### "Recognition service error"

**Cause**: No internet connection
**Fix**:
1. Check internet connectivity
2. Try again when online
3. Google Speech API requires internet

### Text-to-Speech Not Working

**Cause**: Audio output issue or TTS engine problem
**Fix**:
1. Check speaker/headphone connection
2. Verify system volume not muted
3. Restart application
4. Check BOI Mode is ON

---

## 🎯 Voice Command Best Practices

### Command Structure

**Good Examples:**
- "Take a screenshot" ✅
- "Search Google for Python tutorials" ✅
- "What's the weather today" ✅
- "Open downloads folder" ✅

**Less Optimal:**
- "Um... can you maybe... take a screenshot?" ❌
- Very long run-on sentences ❌
- Commands with lots of filler words ❌

### Multi-Step Commands

BOI can handle complex requests:
- "Search for Python files and organize them by date"
- "Check system information and take a screenshot"
- "Create a calendar event for tomorrow at 2 PM called team meeting"

### Natural Language

BOI understands context:
- "What time is it?" → Shows current time
- "How's my system doing?" → System report
- "Play some music" → Opens YouTube/Spotify
- "Help me code a calculator" → Generates code

---

## 🔐 Privacy & Security

- **Local Processing**: TTS runs completely offline
- **Google Speech API**: Voice data sent to Google for recognition
- **No Storage**: Voice commands are not stored
- **Temporary**: Audio processed in real-time, then discarded
- **Secure**: No voice data saved to disk

---

## 🎓 Advanced Features

### Wake Word (AVAILABLE NOW!)
- **Active Feature**: Wake word detection enabled
- **Multiple Wake Words**: "Hey BOI", "BOI", "OK BOI", "Computer", "Hey Computer"
- **True Hands-Free**: Say wake word before command in continuous mode
- **Toggle Control**: Use 💬 button to enable/disable
- **Privacy Friendly**: Only processes speech when wake word detected (when enabled)

### Voice Profiles (Future)
- Custom voice selection
- Speed/pitch adjustment
- Language support expansion

### Voice Macros (Future)
- Record voice command sequences
- One-word triggers for complex workflows
- Voice shortcuts

---

## 📊 Comparison: Voice vs Text Input

| Feature | Voice Input | Text Input |
|---------|------------|------------|
| Speed | ⚡ Fast (1-3 sec) | ⚡⚡ Very Fast (instant) |
| Accuracy | ~90% | ~100% |
| Hands-free | ✅ Yes | ❌ No |
| Multi-tasking | ✅ Yes | ⚠️ Limited |
| Complex commands | ⚠️ Good | ✅ Excellent |
| Precise syntax | ⚠️ Good | ✅ Perfect |
| Best for | Quick tasks, accessibility | Complex tasks, precision |

---

## 🌟 Use Cases

### Perfect for Voice Commands

1. **Hands-Free Work**: 
   - Coding while looking at reference
   - Taking notes while reading
   - Multitasking workflows

2. **Accessibility**:
   - Users with mobility limitations
   - RSI/carpal tunnel relief
   - Eye strain reduction

3. **Quick Tasks**:
   - Fast system checks
   - Quick screenshots
   - Rapid web searches

4. **Demonstration**:
   - Presenting to others
   - Teaching/training
   - Showcasing features

### Better with Text Input

1. **Complex Code**: Detailed code generation
2. **Precise Commands**: Specific file paths
3. **Silent Environments**: Libraries, offices
4. **Private Tasks**: Sensitive information

---

## 🎉 Getting Started

1. **Enable Voice Commanding**:
   - Voice is enabled by default
   - Click 🎤 button to test
   - Speak a simple command like "what time is it"

2. **Try Continuous Mode**:
   - Click 🔊 button
   - Speak multiple commands
   - Say "stop listening" when done

3. **Experiment**:
   - Try different command types
   - Use natural language
   - Combine with BOI personality

4. **Customize**:
   - Adjust system volume
   - Test microphone sensitivity
   - Find your optimal setup

---

## 📞 Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Verify microphone/speaker setup
3. Review system permissions
4. Restart the application

---

**Voice commanding makes BOI even more powerful and accessible. Speak your mind, and BOI will respond!** 🎤🤖

---

*Last Updated: October 28, 2025*
*Compatible with: BOI (Barely Obeys Instructions) Desktop Automation Controller v2.0+*
