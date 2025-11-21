# Windows Setup Guide for BOI (Barely Obeys Instructions) Desktop Automation

## Python Version Compatibility

### Current Issue
You're running **Python 3.13.9**, but MediaPipe (required for hand gesture recognition) doesn't support Python 3.13 on Windows yet.

### Solutions

#### Option 1: Run Without MediaPipe (Recommended for Quick Start)
The app is now configured to work **without MediaPipe**:
- ✅ Face detection works (uses OpenCV)
- ❌ Hand gesture recognition disabled
- ✅ All other features work normally

**Just run:**
```bash
streamlit run vatsal.py --server.port=5000 --server.address=0.0.0.0 --server.headless=true
```

#### Option 2: Install Compatible Python Version (For Full Features)
To enable hand gesture recognition:

1. **Install Python 3.11** from https://www.python.org/downloads/
   - ⚠️ During installation, check "Add Python to PATH"
   - Choose "Customize installation" and install for all users

2. **Create a new virtual environment:**
   ```bash
   # Navigate to your project directory
   cd "C:\Users\BOI VARSHNEY\PycharmProjects\BOI NL"
   
   # Create virtual environment with Python 3.11
   py -3.11 -m venv venv311
   
   # Activate it
   venv311\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   streamlit run vatsal.py --server.port=5000 --server.address=0.0.0.0 --server.headless=true
   ```

## Feature Comparison

| Feature | With MediaPipe (Python 3.11) | Without MediaPipe (Python 3.13) |
|---------|------------------------------|----------------------------------|
| Face Detection | ✅ | ✅ |
| Hand Gesture Recognition | ✅ | ❌ |
| Voice Commands | ✅ | ✅ |
| Desktop Automation | ✅ | ✅ |
| AI Features (Gemini) | ✅ | ✅ |
| All Other Features | ✅ | ✅ |

## Recommended Configuration

For **full feature access**, use:
- **Python 3.11** (best compatibility)
- OR **Python 3.10** (also works)

For **quick testing without hand gestures**:
- Your current **Python 3.13** setup will work fine

## Troubleshooting

### "mediapipe not found" Error
This is **expected** on Python 3.12/3.13. The app will show:
```
⚠️  MediaPipe not available - hand gesture recognition will be disabled
   Face detection will still work using OpenCV
```

This is normal and the app will continue running.

### Running the Correct Command
Don't use `python vatsal.py` directly. Instead use:
```bash
streamlit run vatsal.py --server.port=5000 --server.address=0.0.0.0 --server.headless=true
```

This ensures Streamlit's session management works correctly.

## Questions?

The app is designed to gracefully handle missing features, so you can start using it right away even without MediaPipe installed!
