# 🎤 Voice Changing Guide - Fun Voices! 🎭

Your voice assistant now supports **multiple voice styles** including male, female, robot, chipmunk, and more funny voices!

---

## 🎨 Available Voice Styles

### 1. 👨 **Male Voice**
Standard male voice with normal speed
```
"Bhai, change voice to male"
```

### 2. 👩 **Female Voice** (Default)
Standard female voice with normal speed
```
"Bhai, change voice to female"
```

### 3. 🤖 **Robot Voice**
Robotic-sounding voice with steady pace
```
"Bhai, change voice to robot"
```

### 4. 🐿️ **Chipmunk Voice**
High-pitched, super-fast voice (hilarious!)
```
"Bhai, change voice to chipmunk"
```

### 5. 🎙️ **Deep Voice**
Low-pitched, slow voice for dramatic effect
```
"Bhai, change voice to deep"
```

### 6. 😂 **Funny Voice**
Fast-paced, energetic voice
```
"Bhai, change voice to funny"
```

### 7. ⚡ **Fast Voice**
Quick-talking voice
```
"Bhai, change voice to fast"
```

### 8. 🐌 **Slow Voice**
Slow, deliberate voice
```
"Bhai, change voice to slow"
```

---

## 🎚️ Voice Speed Control

Change how fast the assistant talks:

### Speed Options:
- **Very Slow** (80 wpm): `"Bhai, speak very slow"`
- **Slow** (120 wpm): `"Bhai, speak slower"`
- **Normal** (150 wpm): `"Bhai, speak normal speed"`
- **Fast** (200 wpm): `"Bhai, speak faster"`
- **Very Fast** (250 wpm): `"Bhai, speak very fast"`
- **Super Fast** (300 wpm): `"Bhai, speak super fast"`

---

## 📋 Voice Information Commands

### List All Available Voices
See all voices installed on your system:
```
"Bhai, list voices"
```

### Check Current Voice
Get information about the current voice:
```
"Bhai, current voice"
```

---

## 🎯 Complete Voice Command List

| Command | Effect |
|---------|--------|
| "Change voice to male" | Switch to male voice |
| "Change voice to female" | Switch to female voice |
| "Change voice to robot" | Robotic voice |
| "Change voice to chipmunk" | High & fast (funny!) |
| "Change voice to deep" | Low & slow |
| "Change voice to funny" | Energetic voice |
| "Speak faster" | Increase speed |
| "Speak slower" | Decrease speed |
| "Speak very fast" | Maximum speed |
| "Speak super fast" | Super quick |
| "Speak very slow" | Very slow |
| "List voices" | Show all voices |
| "Current voice" | Show voice info |

---

## 💡 Usage Examples

### Example 1: Fun Conversation
```
You: "Bhai, change voice to chipmunk"
Assistant: "✅ Voice changed to CHIPMUNK mode!"
         → Speaks in high-pitched fast voice

You: "Tell me a joke"
Assistant: "Why did the programmer quit? Because he didn't get arrays!"
         → Joke in chipmunk voice (hilarious!)
```

### Example 2: Professional Mode
```
You: "Bhai, change voice to male"
Assistant: "✅ Voice changed to MALE mode!"

You: "Speak slower"
Assistant: "✅ Voice speed set to SLOW (120 wpm)"

You: "What time is it?"
Assistant: "It's 3:45 PM"
         → Spoken in slow, deep male voice
```

### Example 3: Robot Mode
```
You: "Bhai, change voice to robot"
Assistant: "✅ Voice changed to ROBOT mode!"

You: "System report"
Assistant: "CPU: 45%, RAM: 8GB/16GB..."
         → Robotic voice perfect for system info!
```

### Example 4: Speed Test
```
You: "Bhai, speak super fast"
Assistant: "✅ Voice speed set to SUPER FAST (300 wpm)"

You: "Tell me the news"
Assistant: *Speaks news at 300 words per minute*
         → Super fast news update!
```

---

## 🎬 Voice Presets

