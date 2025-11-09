# Hand Gesture Controls - Complete Guide

## Overview
Control your computer hands-free using natural hand gestures! This system recognizes various hand signs and converts them into system actions like locking the screen, taking screenshots, controlling media, and much more.

---

## Available Gestures (MVP - Static Gestures)

### 🎤 Voice Control Gestures

#### 👋 **OPEN PALM** - Activate Voice Listening
- **How**: Show your open palm (all 5 fingers extended)
- **Action**: Starts voice command listening
- **Feedback**: "Listening"
- **Cooldown**: 2 seconds

#### ✊ **FIST** - Stop Voice Listening  
- **How**: Close your hand into a fist (all fingers down)
- **Action**: Stops voice listening
- **Cooldown**: 1 second

---

### 📸 Screenshot & Media

#### ✌️ **PEACE SIGN** (V Sign) - Take Screenshot
- **How**: Show 2 fingers up (index + middle)
- **Action**: Captures a screenshot
- **Feedback**: "Screenshot taken"
- **Cooldown**: 2 seconds

#### ✌️✌️ **TWO PEACE SIGNS** - Supreme Leader Greeting
- **How**: Show V signs with BOTH hands simultaneously
- **Action**: Triggers random greeting like "Supreme leader, welcome!"
- **Cooldown**: 3 seconds
- **Note**: Random greetings that don't repeat consecutively

---

### 👍👎 Confirmation Gestures

#### 👍 **THUMBS UP** - Confirm/Approve
- **How**: Thumb up, other fingers down
- **Action**: Confirmation signal
- **Feedback**: "Confirmed"
- **Cooldown**: 1 second

#### 👎 **THUMBS DOWN** - Reject/Decline
- **How**: Thumb down, other fingers down
- **Action**: Rejection signal
- **Feedback**: "Rejected"
- **Cooldown**: 1 second

---

### 🪟 Window Management

#### 🖐️ **THREE FINGERS** - Minimize Window
- **How**: Hold up 3 fingers (index + middle + ring)
- **Action**: Minimizes current active window
- **Feedback**: "Minimized"
- **Cooldown**: 1 second
- **Shortcut**: Windows/Super + Down

#### 🖐️ **FOUR FINGERS** - Maximize Window
- **How**: Hold up 4 fingers (all except thumb)
- **Action**: Maximizes current active window  
- **Feedback**: "Maximized"
- **Cooldown**: 1 second
- **Shortcut**: Windows/Super + Up

#### 👌 **OK SIGN** - Close Window
- **How**: Make circle with thumb + index, other fingers up
- **Action**: Closes current active window
- **Feedback**: "Closing window"
- **Cooldown**: 2 seconds
- **Shortcut**: Alt + F4 (Windows) / Cmd + W (Mac)

---

### 🎵 Media Control

#### 🤏 **PINCH** - Play/Pause Media
- **How**: Bring thumb and index finger together
- **Action**: Toggles play/pause for music/video
- **Cooldown**: 1 second

#### 👉 **POINTING RIGHT** - Next Track
- **How**: Point index finger to the right
- **Action**: Skip to next track/video
- **Feedback**: "Next"
- **Cooldown**: 1 second

#### 👈 **POINTING LEFT** - Previous Track  
- **How**: Point index finger to the left
- **Action**: Go to previous track/video
- **Feedback**: "Previous"
- **Cooldown**: 1 second

---

### 🔊 Volume Control

#### ☝️ **POINTING UP** - Volume Up
- **How**: Point index finger upward
- **Action**: Increases system volume by 5%
- **Cooldown**: 0.5 seconds

#### 👇 **POINTING DOWN** - Volume Down
- **How**: Point index finger downward  
- **Action**: Decreases system volume by 5%
- **Cooldown**: 0.5 seconds

---

### 🔒 System Control

#### 🤚 **PALM LEFT** - Lock Screen
- **How**: Show palm facing to the left
- **Action**: Locks your computer screen
- **Feedback**: "Locking screen"
- **Cooldown**: 3 seconds

---

## Planned Gestures (Coming Soon - Motion Based)

These gestures require motion tracking and will be added in a future update:

- **SWIPE LEFT** - Switch to left workspace/virtual desktop
- **SWIPE RIGHT** - Switch to right workspace/virtual desktop  
- **CIRCLE MOTION** - Start/stop screen recording

---

## Configuration

### Gesture Settings
Located in `config/gesture_actions.json`:

```json
{
  "gestures": {
    "OPEN_PALM": {
      "action": "voice_listen",
      "cooldown": 2,
      "priority": 10,
      "enabled": true
    }
  },
  "settings": {
    "enable_voice_feedback": true,
    "confidence_threshold": 0.7,
    "global_cooldown": 0.3
  }
}
```

