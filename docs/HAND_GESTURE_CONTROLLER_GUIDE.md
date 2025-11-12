# Hand Gesture Mouse Controller - Complete Guide

## Overview

The **Hand Gesture Mouse Controller** transforms your webcam into a touchless computer interface. Control your mouse cursor, click, scroll, and more using natural hand gestures detected in real-time.

## 🎯 Features

### Gesture Controls
- **Cursor Movement** - Move mouse with index finger
- **Left Click** - Pinch index finger and thumb together
- **Right Click** - Extend only pinky finger
- **Scroll** - Open palm (all fingers up) and move hand
- **Drag & Drop** - Close fist to hold, open to release
- **Volume Control** - Thumb + index distance controls volume

### Technical Features
- Real-time hand tracking with MediaPipe
- Smooth cursor movement with jitter reduction
- Multi-gesture recognition
- 30-60 FPS performance on CPU
- Statistics tracking
- Adjustable sensitivity and smoothing

## 📦 Installation

### Required Dependencies

```bash
pip install opencv-python mediapipe pyautogui numpy
```

### Optional (for volume control)

```bash
pip install pycaw comtypes
```

### Complete Installation

```bash
# All required packages
pip install opencv-python==4.8.1.78 mediapipe==0.10.8 pyautogui==0.9.54 numpy==1.24.3

# Optional for Windows volume control
pip install pycaw comtypes
```

## 🚀 Quick Start

### Basic Usage

```python
from modules.automation.hand_gesture_controller import HandGestureController

# Create controller
controller = HandGestureController()

# Initialize
result = controller.initialize()

if result["success"]:
    # Start (blocks until 'q' pressed)
    controller.start(show_video=True)
else:
    print(f"Error: {result['error']}")
```

### Run Demo

```bash
# Interactive menu
python demo_hand_gesture_controller.py

# Quick start
python demo_hand_gesture_controller.py --quick

# Run tests
python demo_hand_gesture_controller.py --test

# View guide
python demo_hand_gesture_controller.py --guide
```

## ✋ Gesture Guide

### 1. Cursor Movement
**Gesture**: Index finger up (alone) OR Index + Middle fingers up

**How it works**:
- Extend your index finger
- Move your hand to control cursor position
- Cursor follows your fingertip with smooth tracking

**Tips**:
- Keep hand steady for precision
- Move slowly for fine control
- Use larger movements for fast navigation

---

### 2. Left Click
**Gesture**: Pinch index finger and thumb together

**How it works**:
- Bring index fingertip and thumb tip close together
- When distance < threshold, click is triggered
- Automatic cooldown prevents double-clicks

**Tips**:
- Quick pinch for single click
- Hold pinch briefly for stability
- Release fully before next click

---

### 3. Scroll Mode
**Gesture**: All 5 fingers extended (open palm)

**How it works**:
- Open your hand completely (all fingers up)
- Move hand up → Scroll up
- Move hand down → Scroll down
- Scroll speed based on movement speed

**Tips**:
- Larger movements = faster scrolling
- Keep hand flat and stable
- Smooth movements for precise scrolling

---

### 4. Volume Control
**Gesture**: Thumb + Index finger up (other 3 down)

**How it works**:
- Extend only thumb and index finger
- Distance between them controls volume
- Close together = quiet
- Far apart = loud

**Requirements**:
- Windows: Requires `pycaw` package
- Mac/Linux: Alternative implementation needed

---

### 5. Right Click
**Gesture**: Only pinky finger up (all others down)

**How it works**:
- Extend only your pinky finger
- Keep other fingers closed
- Triggers right-click action

**Tips**:
- Hold gesture briefly
- Clear finger position for detection

---

### 6. Drag and Drop
**Gesture**: Closed fist (all fingers down)

**How it works**:
- Make a fist to "grab" (mouse down)
- Move hand while maintaining fist
- Open hand to "release" (mouse up)

**Use cases**:
- Dragging files
- Selecting text
- Moving windows
- Drawing applications

---

## ⚙️ Configuration

### Initialization Options

```python
controller.initialize(
    camera_id=0,                    # Webcam index (0=default)
    detection_confidence=0.7,       # Hand detection threshold (0.0-1.0)
    tracking_confidence=0.7         # Hand tracking threshold (0.0-1.0)
)
```

### Adjustable Parameters

```python
# Cursor smoothing (higher = smoother but slower response)
controller.smoothing = 5  # Default: 5, Range: 1-10

# Click cooldown (frames between clicks)
controller.cooldown_frames = 10  # Default: 10

# Screen mapping
controller.screen_width   # Auto-detected
controller.screen_height  # Auto-detected
```

## 📊 Statistics

Get usage statistics:

```python
stats = controller.get_stats()

print(f"Total gestures: {stats['total_gestures']}")
print(f"Clicks: {stats['clicks']}")
print(f"Scrolls: {stats['scrolls']}")
print(f"Drags: {stats['drags']}")
```

## 🎮 Keyboard Controls

When running:
- **'Q'** - Quit application
- **'S'** - Toggle statistics display

## 💡 Tips for Best Results

### Lighting
- ✅ Well-lit room (bright, even lighting)
- ✅ Face camera toward light source
- ❌ Avoid backlighting
- ❌ Avoid harsh shadows

### Background
- ✅ Plain, solid-color background
- ✅ Contrasting with hand color
- ❌ Busy patterns or cluttered background
- ❌ Similar color to skin tone

