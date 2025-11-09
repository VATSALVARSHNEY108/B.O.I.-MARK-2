# Custom Hand Gesture Training

This directory stores your custom-trained hand gesture models.

## Quick Start

### 1. Train Custom Gestures

Run the training utility:
```bash
python train_hand_gestures.py
```

### 2. Follow the Interactive Menu

1. **Capture gesture samples** - Record 50+ samples per gesture
2. **Train the model** - Build the ML classifier
3. **List gestures** - View your trained gestures

### 3. Test Your Gestures

Run the gesture demo:
```bash
python demo_opencv_hand_gesture.py
```

Or use the GUI app which automatically loads your trained model.

## Directory Structure

```
biometric_data/hands/
├── models/                    # Trained model files (auto-generated)
│   ├── gesture_model.pkl      # SVM classifier
│   ├── gesture_scaler.pkl     # Feature scaler
│   ├── gesture_labels.pkl     # Gesture label mapping
│   └── custom_gestures.json   # Model metadata
├── <GESTURE_NAME_1>/          # Your custom gesture
│   └── samples/               # Training images
│       ├── sample_000.png
│       ├── sample_001.png
│       └── ...
├── <GESTURE_NAME_2>/
│   └── samples/
└── README.md (this file)
```

## Tips for Good Gesture Training

1. **Lighting** - Use good, consistent lighting
2. **Hand Position** - Keep your hand clearly visible in the frame
3. **Steady Gesture** - Hold the gesture steady while capturing
4. **Enough Samples** - Capture 50+ samples per gesture for best accuracy
5. **Variety** - Slightly vary hand position/angle during capture
6. **Clear Background** - Use a plain background if possible

## Available Gesture Types

Your system supports 3 types of gestures:

### 1. MediaPipe Pretrained (7 gestures)
- ✅ NO training required
- Works instantly
- Gestures: Open_Palm, Closed_Fist, Thumbs_Up, Thumbs_Down, Pointing_Up, Victory, ILoveYou

### 2. Custom Trained (unlimited gestures)
- ⚙️ Requires training (this directory)
- Train any gesture you want
- Examples: OK_SIGN, CALL_ME, ROCK_ON, WAVE, POINTING_LEFT, etc.

### 3. Hardcoded Finger-Counting (4 gestures)
- ✅ Always available as fallback
- Gestures: OPEN_PALM, FIST, PEACE_SIGN, THUMBS_UP

## Troubleshooting

**No gestures recognized?**
- Check if model files exist in `models/` directory
- Retrain the model if files are missing
- Ensure camera access is available

**Low accuracy?**
- Capture more samples (100+ recommended)
- Use better lighting
- Train with consistent hand positioning

**Camera not working?**
- This requires a local Windows/Mac/Linux machine with camera
- Replit environment doesn't support camera access
