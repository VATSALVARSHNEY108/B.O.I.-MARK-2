# OpenCV Hand Gesture & Face Detection Guide

## Overview

VATSAL AI now includes an **enhanced hand gesture and face detection system** using pure OpenCV that works everywhere - no MediaPipe required!

## Features

### ✅ What's Included

1. **Face Detection**
   - Uses OpenCV Haar Cascade
   - Real-time face tracking
   - Automatic user greeting when face detected
   - Name display overlay

2. **Hand Gesture Recognition**
   - Skin color-based hand detection
   - Contour analysis for gesture recognition
   - Supported gestures:
     - 👋 **OPEN PALM** - Activates voice listening
     - ✊ **FIST** - Stop/Cancel action
   - Real-time hand tracking with visual feedback

3. **Voice Integration**
   - Automatic voice activation with open palm gesture
   - Works seamlessly with VATSAL voice commander
   - Visual and audio feedback

4. **Statistics Tracking**
   - Faces detected count
   - Gestures detected count
   - Greetings given count
   - Open palm detections
   - Fist detections

## How It Works

### Detection Methods

#### Face Detection (Haar Cascade)
- Uses pre-trained Haar Cascade classifier
- Detects faces at 30-60 FPS
- Accurate in various lighting conditions
- Green rectangle drawn around detected face

#### Hand Detection (Skin Color + Contours)
The hand gesture detection uses a multi-step process:

1. **Color Segmentation**: Converts frame to HSV and detects skin-colored regions
2. **Noise Reduction**: Applies morphological operations to clean the mask
3. **Contour Extraction**: Finds the largest contour (the hand)
4. **Shape Analysis**: Uses convexity defects to count fingers
5. **Gesture Classification**: Determines gesture based on finger count

### Gesture Recognition

| Fingers Extended | Gesture | Action |
|-----------------|---------|--------|
| 4-5 fingers | OPEN PALM 👋 | Activate voice listening |
| 0-1 fingers | FIST ✊ | Stop/Cancel |
| 2-3 fingers | PARTIAL ✌️ | Detected but no action |

## Usage

### Method 1: Run Standalone Demo

```bash
python demo_opencv_hand_gesture.py
```

This will:
- Open your webcam
- Start detecting faces and hand gestures
- Display real-time video with overlays
- Show statistics when you quit

### Method 2: Use in Main GUI

The OpenCV detector is automatically integrated into the main VATSAL GUI:

```bash
streamlit run vatsal.py --server.port=5000 --server.address=0.0.0.0 --server.headless=true
```

In the GUI:
1. Navigate to the **Automation** section
2. Click the **Face & Gesture** button (👤)
3. The detector will start automatically

### Method 3: Programmatic Usage

```python
from modules.automation.opencv_hand_gesture_detector import OpenCVHandGestureDetector

# Create detector
detector = OpenCVHandGestureDetector()

# Set callbacks (optional)
def on_face_detected():
    print("Face detected!")

def on_gesture_detected(command):
    print(f"Gesture command: {command}")

detector.set_face_callback(on_face_detected)
detector.set_gesture_callback(on_gesture_detected)

# Start detection
result = detector.start(camera_index=0)
if result['success']:
    print("Detector started!")
    
    # ... do other work ...
    
    # Stop when done
    detector.stop()
    
    # Get statistics
    stats = detector.get_stats()
    print(stats)
```

## Integration with VATSAL Voice Commander

When integrated with the voice commander, the detector provides a hands-free experience:

1. **Face Detected** → System greets you ("Hello Vatsal", "Yes sir", etc.)
2. **Show Open Palm** → System says "I'm listening" and activates microphone
3. **Speak Command** → System processes your voice command
4. **Show Fist** → (Optional) Cancel/Stop action

Example workflow:
```
You: [Face appears on camera]
VATSAL: "Hello Vatsal"
You: [Show open palm]
VATSAL: "I'm listening"
You: "Open Chrome browser"
VATSAL: [Opens Chrome and confirms]
```

