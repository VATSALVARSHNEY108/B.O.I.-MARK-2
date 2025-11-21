# How to Run BOI GUI with Voice Commands Locally

Voice commands **cannot work in Replit cloud** because the code needs direct access to your computer's microphone.

## Steps to Run Locally:

1. **Download this project**
   - Click the three dots menu in Replit
   - Select "Download as zip"
   - Extract to your computer

2. **Install Python** (if not already installed)
   - Download from python.org
   - Version 3.11 or higher

3. **Install dependencies**
   ```bash
   cd /path/to/extracted/folder
   pip install -r requirements.txt
   ```

4. **Set up environment**
   - Create a `.env` file
   - Add your API key: `GEMINI_API_KEY=your_key_here`

5. **Run the GUI**
   ```bash
   python vatsal.py
   ```

6. **Voice commands will now work** ✅
   - The GUI will access your local microphone
   - Say "bhai" or "vatsal" to activate
   - Speak your commands

## Why This is Required:

- ❌ Cloud (Replit): GUI cannot access your microphone
- ✅ Local (Your PC): GUI has full hardware access

The code `sr.Microphone()` needs physical hardware that only exists on your local computer.
