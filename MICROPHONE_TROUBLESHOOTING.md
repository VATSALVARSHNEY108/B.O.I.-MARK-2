# 🎤 MICROPHONE TROUBLESHOOTING GUIDE

## ✅ Good News!

Your diagnostic shows:
- ✅ Microphone is accessible (working connection)
- ✅ PyAudio is installed correctly
- ✅ SpeechRecognition is working
- ❌ **BUT: No sound is being detected**

---

## 🔧 THE PROBLEM

Your microphone is **connected and recognized**, but it's **not picking up your voice**. This usually means:

1. **Microphone is MUTED** (most common)
2. **Microphone volume too LOW**
3. **Wrong microphone selected** (if you have multiple)
4. **You're not speaking loud/close enough**

---

## 🛠️ QUICK FIXES (Try in Order)

### Fix 1: Check if Microphone is Muted

#### Windows:
1. Right-click **speaker icon** in taskbar
2. Click **"Open Sound settings"**
3. Scroll to **"Input"**
4. Make sure your microphone is selected
5. Check the **volume slider** is NOT at 0
6. Click **"Device properties"**
7. Make sure **"Disable"** is NOT checked

#### Mac:
1. Click **Apple menu** → **System Preferences**
2. Click **Sound** → **Input** tab
3. Select your microphone
4. Drag **Input volume** slider to the right (at least 50%)
5. Check **Input level** - speak and see if bars move

#### Linux:
```bash
# Check if microphone is muted
amixer get Capture

# Unmute microphone
amixer set Capture unmute

# Increase volume to 80%
amixer set Capture 80%
```

---

### Fix 2: Test Audio Levels (Use My Tool!)

I created a tool that shows **real-time audio levels**:

```bash
python microphone_level_test.py
```

**What it does:**
- Shows visual bars of your microphone input
- Tells you if volume is loud enough
- Helps you pick the right microphone

**How to use:**
1. Run the command above
2. Press Enter (or select microphone number)
3. **SPEAK LOUDLY** and watch the bars
4. If bars stay at 0 → microphone is muted or broken
5. If bars are small → increase volume in settings
6. If bars are big → microphone is working!

---

### Fix 3: Select Correct Microphone

If you have **multiple microphones** (webcam, headset, built-in):

1. **List all microphones:**
   ```bash
   python -c "import speech_recognition as sr; [print(f'[{i}] {name}') for i, name in enumerate(sr.Microphone.list_microphone_names())]"
   ```

2. **Test each one:**
   ```bash
   python microphone_level_test.py
   ```
   Enter the number of each microphone to test

3. **Set default in system settings:**
   - Windows: Sound Settings → Input → Choose device
   - Mac: System Preferences → Sound → Input → Select device
   - Linux: `pavucontrol` → Input Devices → Set as fallback

---

### Fix 4: Increase Microphone Boost

#### Windows:
1. Right-click speaker icon → **"Open Sound settings"**
2. Scroll to Input → **"Device properties"**
3. Click **"Additional device properties"**
4. Go to **"Levels"** tab
5. Set **Microphone** to 100
6. Set **Microphone Boost** to +20dB or +30dB
7. Click **Apply** and **OK**

#### Mac:
1. System Preferences → **Sound** → **Input**
2. Drag **Input volume** all the way to the right
3. Some Macs don't have boost - use external mic instead

---

### Fix 5: Test with Ultra-Sensitive Settings

Create a test file:

```python
# test_sensitive_mic.py
import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.energy_threshold = 50  # ULTRA sensitive
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 0.3

with sr.Microphone() as source:
    print("🎤 Speak NOW (10 seconds)...")
    recognizer.adjust_for_ambient_noise(source, duration=0.5)
    audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
    
    print("Processing...")
    text = recognizer.recognize_google(audio)
    print(f"You said: {text}")
```

Run with: `python test_sensitive_mic.py`

---

## 🔍 DIAGNOSTIC CHECKLIST

Run through this checklist:

- [ ] Microphone is **not muted** in system settings
- [ ] Microphone volume is at **50% or higher**
- [ ] Correct microphone is **selected as default**
- [ ] Speaking **loud and clear** (not whispering)
- [ ] Close to microphone (within **30cm / 1 foot**)
- [ ] No background noise interfering
- [ ] Tested with `python microphone_level_test.py` and saw bars move

---

## 🆘 STILL NOT WORKING?

### Test with System's Built-in Voice Recorder

**Windows:**
1. Open **Voice Recorder** app
2. Click **Record**
3. Speak for 5 seconds
4. Click **Stop**
5. Play it back - do you hear your voice?

**Mac:**
1. Open **QuickTime Player**
2. File → **New Audio Recording**
3. Click **Record** button
4. Speak for 5 seconds
5. Click **Stop** and play back

**Linux:**
```bash
# Record 5 seconds
arecord -d 5 test.wav

# Play it back
aplay test.wav
```

**If system recorder ALSO doesn't work:**
- Your microphone is broken or not connected
- Try a different microphone or headset
- Check USB connection (if using USB mic)

**If system recorder WORKS but Python doesn't:**
- Run: `pip uninstall pyaudio && pip install pyaudio`
- Make sure you're using the same microphone in both

---

## 💡 COMMON SOLUTIONS SUMMARY

| Problem | Solution |
|---------|----------|
| Muted mic | Unmute in Sound Settings |
| Volume too low | Increase to 80-100% + boost |
| Wrong mic | Select correct one as default |
| Not loud enough | Speak louder, get closer |
| Multiple mics | Test each with level tester |
| Headset not working | Make sure it's plugged in fully |

---

## 🎯 NEXT STEPS

1. **Run the level tester:**
   ```bash
   python microphone_level_test.py
   ```

2. **Watch for bars** - if you see bars moving, mic is working!

3. **If bars don't move:**
   - Check system settings (mute, volume)
   - Test with system voice recorder
   - Try different microphone

4. **Once bars are moving:**
   - Run `python gui_voice_diagnostic.py` again
   - Should work this time!

---

## 📞 Need More Help?

Run this and send me the output:

```bash
python microphone_level_test.py
```

Let me know:
1. Do you see any bars moving when you speak?
2. What's the energy threshold number?
3. What's the highest level number you see?

I'll help you debug from there!
