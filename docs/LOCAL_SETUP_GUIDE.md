# 🏠 Running on Your Local Windows PC

## Quick Setup (5 minutes)

### Step 1: Download Files from Replit

Click the three dots menu (⋮) in Replit and select **"Download as ZIP"**

Or download these essential files:
- `gui_app.py`
- `desktop_controller_integration.py`
- `desktop_file_controller.bat`
- `simple_chatbot.py`
- `command_executor.py`
- `gemini_controller.py`
- All other `.py` files from the project
- `.env` file (with your API keys)

### Step 2: Install Python (if not installed)

1. Download Python 3.11+ from: https://www.python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Verify: Open Command Prompt and type `python --version`

### Step 3: Install Dependencies

Open Command Prompt in your project folder:

```bash
pip install google-genai pyautogui pyperclip psutil python-dotenv pyttsx3 pywhatkit requests speechrecognition watchdog cryptography
```

### Step 4: Run the GUI

```bash
python gui_app.py
```

### Step 5: Test Desktop Controller

1. Open GUI
2. Go to **🖥️ Desktop** tab
3. Click **📋 List Desktop Items**
4. You'll see YOUR actual desktop folders including "coding"!
5. Click **🗂️ Launch Batch Controller** to use the Windows menu

---

## 🪟 Using Just the Batch File (Easier)

If you just want the file controller:

1. Download `desktop_file_controller.bat`
2. Put it anywhere on your PC
3. Double-click to run
4. It will manage your **actual desktop**!

No Python needed for the batch file! ✅

---

## 🔧 Accessing Your Real Desktop from BOI Chatbot

Once running locally, BOI commands like:
- "open coding folder on desktop" ✅ Will work!
- "organize desktop" ✅ Will organize YOUR desktop!
- "list desktop files" ✅ Will show YOUR files!

---

## 📊 Current Status

**On Replit (Cloud):**
- ✅ GUI works but accesses Replit's virtual desktop
- ✅ Test folders created: coding, projects, documents, downloads
- ✅ Good for testing functionality

**On Your PC (Local):**
- ✅ Accesses YOUR actual desktop with YOUR folders
- ✅ Full system integration
- ✅ All automation features work with your real files

---

## ⚡ Quick Test

Try this in the BOI chatbot NOW (on Replit):

```
list desktop files
```

You'll see the test folders! When you run locally, you'll see your real folders instead.
