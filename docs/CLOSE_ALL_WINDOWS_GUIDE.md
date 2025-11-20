# Close All Windows Feature - Complete Guide

## Overview

The **Close All Windows** feature allows VATSAL AI to instantly close all open windows, tabs, and applications on your computer. This is useful for:
- Quickly cleaning up your workspace
- Preparing for a presentation
- Closing many browser tabs at once
- Emergency privacy shutdown
- System cleanup before shutdown

## Features

✅ **Comprehensive Closing:**
- Closes all browser windows and tabs (Chrome, Firefox, Edge, Opera, Brave)
- Closes common applications (VS Code, Discord, Spotify, Telegram, WhatsApp, etc.)
- Safely handles remaining windows with PowerShell

✅ **Smart Protection:**
- Never closes system-critical processes
- Protects: Explorer, Task Manager, System Settings
- Protects: Python processes (so VATSAL keeps running!)
- Protects: CMD and PowerShell windows

✅ **Multi-Platform Support:**
- **Windows:** Full support with batch files and PowerShell
- **macOS:** AppleScript-based closing
- **Linux:** wmctrl-based window management

## Usage Methods

### 1. Voice Commands

Simply say:
```
"Close all windows"
"Close all tabs"
"Close everything"
```

### 2. Python API

```python
from modules.system.system_control import SystemController

controller = SystemController()

# Close all windows and tabs
result = controller.close_all_windows()
print(result)

# Alternative method (same as above)
result = controller.close_all_tabs()
print(result)
```

### 3. Quick Command Line

```bash
# Using quick system commands
python modules/system/quick_system_commands.py close-all

# Or using the dedicated test script
python scripts/test_close_all_windows.py
```

### 4. Direct Batch File (Windows Only)

```batch
# With confirmation
scripts\windows_controls\close_all_windows.bat

# Quick close without confirmation
scripts\close_all_tabs.bat
```

### 5. GUI Integration

The feature is automatically available in:
- VATSAL GUI voice commands
- VATSAL Desktop Automator
- Web GUI controls

## How It Works

### Windows Implementation

1. **Batch File Method (Primary):**
   - Runs `scripts/windows_controls/close_all_windows.bat`
   - Uses `taskkill` for known applications
   - Uses PowerShell for remaining windows

2. **PowerShell Fallback:**
   - Closes browsers: Chrome, Firefox, Edge, Opera, Brave
   - Closes apps: Notepad, VS Code, Discord, Spotify, Telegram, WhatsApp
   - Uses PowerShell to gracefully close other windows
   - Filters out protected processes

3. **Protected Processes:**
   ```
   - explorer.exe (Windows Explorer)
   - taskmgr.exe (Task Manager)
   - SystemSettings.exe (Windows Settings)
   - cmd.exe (Command Prompt)
   - powershell.exe (PowerShell)
   - python.exe / pythonw.exe (VATSAL itself)
   ```

### macOS Implementation

Uses AppleScript to:
- Query all running applications
- Quit non-system applications
- Protect Finder, System Preferences, and Terminal

### Linux Implementation

Uses command-line tools:
- `killall` for browsers
- `wmctrl` for window management
- Graceful fallback if tools not available

## Safety Features

🛡️ **System Protection:**
- Critical system processes are never closed
- VATSAL AI itself continues running
- File explorers remain open for navigation

⏱️ **Countdown Timer:**
- Batch file version has 5-second countdown
- Can be cancelled with Ctrl+C

💾 **Data Safety:**
- **WARNING:** Unsaved work will be lost!
- Applications are force-closed (like Alt+F4)
- Always save your work first

## Testing

### Safe Testing

Use the test script for controlled testing:

```bash
python scripts/test_close_all_windows.py
```

This will:
1. List all open windows
2. Wait 5 seconds (cancel with Ctrl+C)
3. Close all windows
4. Show results

### Manual Testing

1. **Open some test windows:**
   - Open a browser with multiple tabs
   - Open Notepad or other applications
   - Open VS Code or other editors

