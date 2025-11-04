# Windows Volume Control Setup

## ⚠️ Current Issue
You're seeing: `'nircmd.exe' is not recognized as an internal or external command`

This means Windows volume control needs additional setup.

## ✅ SOLUTION - Choose One Method:

### Method 1: Install pycaw (Recommended - No external files needed)

Run this in PowerShell:
```powershell
pip install pycaw comtypes
```

**Benefits:**
- ✅ No external files needed
- ✅ Native Windows API
- ✅ Most reliable
- ✅ Works permanently

After installation, the volume commands will work automatically!

---

### Method 2: Download nircmd.exe (Alternative)

1. Download from: https://www.nirsoft.net/utils/nircmd.html
2. Extract `nircmd.exe` from the zip file
3. Place it in ONE of these locations:
   - `C:\Windows\System32\` (recommended - works globally)
   - `scripts\windows_controls\` (works for batch files only)
   - Your project root folder

---

## 🧪 Test After Setup

```powershell
# Test volume control
python scripts/volume_brightness_controller.py volume set 50
python scripts/volume_brightness_controller.py volume get

# Or use batch files (if nircmd is in scripts/windows_controls/)
cd scripts\windows_controls
quick_volume_control.bat set 80
```

---

## 🎯 Quick Install Command

**Just run this in your PowerShell:**
```powershell
pip install pycaw comtypes
```

Then test again:
```powershell
python scripts/volume_brightness_controller.py volume set 50
```

---

## ℹ️ How It Works

The system now uses this priority:
1. **pycaw** (Python library - best for Windows) ← Install this!
2. **nircmd.exe** (External tool - fallback)
3. Error message if neither is available

Once you install `pycaw`, you'll never need nircmd.exe!

---

## 🚀 After Installation

All these will work:
```powershell
# Python controller
python scripts/volume_brightness_controller.py volume set 80
python scripts/volume_brightness_controller.py volume up 5
python scripts/volume_brightness_controller.py volume mute

# Quick system commands
cd modules/system
python quick_system_commands.py vol-set 75
python quick_system_commands.py vol-up 10

# Batch files (if you installed nircmd.exe in the right location)
cd scripts\windows_controls
quick_volume_control.bat set 80
windows_volume_brightness_control.bat  # Interactive menu
```

---

## 📞 Still Having Issues?

If `pip install pycaw` gives you errors, try:
```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Then install pycaw
pip install pycaw comtypes
```

Or just use the batch files with nircmd.exe!
