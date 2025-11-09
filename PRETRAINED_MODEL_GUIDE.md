# Pre-trained Hand Gesture Models for VATSAL AI

## Quick Start - No Training Required!

Your system already comes with **7 MediaPipe gestures** that work instantly with NO training:

✅ **MediaPipe Pretrained Gestures** (Ready to use now!):
- Open_Palm
- Closed_Fist  
- Thumbs_Up
- Thumbs_Down
- Pointing_Up
- Victory (Peace sign)
- ILoveYou (Rock-n-roll sign)

### How to Use MediaPipe Gestures

Just run the gesture detector - they work immediately!

```bash
python demo_opencv_hand_gesture.py
```

---

## Custom Trained Gestures (For Unlimited Gestures)

Want to add your own custom gestures like OK_SIGN, CALL_ME, WAVE, etc.?

### Option 1: Train Your Own (Recommended)

```bash
python train_hand_gestures.py
```

Follow the interactive menu to:
1. Capture gesture samples (50+ per gesture)
2. Train the ML model
3. Your gestures will be automatically loaded!

**Advantages:**
- ✅ Train unlimited custom gestures
- ✅ Perfectly tuned to your hand/lighting
- ✅ Full control over gesture names
- ✅ Works with your camera setup

### Option 2: Download Open-Source Model (Reference Only)

Download a pre-trained SVM model from open-source projects:

```bash
python download_pretrained_gestures.py
```

**Note:** Open-source models use different feature extraction methods, so they're provided as learning references. For best results, train your own gestures with Option 1.

---

## Available Open-Source Models

### 1. Hand_Gesture_Recognition_Using_SVM
- **GitHub:** https://github.com/me2190901/Hand_Gesture_Recognition_Using_SVM
- **Gestures:** 6 hand gestures (labeled 0-5)
- **Accuracy:** 87.66%
- **Features:** HOG + Canny edge detection
- **Model File:** `hog_svm2.pkl` (2.2MB)

### 2. NVIDIA trt_pose_hand
- **GitHub:** https://github.com/NVIDIA-AI-IOT/trt_pose_hand
- **Gestures:** fist, pan, stop, fine, peace, no hand
- **Features:** TensorRT + SVM
- **Best for:** NVIDIA Jetson hardware

### 3. MediaPipe + Custom sklearn
- **Tutorial:** https://medium.com/@vinubalan2892002/realtime-hand-gesture-detection-dataset-collection-and-detection-in-python-scikit-learn-ed5fd896b35f
- **Features:** MediaPipe landmarks + Logistic Regression/SVM
- **Best for:** Modern, lightweight approach

---

## Comparison Table

| Method | Gestures | Training Required | Compatibility | Recommendation |
|--------|----------|-------------------|---------------|----------------|
| **MediaPipe Pretrained** | 7 gestures | ❌ NO | ✅ Built-in | ⭐⭐⭐⭐⭐ Use this first! |
| **Custom Trained** | Unlimited | ✅ YES (5-10 min) | ✅ Perfect fit | ⭐⭐⭐⭐⭐ Best results |
| **Open-source Models** | 6-10 gestures | ❌ NO | ⚠️ May need adaptation | ⭐⭐⭐ Reference only |

---

## Recommended Workflow

```
START HERE
    ↓
Use MediaPipe gestures (already working!)
    ↓
Test with demo: python demo_opencv_hand_gesture.py
    ↓
Need more gestures?
    ↓
Train custom gestures: python train_hand_gestures.py
    ↓
DONE! Unlimited custom gestures!
```

---

## Creating Your Own Gestures

Popular custom gestures to train:

- **Communication:** OK_SIGN, CALL_ME, WAVE, STOP
- **Media Control:** PLAY, PAUSE, NEXT, PREVIOUS
- **Numbers:** ONE, TWO, THREE, FOUR, FIVE
- **Symbols:** HEART, STAR, CHECK, CROSS
- **Fun:** ROCK_ON, SHAKA, HANG_LOOSE, VULCAN_SALUTE

### Training Tips

1. **Lighting:** Use good, consistent lighting
2. **Background:** Plain background works best
3. **Samples:** Capture 50-100 samples per gesture
4. **Variety:** Slightly vary hand angle during capture
5. **Steady:** Hold gesture steady while capturing

---

## Troubleshooting

**Q: Which gestures are currently loaded?**
A: Run your gesture detector and check the startup summary. It shows all available gesture types.

**Q: Can I use both MediaPipe AND custom gestures?**
A: Yes! The system uses a 3-tier detection:
   1. MediaPipe pretrained (best)
   2. Custom ML (user-trained)
   3. Hardcoded finger-counting (fallback)

**Q: Do I need to download open-source models?**
A: No! MediaPipe gestures work instantly, and you can train custom ones in minutes.

**Q: How do I see which gestures are working?**
A: The gesture detector prints a complete summary at startup showing all available gestures.

---

## Support

- Training guide: `GESTURE_TRAINING_GUIDE.md`
- Hands directory: `biometric_data/hands/README.md`
- MediaPipe guide: `docs/MEDIAPIPE_GESTURES.md`

Start with MediaPipe gestures (already working!), then train your own for unlimited possibilities! 🎯