### Customization
You can customize:
- **Cooldown times**: How long before a gesture can be repeated
- **Voice feedback**: Enable/disable spoken confirmations
- **Priority**: Which gesture takes precedence if multiple detected
- **Enable/Disable**: Turn specific gestures on/off

---

## Tips for Best Results

### Lighting & Background
- ✅ Use good lighting (front-lit, not backlit)
- ✅ Plain background (solid color wall)
- ❌ Avoid busy patterns or cluttered backgrounds
- ❌ Avoid backlighting (window behind you)

### Hand Position
- ✅ Keep hand 1-2 feet from camera
- ✅ Hand centered in camera frame
- ✅ Palm facing camera
- ✅ Make gestures deliberately (not too fast)

### Camera Setup
- ✅ Position camera at eye level
- ✅ Clean camera lens
- ✅ Use built-in webcam or USB camera
- ✅ 30-60 FPS for best tracking

---

## How It Works

### Detection Pipeline
1. **Camera Capture**: Webcam captures your hand movements
2. **Hand Detection**: OpenCV detects skin color and hand contours
3. **Gesture Recognition**: Analyzes finger patterns and positions
4. **Action Dispatch**: Maps gesture to configured action
5. **Cooldown Check**: Prevents accidental repeated triggers
6. **Action Execution**: Performs the system action
7. **Voice Feedback**: Optional spoken confirmation

### Modules
- **opencv_hand_gesture_detector.py**: Detects hand gestures
- **gesture_action_dispatcher.py**: Routes gestures to actions
- **window_control_helper.py**: Window management operations
- **media_control_helper.py**: Media playback control
- **system_control.py**: System-level operations

---

## Troubleshooting

### Gesture Not Detected
- Check lighting (too dark/too bright?)
- Ensure hand is in camera view
- Make gesture more deliberate
- Check if gesture is enabled in config

### Wrong Action Triggered
- Make gesture more distinct
- Adjust cooldown times in config
- Ensure proper hand orientation

### No Voice Feedback
- Check `enable_voice_feedback` in settings
- Verify speakers/audio output working
- Some gestures have `voice_feedback: null` intentionally

### High False Positives
- Increase `confidence_threshold` in settings
- Increase `cooldown` for specific gestures
- Improve lighting and background

---

## Statistics & Monitoring

Track your gesture usage:
```python
from modules.automation.gesture_action_dispatcher import GestureActionDispatcher

dispatcher = GestureActionDispatcher()
stats = dispatcher.get_stats()

print(f"Total gestures detected: {stats['total_gestures']}")
print(f"Actions executed: {stats['actions_executed']}")
print(f"Cooldown blocks: {stats['cooldown_blocked']}")
```

---

## Platform Compatibility

| Feature | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Voice Control | ✅ | ✅ | ✅ |
| Screenshots | ✅ | ✅ | ✅ |
| Window Control | ✅ | ✅ | ✅ |
| Media Control | ✅ | ✅ | ✅ |
| Volume Control | ✅ | ✅ | ✅ |
| Lock Screen | ✅ | ✅ | ✅ |

---

## Safety & Privacy

- ✅ All processing is done **locally** on your computer
- ✅ No camera data is sent to the internet
- ✅ No recordings are stored unless you use screenshot feature
- ✅ You can disable any gesture anytime in the config
- ✅ Camera access is only when gesture detection is active

---

## Quick Reference Card

| Gesture | Fingers | Action |
|---------|---------|--------|
| 👋 Open Palm | 5 up | Voice Listen |
| ✊ Fist | 0 up | Stop Listen |
| 👍 Thumbs Up | Thumb only | Confirm |
| 👎 Thumbs Down | Thumb down | Reject |
| ✌️ Peace (V) | 2 up | Screenshot |
| ✌️✌️ Two Vs | Both hands | Greeting |
| 🖐️ Three Fingers | 3 up | Minimize |
| 🖐️ Four Fingers | 4 up | Maximize |
| 👌 OK Sign | Circle | Close Window |
| 🤏 Pinch | Thumb+Index | Play/Pause |
| 👉 Point Right | Index right | Next Track |
| 👈 Point Left | Index left | Previous |
| ☝️ Point Up | Index up | Volume Up |
| 👇 Point Down | Index down | Volume Down |
| 🤚 Palm Left | Palm sideways | Lock Screen |

---

## Getting Started

1. **Start the gesture detector**:
   ```bash
   python demo_hand_gesture_controller.py --quick
   ```

2. **Position yourself**: Sit facing the camera with good lighting

3. **Test basic gestures**: Try open palm and fist first

4. **Explore more**: Gradually try other gestures

5. **Customize**: Edit `config/gesture_actions.json` to your liking

---

## Support & Feedback

If you encounter issues or have suggestions for new gestures, please provide feedback!

**Created by**: Vatsal Varshney  
**Version**: 1.0 MVP (Static Gestures)  
**Last Updated**: November 2025
