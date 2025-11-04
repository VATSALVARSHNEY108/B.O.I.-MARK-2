# Windows Volume & Brightness Control Batch Files

This project includes batch files for easy volume and brightness control on Windows systems.

## Prerequisites

### Download NirCmd
The volume control batch files require `nircmd.exe` - a free command-line utility for Windows.

1. Download from: https://www.nirsoft.net/utils/nircmd.html
2. Extract `nircmd.exe` from the zip file
3. Place it in one of these locations:
   - Same folder as the batch files
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

## Creating Shortcuts

### Desktop Shortcuts
1. Right-click on any batch file
2. Select "Send to" → "Desktop (create shortcut)"
3. Rename the shortcut if desired

### Keyboard Shortcuts
1. Right-click the shortcut → Properties
2. Click in the "Shortcut key" field
3. Press your desired key combination (e.g., Ctrl + Alt + V)
4. Click OK

**Recommended shortcuts:**
- Volume menu: `Ctrl + Alt + V`
- Set volume 80%: `Ctrl + Alt + 8`
- Brightness 50%: `Ctrl + Alt + B`

## Volume Scale Reference

NirCmd uses a scale of 0-65535 for volume. The batch files convert percentages:
- 0% = 0
- 25% = 16384
- 50% = 32768
- 75% = 49152
- 100% = 65535

## Troubleshooting

### "nircmd.exe is not recognized"
- Download nircmd.exe and place it in the same folder as the batch files
- Or add it to your system PATH

### Brightness control not working
- Some laptops don't support WMI brightness control
- Try using your laptop's function keys (Fn + brightness keys) instead
- External monitors may not support software brightness control

### Permission errors
- Run the batch file as Administrator (right-click → "Run as administrator")

## Integration with Python Scripts

These batch files complement the Python-based system control in `modules/system/system_control.py`. Use:
- Batch files: For quick Windows-only control
- Python scripts: For cross-platform automation with Gemini AI integration

## Advanced Usage

### Run from Command Prompt
```cmd
cd path\to\project
quick_volume_control.bat set 80
```

### Use in scripts
```batch
@echo off
call quick_volume_control.bat set 50
call quick_brightness_control.bat 75
echo Volume and brightness set!
```

### Schedule with Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (time, logon, etc.)
4. Action: Start a program
5. Program: Full path to batch file
6. Add arguments if using quick control versions

## Safety Notes

- Volume is limited to 0-100% to protect hearing and speakers
- Brightness changes are immediate - be careful in dark environments
- Test with moderate values first before using extreme settings