### Hand Position
- ✅ Hand centered in camera view
- ✅ Palm facing camera
- ✅ 1-2 feet from camera
- ✅ Keep hand within frame
- ❌ Too close (fills entire frame)
- ❌ Too far (hand too small)

### Movement
- ✅ Smooth, deliberate gestures
- ✅ Clear finger positions
- ✅ Hold gestures briefly for recognition
- ❌ Rapid, jerky movements
- ❌ Ambiguous finger positions

## 🔧 Troubleshooting

### Hand Not Detected

**Symptoms**: No landmarks drawn, "No Hand Detected" message

**Solutions**:
1. Improve lighting
2. Lower `detection_confidence` to 0.5
3. Use plain background
4. Move hand closer to camera
5. Ensure palm faces camera

```python
# Lower detection threshold
controller.initialize(detection_confidence=0.5)
```

---

### Jittery Cursor

**Symptoms**: Cursor jumps around, not smooth

**Solutions**:
1. Increase smoothing factor
2. Improve lighting consistency
3. Keep hand more stable
4. Increase tracking confidence

```python
# Increase smoothing
controller.smoothing = 8  # Higher = smoother
```

---

### False Clicks

**Symptoms**: Unintended clicks happening

**Solutions**:
1. Increase click threshold
2. Increase cooldown frames
3. Make more deliberate pinch gestures

```python
# Increase cooldown
controller.cooldown_frames = 15
```

---

### Slow Performance

**Symptoms**: Low FPS, laggy response

**Solutions**:
1. Close other applications
2. Reduce camera resolution
3. Use `model_complexity=0` (faster, less accurate)

```python
# In initialization code, modify:
self.hands = self.mp_hands.Hands(
    model_complexity=0,  # 0=lite, 1=full
    max_num_hands=1
)
```

---

### Gesture Not Recognized

**Symptoms**: Specific gesture not triggering

**Solutions**:
1. Check finger positions clearly match description
2. Hold gesture for 1-2 seconds
3. Ensure good lighting
4. Try slightly different hand angle

---

## 🔌 Integration Examples

### Voice Command Integration

```python
def voice_command_handler(command):
    if "start gesture control" in command:
        controller = HandGestureController()
        controller.initialize()
        controller.start()
```

### Background Thread

```python
import threading

def run_gesture_control():
    controller = HandGestureController()
    controller.initialize()
    controller.start()

# Run in background
thread = threading.Thread(target=run_gesture_control, daemon=True)
thread.start()
```

### Custom Gesture Actions

```python
# Extend the HandGestureController class
class CustomGestureController(HandGestureController):
    
    def recognize_gesture(self, fingers):
        if fingers == [1, 0, 0, 0, 1]:  # Thumb + Pinky
            return "custom_action"
        return super().recognize_gesture(fingers)
    
    def process_custom_action(self):
        # Your custom action here
        print("Custom gesture triggered!")
```

## 📈 Performance Benchmarks

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | Dual-core 2.0 GHz | Quad-core 2.5+ GHz |
| RAM | 4 GB | 8 GB+ |
| Camera | 480p @ 15 fps | 720p @ 30 fps |
| OS | Windows 10, macOS 10.14, Ubuntu 18.04+ | Latest versions |

### Expected Performance

| Hardware | FPS | Latency |
|----------|-----|---------|
| Budget laptop | 20-30 | 50-80ms |
| Mid-range laptop | 30-45 | 30-50ms |
| High-end desktop | 45-60 | 20-40ms |

## 🔒 Privacy & Security

- ✅ All processing done locally (no cloud)
- ✅ No data stored or transmitted
- ✅ Camera access only when running
- ✅ Can run fully offline
- ✅ Open source implementation

## 🌐 Platform Support

### Windows
- ✅ Full support
- ✅ Volume control (with pycaw)
- ✅ All gestures work

### macOS
- ✅ Full support (except volume)
- ⚠️ Requires accessibility permissions for mouse control
- ✅ All cursor gestures work

### Linux
- ✅ Full support (except volume)
- ✅ Works on Ubuntu, Fedora, etc.
- ✅ All cursor gestures work

## 🎓 Advanced Topics

### MediaPipe Hand Landmarks

21 hand landmarks detected:
- 0: Wrist
- 1-4: Thumb (CMC, MCP, IP, TIP)
- 5-8: Index (MCP, PIP, DIP, TIP)
- 9-12: Middle (MCP, PIP, DIP, TIP)
- 13-16: Ring (MCP, PIP, DIP, TIP)
- 17-20: Pinky (MCP, PIP, DIP, TIP)

### Coordinate System

- X: 0.0 (left) to 1.0 (right)
- Y: 0.0 (top) to 1.0 (bottom)
- Z: Relative depth

### Smoothing Algorithm

Exponential moving average:
```python
cursor_x = prev_x + (raw_x - prev_x) / smoothing
```

## 📚 Resources

- **MediaPipe Docs**: https://developers.google.com/mediapipe
- **PyAutoGUI Docs**: https://pyautogui.readthedocs.io
- **OpenCV Docs**: https://docs.opencv.org

## 🐛 Known Issues

1. **Volume control Windows only**: Mac/Linux need different implementation
2. **Accessibility permissions**: macOS requires explicit permission
3. **Multiple monitors**: Cursor may behave unexpectedly across screens
4. **High DPI**: Some scaling issues on 4K displays

## 🔄 Version History

- **v1.0.0** (November 2025) - Initial release
  - 7 gesture types
  - Real-time tracking
  - Statistics system
  - Multi-platform support

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Module**: `modules/automation/hand_gesture_controller.py`
