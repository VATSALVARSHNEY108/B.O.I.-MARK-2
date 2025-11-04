# Windows Volume & Brightness Control

## ⚠️ IMPORTANT: Recommended Approach

**The Python-based volume control is now the recommended method** as it works out-of-the-box without requiring external tools!

### Use Python Scripts Instead (Recommended ✅)

```powershell
# Volume control - Works immediately, no setup required!
python scripts/volume_brightness_controller.py volume set 80
python scripts/volume_brightness_controller.py volume up 5
python scripts/volume_brightness_controller.py volume down 10
python scripts/volume_brightness_controller.py volume mute
python scripts/volume_brightness_controller.py volume get

# Brightness control
python scripts/volume_brightness_controller.py brightness set 75
```

**Benefits:**
- ✅ No external tools required (nircmd.exe not needed)
- ✅ Works immediately - no downloads or setup
- ✅ More secure - pure Python solution
- ✅ Cross-platform ready (Windows, macOS, Linux)
- ✅ Better error handling and reliability

---

## Legacy Batch Files (Deprecated)

This folder contains **legacy** batch files that rely on `nircmd.exe`. These are kept for backward compatibility but are **no longer recommended**.

**Location:** `scripts/windows_controls/`

### Why Not Use Batch Files?

1. **Requires nircmd.exe download** - Extra setup step
2. **Security concerns** - External executable required
3. **Windows-only** - Not cross-platform
4. **Outdated** - Python solution is superior

### If You Still Want to Use Batch Files

The volume control batch files require `nircmd.exe` - a free command-line utility for Windows.

1. Download from: https://www.nirsoft.net/utils/nircmd.html
2. Extract `nircmd.exe` from the zip file
3. Place it in one of these locations:
   - `scripts/windows_controls/` (same folder as these batch files)
   - `C:\Windows\System32\` (requires admin rights)
   - Any folder in your system PATH

## Available Batch Files

### 1. `windows_volume_brightness_control.bat` (Interactive Menu)

A full-featured interactive menu for controlling volume and brightness.

**How to use:**
- Double-click the file to launch the menu
- Select options by typing the number/letter and pressing Enter

**Features:**
- Preset volume levels (0%, 25%, 50%, 75%, 100%)
- Volume up/down by 10%
- Toggle mute
- Get current volume level
- Preset brightness levels (25%, 50%, 75%, 100%)
- Custom volume and brightness input

### 2. `quick_volume_control.bat` (Command Line)

Quick command-line volume control without menus.

**Usage:**
```batch
quick_volume_control.bat [command] [value]
```

**Commands:**
- `set [0-100]` - Set volume to specific percentage
- `up [amount]` - Increase volume (default 10)
- `down [amount]` - Decrease volume (default 10)
- `mute` - Toggle mute
- `get` - Show current volume

**Examples:**
```batch
quick_volume_control.bat set 80
quick_volume_control.bat up 5
quick_volume_control.bat down 10
quick_volume_control.bat mute
quick_volume_control.bat get
```

### 3. `quick_brightness_control.bat` (Command Line)

Quick command-line brightness control.

**Usage:**
```batch
quick_brightness_control.bat [0-100]
```

**Examples:**
```batch
quick_brightness_control.bat 50
quick_brightness_control.bat 100
quick_brightness_control.bat 25
```

---

## Migration Guide

### From Batch Files to Python

**Old (Batch):**
```batch
quick_volume_control.bat set 80
```

**New (Python):**
```powershell
python scripts/volume_brightness_controller.py volume set 80
```

### Creating Shortcuts for Python Commands

1. Create a new `.bat` file with this content:
```batch
@echo off
python scripts/volume_brightness_controller.py volume set 80
```

2. Create a shortcut to this file
3. Assign a keyboard shortcut if desired

---

## Recommended: Switch to Python

For the best experience, use the Python-based controller:

```powershell
# See all available commands
python scripts/volume_brightness_controller.py

# Test the new system
python test_volume_pycaw.py
```

**No downloads required - Everything just works!** ✅