## Configuration

### Adjustable Parameters

You can modify these in the `OpenCVHandGestureDetector` class:

```python
# In modules/automation/opencv_hand_gesture_detector.py

# Skin color range (HSV)
self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)

# Hand size limits (pixels²)
self.min_hand_area = 5000    # Minimum area to detect as hand
self.max_hand_area = 50000   # Maximum area to detect as hand

# Timing
self.greeting_cooldown = 10  # Seconds between greetings
self.gesture_cooldown = 2    # Seconds between gesture activations
```

### Camera Settings

```python
# Default camera (usually 0)
detector.start(camera_index=0)

# External USB camera (usually 1)
detector.start(camera_index=1)

# IP camera
detector.start(camera_index="rtsp://192.168.1.100:8080/video")
```

## Advantages Over MediaPipe

| Feature | OpenCV Detector | MediaPipe |
|---------|----------------|-----------|
| **Dependencies** | Minimal (just OpenCV) | Requires MediaPipe + protobuf |
| **Python 3.13 Support** | ✅ Yes | ❌ No (Windows) |
| **Headless Environments** | ✅ Works | ⚠️ Limited |
| **Performance** | ~30-60 FPS | ~30-60 FPS |
| **Accuracy** | Good | Excellent |
| **Setup Complexity** | Simple | Complex |
| **File Size** | Small | Large (34MB+) |

## Troubleshooting

### Camera Not Opening

```python
# Check available cameras
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i} is available")
        cap.release()
```

### Poor Hand Detection

- **Improve lighting**: Ensure good, even lighting
- **Adjust skin color range**: Modify `lower_skin` and `upper_skin` values
- **Check hand size**: Ensure your hand is within min/max area limits
- **Clear background**: Avoid skin-colored objects in background

### Gestures Not Recognized

- **Show palm clearly**: Spread fingers wide for open palm
- **Close fist completely**: Curl all fingers for fist gesture
- **Hold for 1-2 seconds**: Give the system time to analyze
- **Check cooldown**: Wait 2 seconds between gestures

## Technical Details

### Dependencies
- OpenCV (cv2) - Computer vision operations
- NumPy - Array operations
- Threading - Background processing

### Performance
- **Frame Rate**: 30-60 FPS (depending on hardware)
- **Latency**: <100ms gesture recognition
- **CPU Usage**: 5-15% (single core)
- **Memory**: ~50-100MB

### Compatibility
- ✅ Windows (all Python versions)
- ✅ Linux (all Python versions)
- ✅ macOS (all Python versions)
- ✅ Replit (cloud environment)
- ✅ Docker containers
- ✅ Raspberry Pi

## Examples

### Example 1: Face Detection Only

```python
detector = OpenCVHandGestureDetector()
detector.start()

# Just detect faces, ignore gestures
while detector.is_running():
    time.sleep(0.1)
```

### Example 2: Custom Greeting

```python
def custom_greeting():
    print("Welcome back, boss!")
    # Play custom sound
    # Send notification
    # etc.

detector = OpenCVHandGestureDetector()
detector.set_face_callback(custom_greeting)
detector.start()
```

### Example 3: Gesture-Based Automation

```python
def handle_gesture(command):
    if "chrome" in command.lower():
        os.system("start chrome")
    elif "notepad" in command.lower():
        os.system("notepad")
    # etc.

detector = OpenCVHandGestureDetector()
detector.set_gesture_callback(handle_gesture)
detector.start()
```

## Future Enhancements

Planned improvements:
- [ ] More gesture types (peace sign, thumbs up, etc.)
- [ ] Multiple hand tracking
- [ ] Gesture customization via config file
- [ ] Machine learning-based gesture recognition
- [ ] 3D hand pose estimation
- [ ] Gesture macros and sequences

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Run the demo script to isolate issues
3. Check camera permissions and drivers
4. Ensure good lighting conditions

## License

Part of VATSAL AI Desktop Automation System