2. **Run the command:**
   ```bash
   python modules/system/quick_system_commands.py close-all
   ```

3. **Verify:**
   - All browser tabs should be closed
   - Applications should be closed
   - System apps should still be running

## Integration with Other Features

### Shutdown Workflow

Combine with shutdown for a complete cleanup:

```python
# Close everything then shutdown
controller.close_all_windows()
time.sleep(2)  # Give processes time to close
controller.shutdown_system(10)
```

### Automation Scripts

```python
# End of workday automation
def end_workday():
    controller.close_all_windows()
    controller.clear_temp_files()
    controller.empty_recycle_bin()
    controller.shutdown_system(60)
```

### Voice Command Chains

Configure VATSAL to recognize complex commands:
- "Clean up and shutdown" → Close all + Shutdown
- "Privacy mode" → Close all + Lock screen
- "Reset workspace" → Close all + Minimize all

## Customization

### Adding Applications to Close

Edit `scripts/windows_controls/close_all_windows.bat`:

```batch
REM Add your custom application
taskkill /F /IM YourApp.exe 2>nul
```

### Protecting Additional Processes

Edit `modules/system/system_control.py` in the `close_all_windows()` method:

```python
# Add to protected process list
powershell_cmd = """Get-Process | Where-Object {$_.MainWindowTitle -ne ''} | 
Where-Object {$_.ProcessName -notin @('explorer','taskmgr','SystemSettings',
'cmd','powershell','python','pythonw','YourProtectedApp')} | 
Stop-Process -Force -ErrorAction SilentlyContinue"""
```

## Troubleshooting

### Issue: Some windows don't close

**Solution:**
- Some applications have close protection
- Try adding them specifically to the batch file
- Or close them manually before running

### Issue: "Access Denied" errors

**Solution:**
- Run the script/command as Administrator
- Some processes require elevated privileges

### Issue: VATSAL closes itself

**Solution:**
- This shouldn't happen - Python processes are protected
- If it does, report it as a bug
- Check if process name is in protected list

### Issue: Works in test but not via voice

**Solution:**
- Check command executor integration
- Verify voice recognition is detecting the command
- Check logs for error messages

## Command Reference

| Method | Command | Description |
|--------|---------|-------------|
| Voice | "Close all windows" | Close everything |
| Voice | "Close all tabs" | Same as above |
| CLI | `python modules/system/quick_system_commands.py close-all` | Command line |
| Batch | `scripts\close_all_tabs.bat` | Quick Windows |
| Python | `controller.close_all_windows()` | API call |
| Python | `controller.close_all_tabs()` | API call (alias) |

## Performance Notes

- **Execution time:** 2-5 seconds
- **Processes closed:** Typically 10-30 processes
- **Memory freed:** Varies by usage (often 1-4 GB)
- **CPU spike:** Brief spike during execution

## Security Considerations

⚠️ **Warning:**
- This is a powerful feature
- Unsaved work will be lost
- Use with caution
- Not recommended for:
  - Active downloads
  - Rendering operations
  - Unsaved documents
  - Database transactions

✅ **Safe for:**
- End of day cleanup
- Pre-presentation setup
- System maintenance
- Privacy shutdown

## Future Enhancements

Planned improvements:
- [ ] Selective closing by application type
- [ ] Save-prompt for unsaved documents
- [ ] Whitelist/blacklist management
- [ ] Scheduled cleanup automation
- [ ] Statistics tracking

## Related Features

- `lock_screen()` - Lock your computer
- `shutdown_system()` - Shutdown computer
- `restart_system()` - Restart computer
- `minimize_all_windows()` - Minimize all (without closing)
- `clear_temp_files()` - Clean temporary files
- `empty_recycle_bin()` - Empty trash

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the main VATSAL AI documentation
3. Check system logs for error messages
4. Test with the diagnostic script

---

**Version:** 1.0  
**Last Updated:** November 2025  
**Platform:** Windows 10/11, macOS 10.14+, Linux (Ubuntu/Debian)
