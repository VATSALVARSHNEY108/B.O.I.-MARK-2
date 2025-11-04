# Easy Volume Control Fix for Windows

## ✅ Brightness Already Works!
Your brightness control is working perfectly. No setup needed.

## 🔧 Fix Volume Control (2 minutes)

### Step 1: Download nircmd.exe
1. Go to: https://www.nirsoft.net/utils/nircmd.html
2. Click "Download NirCmd 64-bit" (or 32-bit if you have 32-bit Windows)
3. Extract the zip file

### Step 2: Install nircmd.exe
**Option A: System-wide (Recommended)**
- Copy `nircmd.exe` to: `C:\Windows\System32\`
- This makes it work everywhere

**Option B: Project-only**
- Copy `nircmd.exe` to your project root folder (where you run commands from)
- Works for this project only

### Step 3: Test
```powershell
# Test volume control
python scripts/volume_brightness_controller.py volume set 50
python scripts/volume_brightness_controller.py volume get
python scripts/volume_brightness_controller.py volume mute

# Test brightness (already working!)
python scripts/volume_brightness_controller.py brightness set 75
```

## 🎯 Why nircmd.exe?

- **Simple**: Just one file, no installation
- **Reliable**: Works on all Windows versions
- **Small**: Only ~100KB
- **Free**: No cost, no signup needed
- **Trusted**: Used by millions of Windows users

## ✅ After Setup

All these will work:

```powershell
# Volume control
python scripts/volume_brightness_controller.py volume set 80
python scripts/volume_brightness_controller.py volume up 5
python scripts/volume_brightness_controller.py volume down 10
python scripts/volume_brightness_controller.py volume mute
python scripts/volume_brightness_controller.py volume get

# Brightness control (already works!)
python scripts/volume_brightness_controller.py brightness set 50
python scripts/volume_brightness_controller.py brightness up 20

# Or use the batch files:
cd scripts\windows_controls
quick_volume_control.bat set 80
quick_brightness_control.bat 50
windows_volume_brightness_control.bat  # Interactive menu
```

## 📸 Quick Visual Guide

1. **Download** → Click "Download NirCmd 64-bit"
2. **Extract** → Right-click zip → "Extract All"
3. **Copy** → Copy `nircmd.exe` from the extracted folder
4. **Paste** → Paste into `C:\Windows\System32\`
5. **Done!** → Volume control now works

---

**That's it!** Just download one small file and everything works perfectly.