The system has **8 voice presets** optimized for different uses:

| Preset | Voice | Speed | Best For |
|--------|-------|-------|----------|
| **male** | Male | 150 wpm | Professional use |
| **female** | Female | 150 wpm | Default, balanced |
| **robot** | Male | 180 wpm | System notifications |
| **chipmunk** | Female | 300 wpm | Fun, entertainment |
| **deep** | Male | 120 wpm | Dramatic reading |
| **funny** | Female | 200 wpm | Jokes, casual |
| **fast** | Female | 250 wpm | Quick updates |
| **slow** | Male | 100 wpm | Clear instructions |

---

## 🔧 Technical Details

### Voice Properties:
- **Rate**: Words per minute (80-300)
- **Volume**: 0-100%
- **Voice Index**: 0 (male) or 1 (female) on most systems

### Python API:
```python
from voice_assistant import VoiceAssistant

assistant = VoiceAssistant()

# Change voice
assistant.change_voice("chipmunk")

# Set speed
assistant.set_voice_speed("super fast")

# Get current voice info
print(assistant.get_current_voice())

# List all voices
print(assistant.list_voices())
```

---

## 🎮 Try the Demo

Test all voices with the demo script:

```bash
python test_voice_change.py
```

This will demo:
- ✅ All 8 voice presets
- ✅ All 6 speed settings
- ✅ Voice information display
- ✅ Live speaking examples

---

## 🎭 Fun Use Cases

### 1. **Storytelling Mode**
Use different voices for different characters!
- Narrator: Deep voice
- Hero: Male voice
- Villain: Robot voice
- Comic relief: Chipmunk voice

### 2. **Language Learning**
Slow down speech for better understanding:
```
"Bhai, speak very slow"
"Translate hello to Spanish"
```

### 3. **Entertainment**
Make jokes funnier with chipmunk voice:
```
"Bhai, change voice to chipmunk"
"Tell me a joke"
```

### 4. **Productivity**
Fast voice for quick updates:
```
"Bhai, speak super fast"
"System report"
```

### 5. **Accessibility**
Adjust speed for better comprehension:
```
"Bhai, speak slower"
```

---

## 📊 Voice Comparison

| Feature | Female | Male | Robot | Chipmunk | Deep |
|---------|--------|------|-------|----------|------|
| **Pitch** | Normal | Normal | Robotic | High | Low |
| **Speed** | 150 wpm | 150 wpm | 180 wpm | 300 wpm | 120 wpm |
| **Fun Level** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Professional** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ |
| **Clarity** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |

---

## 🎉 Best Combinations

### For Comedy:
```
"Bhai, change voice to chipmunk"
"Tell me a joke"
"Flip a coin"
```

### For News:
```
"Bhai, change voice to robot"
"Speak faster"
"Tech news"
```

### For Instructions:
```
"Bhai, change voice to male"
"Speak slower"
"Help"
```

### For Quick Updates:
```
"Bhai, change voice to fast"
"Battery status"
"System usage"
```

---

## 🐛 Troubleshooting

**Q: Voice doesn't change?**
- Check if multiple voices are installed on your system
- Run `assistant.list_voices()` to see available voices

**Q: Chipmunk voice is too fast?**
- Use: `"Bhai, speak slower"` to reduce speed

**Q: Want more voices?**
- Install additional TTS voices on your system
- Windows: Control Panel → Speech → Text-to-Speech
- Linux: Install `espeak` or `festival`
- Mac: System Preferences → Accessibility → Speech

---

## ✨ Summary

You now have **8 fun voice styles** + **6 speed settings** = **48 possible combinations!**

**Quick Reference:**
```
🎤 Voice Styles: male, female, robot, chipmunk, deep, funny, fast, slow
⚡ Speeds: very slow, slow, normal, fast, very fast, super fast
📋 Info: list voices, current voice
```

**Try them all and find your favorite!** 🎊

Say **"Bhai, change voice to chipmunk"** for instant fun! 🐿️
