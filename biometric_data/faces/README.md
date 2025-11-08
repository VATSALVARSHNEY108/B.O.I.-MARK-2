# Face Recognition Training Data

This folder contains training data for personalized face recognition.

## Folder Structure

```
biometric_data/faces/
├── vatsal/
│   └── training/          # Your training photos (7 images)
├── models/
│   ├── face_model.yml     # Trained model (generated)
│   └── labels.pkl         # Person labels (generated)
└── README.md
```

## Your Training Photos

Location: `vatsal/training/`

Currently contains:
- 7 photos of Vatsal
- Various poses and gestures
- Good lighting and angles

## How It Works

### 1. Training Process
```bash
python train_vatsal_face.py
```

This will:
1. Scan all photos in `vatsal/training/`
2. Detect faces in each photo
3. Extract facial features
4. Train a recognition model
5. Save model to `models/face_model.yml`

### 2. Recognition Process
```bash
python test_face_recognition.py
```

This will:
1. Load the trained model
2. Open your webcam
3. Detect faces in real-time
4. Recognize you as "VATSAL"
5. Show confidence score

## Adding More People

To add recognition for more people:

```bash
# Create folder for new person
mkdir -p biometric_data/faces/[name]/training

# Add their photos
cp /path/to/photos/*.jpg biometric_data/faces/[name]/training/

# Retrain model
python train_vatsal_face.py
```

## Model Details

- **Algorithm**: LBPH (Local Binary Patterns Histograms)
- **Face Detection**: Haar Cascade
- **Input Size**: 200x200 pixels
- **Confidence**: 0-100% (higher is better)

## Tips for Best Results

### Taking Training Photos:
- ✅ Use 5-10 photos minimum
- ✅ Different angles (front, side, tilted)
- ✅ Different lighting conditions
- ✅ Different expressions
- ✅ With and without glasses (if you wear them)
- ❌ Avoid blurry photos
- ❌ Avoid photos with multiple people

### For Recognition:
- Good, even lighting
- Look at the camera
- Remove obstructions (hands, hair covering face)
- Stay within 1-3 feet of camera

## Privacy & Security

- ⚠️  Training data is stored locally
- ⚠️  Model file contains facial features
- ⚠️  Keep this folder private
- ⚠️  Do not share model files
- ⚠️  Backup before updates

## Files Generated

After training, you'll see:
- `models/face_model.yml` - The trained model (~50-100KB)
- `models/labels.pkl` - Name-to-ID mapping
- Console logs showing training progress

## Troubleshooting

### No faces detected in training:
- Check image quality
- Ensure face is visible and clear
- Try photos with better lighting

### Low recognition confidence:
- Add more training photos
- Ensure varied angles/expressions
- Retrain the model

### "No trained model found":
- Run `python train_vatsal_face.py` first
- Check that `models/face_model.yml` exists

## Status

✅ Training data ready (7 photos)  
⏳ Model not trained yet  
📝 Run: `python train_vatsal_face.py`
