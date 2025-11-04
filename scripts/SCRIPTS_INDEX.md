# Scripts Directory Index

This directory contains various utility scripts for the AI Desktop Automation Controller.

## 📁 Directory Structure

### `windows_controls/`
**Windows batch files for volume and brightness control**
- `windows_volume_brightness_control.bat` - Interactive menu for volume/brightness
- `quick_volume_control.bat` - Command-line volume control
- `quick_brightness_control.bat` - Command-line brightness control
- `WINDOWS_BATCH_FILES_README.md` - Complete documentation

**Requirements:** Download `nircmd.exe` from https://www.nirsoft.net/utils/nircmd.html

## 🔧 Standalone Scripts

### Python Scripts

#### System Control
- `volume_brightness_controller.py` ⭐ **NEW** - Cross-platform volume & brightness control
  - Usage: `python volume_brightness_controller.py volume set 80`
  - Features: volume control, brightness control, interactive menu (Windows)

#### Voice & Audio
- `check_voices.py` - Check available text-to-speech voices
- `create_wav_files.py` - Create WAV audio files
- `hear_modi_voice.py` - Test Modi voice settings
- `set_kid_voice.py` - Configure kid voice settings

#### Utilities
- `debug_lock_command.py` - Debug screen lock functionality
- `organize_project.py` - Project organization utility

### Windows Batch Files
- `desktop_file_controller.bat` - Control desktop files
- `quick_lock.bat` - Quick screen lock
- `quick_restart.bat` - Quick system restart
- `quick_shutdown.bat` - Quick system shutdown

### Web Files
- `whatsapp_launcher.html` - WhatsApp web launcher

## 🚀 Quick Start

### For Windows Users
1. Navigate to `scripts/windows_controls/`
2. Download `nircmd.exe` and place it in that folder
3. Double-click any `.bat` file to run

### For Python Scripts
```bash
cd scripts
python script_name.py
```

### Volume & Brightness Control
**Cross-platform Python control:**
```bash
# Set volume to 80%
python scripts/volume_brightness_controller.py volume set 80

# Increase volume by 5%
python scripts/volume_brightness_controller.py volume up 5

# Set brightness to 50%
python scripts/volume_brightness_controller.py brightness set 50

# Open interactive menu (Windows only)
python scripts/volume_brightness_controller.py volume menu
```

**Windows batch file control:**
- Navigate to `scripts/windows_controls/`
- Double-click `windows_volume_brightness_control.bat` for interactive menu
- Or use command-line: `quick_volume_control.bat set 80`

## 📖 Documentation
For detailed information about specific scripts, refer to the README files in their respective directories.
