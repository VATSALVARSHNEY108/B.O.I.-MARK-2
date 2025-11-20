# Windows Control Scripts

This directory contains batch files for controlling Windows system features.

## Available Scripts

### 1. `close_all_windows.bat`
**Description:** Closes all open windows, browser tabs, and applications.

**What it does:**
- Closes all browser windows (Chrome, Firefox, Edge, Opera, Brave)
- Closes common applications (Notepad, VS Code, Discord, Spotify, etc.)
- Uses PowerShell to gracefully close remaining windows
- Protects system critical processes (explorer, taskmgr, etc.)

**Usage:**
```batch
close_all_windows.bat
```

**Safety Features:**
- 5-second countdown before execution
- Skips system-critical processes
- Can be cancelled with Ctrl+C during countdown

### 2. `quick_volume_control.bat`
**Description:** Control system volume from command line.

**Usage:**
```batch
quick_volume_control.bat set 50    # Set volume to 50%
quick_volume_control.bat up 10     # Increase volume by 10%
quick_volume_control.bat down 10   # Decrease volume by 10%
quick_volume_control.bat mute      # Toggle mute
quick_volume_control.bat get       # Get current volume
```

### 3. `quick_brightness_control.bat`
**Description:** Control screen brightness from command line.

**Usage:**
```batch
quick_brightness_control.bat 75    # Set brightness to 75%
```

### 4. `windows_volume_brightness_control.bat`
**Description:** Interactive menu for volume and brightness control.

**Usage:**
```batch
windows_volume_brightness_control.bat
```

## Python Integration

These batch files are integrated with the VATSAL AI system through the `SystemController` class in `modules/system/system_control.py`.

### Voice Commands

You can use these features through voice commands:
- "Close all windows"
- "Close all tabs"
- "Set volume to 50"
- "Increase brightness"
- "Lock screen"
- "Shutdown computer"

### Python API

```python
from modules.system.system_control import SystemController

controller = SystemController()

# Close all windows
controller.close_all_windows()

# Close all tabs (same as above)
controller.close_all_tabs()

# Control volume
controller.set_volume(50)
controller.increase_volume(10)

# Control brightness
controller.set_brightness(75)

# System control
controller.lock_screen()
controller.shutdown_system(10)
controller.restart_system(10)
```

## Requirements

- Windows 10 or later
- PowerShell 5.0 or later (included in Windows 10+)
- Administrator privileges for some operations

## Safety Notes

⚠️ **Important:**
- Always save your work before using `close_all_windows.bat`
- System-critical processes are protected and won't be closed
- Shutdown/restart commands can be cancelled with `shutdown /a`
- These scripts only work on Windows systems

## Troubleshooting

**Q: close_all_windows.bat doesn't close some applications**
A: Some applications may resist forced closing. You can modify the batch file to add specific applications to the kill list.

**Q: I need administrator privileges error**
A: Right-click the batch file and select "Run as administrator"

**Q: PowerShell execution policy error**
A: Run this in PowerShell as admin: `Set-ExecutionPolicy RemoteSigned`

## Advanced Usage

You can customize the behavior by editing the batch files directly. For example, to add more applications to close:

```batch
taskkill /F /IM YourApp.exe 2>nul
```

## Support

For issues or feature requests, check the main VATSAL AI documentation or contact support.
