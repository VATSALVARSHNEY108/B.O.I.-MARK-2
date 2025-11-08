# 👁️ Face Detection & Gesture Recognition Feature

## Overview

The Face & Gesture Assistant is an advanced computer vision feature for VATSAL that uses OpenCV and MediaPipe to:
- Detect your face and greet you by name ("Vatsal" or "Yes sir")
- Recognize hand gestures to activate voice listening mode
- Provide a hands-free, natural interaction experience

## Features

### 1. Face Detection
- **Technology**: OpenCV Haar Cascade Classifier
- **Capability**: Detects faces in real-time using your webcam
- **Greeting**: Automatically greets you when your face is detected
- **Cooldown**: 10-second cooldown between greetings to avoid repetition

### 2. Hand Gesture Recognition
- **Technology**: Google MediaPipe Hands
- **Gestures**: Detects OPEN PALM gesture (all fingers extended)
- **Action**: Triggers voice listening mode when you show an open palm
- **Integration**: Fully integrated with VATSAL's voice command system

### 3. Voice Integration
- Greetings are spoken using Text-to-Speech
- Voice commands detected via gesture are executed automatically
- Seamless integration with existing voice commander

## How to Use

### From GUI Application

1. **Start the GUI**
   ```bash
   python modules/core/gui_app.py
   ```

2. **Enable Face & Gesture Detection**
   - Click the 👤 button in the voice control section
   - The button will turn green (👁️) when active
   - A camera window will open showing the live feed

3. **Interact with the System**
   - Position your face in front of the camera
   - You'll see a green rectangle around your face with "Vatsal" label
   - VATSAL will greet you ("Yes sir", "Hello Vatsal", etc.)
   - Show an OPEN PALM gesture to activate voice listening
   - Speak your command after the system says "I'm listening"

4. **Stop Detection**
   - Click the 👁️ button again to stop
   - Or press 'q' in the camera window
   - You'll see session statistics (faces detected, greetings, gestures)

### Standalone Testing

You can test the face & gesture assistant independently:

```bash
python modules/automation/face_gesture_assistant.py
```

## Greetings

The system uses randomized greetings to feel more natural:
- "Yes sir"
- "Hello Vatsal"
- "I'm here Vatsal"
- "At your service sir"
- "Ready to assist Vatsal"

## Hand Gestures

### OPEN PALM (Listening Activation)
- Extend all five fingers
- Palm facing the camera
- Hold steady for recognition
- System will say "I'm listening" and wait for your voice command

### Future Gestures
The system is designed to support additional gestures:
- FIST: Could be used for pause/stop
- POINTING: Could be used for navigation
- THUMBS UP: Could be used for confirmation

## Technical Details

### Face Detection
```python
# Uses OpenCV's built-in Haar Cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Detection parameters
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(80, 80)
)
```

### Hand Landmark Detection
```python
# Uses MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
```

### Gesture Recognition Algorithm
The system analyzes 21 hand landmarks to determine:
1. Position of finger tips relative to wrist
2. Number of extended fingers
3. Hand orientation

## Camera Requirements

- **Webcam**: Built-in or USB webcam required
- **Resolution**: 640x480 (automatically set)
- **Lighting**: Good lighting improves face detection accuracy
- **Position**: Face the camera directly for best results

## Cooldowns

To prevent spamming and improve user experience:
- **Greeting Cooldown**: 10 seconds between greetings
- **Gesture Cooldown**: 3 seconds between gesture activations

## Statistics Tracking

The system tracks:
- `faces_detected`: Total number of times a face was detected
- `greetings_given`: Number of greetings spoken
- `gestures_detected`: Number of hand gestures recognized
- `running`: Current status (true/false)
- `face_detected`: Current face detection status

## Troubleshooting

### Camera Not Opening
```
Error: Could not access camera
```
**Solution**: 
- Check camera permissions
- Ensure no other application is using the camera
- Try a different camera index (default is 0)

### Face Not Detected
**Possible causes**:
- Poor lighting conditions
- Face not fully visible or too far from camera
- Camera angle too extreme

**Solutions**:
- Improve lighting
- Move closer to the camera
- Face the camera directly

### Gesture Not Recognized
**Possible causes**:
- Fingers not fully extended
- Hand too far from camera
- Hand moving too quickly

**Solutions**:
- Extend all fingers clearly
- Hold hand steady
- Move hand closer to camera

## Code Architecture

### Main Class: `FaceGestureAssistant`

**Key Methods**:
- `start(camera_index)`: Start detection
- `stop()`: Stop detection
- `set_gesture_callback(callback)`: Set callback for gesture events
- `set_face_callback(callback)`: Set callback for face detection events
- `get_stats()`: Get current statistics

**Private Methods**:
- `_detection_loop()`: Main detection loop (runs in thread)
- `_recognize_gesture(landmarks)`: Analyze hand landmarks
- `_greet_user()`: Speak greeting via TTS
- `_handle_listening_gesture()`: Activate voice listening

## Integration Points

### With Voice Commander
```python
# Initialize with voice commander
assistant = FaceGestureAssistant(voice_commander=voice_commander)

# Greeting uses voice commander's TTS
voice_commander.speak("Yes sir")

# Voice listening triggered by gesture
voice_commander.listen_once(timeout=5)
```

### With GUI Application
```python
# Initialize in GUI
self.face_gesture_assistant = FaceGestureAssistant(
    voice_commander=self.voice_commander
)

# Set callback for gesture commands
self.face_gesture_assistant.set_gesture_callback(
    self._handle_gesture_command
)

# Toggle on/off
self.face_gesture_assistant.start()
self.face_gesture_assistant.stop()
```

## Performance Considerations

- **CPU Usage**: Moderate (face detection + hand tracking)
- **Memory**: ~200-300 MB (MediaPipe models)
- **Frame Rate**: ~30 FPS on modern systems
- **Latency**: <100ms for gesture recognition

## Future Enhancements

1. **Face Recognition**: Identify different users by face
2. **Custom Gestures**: Train custom gesture models
3. **Multi-Hand Support**: Recognize gestures with both hands
4. **Emotion Detection**: Detect user emotions from facial expressions
5. **Gaze Tracking**: Determine where user is looking
6. **Distance Estimation**: Adjust behavior based on user distance

## Dependencies

- `opencv-python` (cv2): Face detection and video capture
- `mediapipe`: Hand landmark detection
- `numpy`: Array operations
- `pyttsx3`: Text-to-speech (via voice_commander)
- `speechrecognition`: Voice recognition (via voice_commander)

## Example Usage

### Standalone Script
```python
from modules.automation.face_gesture_assistant import FaceGestureAssistant
from modules.voice.voice_commander import VoiceCommander

# Initialize
voice = VoiceCommander()
assistant = FaceGestureAssistant(voice_commander=voice)

# Set callback
def handle_command(command):
    print(f"Received command: {command}")

assistant.set_gesture_callback(handle_command)

# Start detection
result = assistant.start()
print(result['message'])

# Keep running
try:
    while assistant.is_running():
        time.sleep(1)
except KeyboardInterrupt:
    assistant.stop()
```

## Conclusion

The Face & Gesture Assistant brings natural, hands-free interaction to VATSAL. With computer vision-powered face detection and gesture recognition, you can now interact with your AI assistant more intuitively than ever before!

---

**Happy Face Detection! 👁️🤖✨**
