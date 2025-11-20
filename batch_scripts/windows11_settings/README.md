# Windows 11 Settings Automation Batch Files

Complete automation suite for controlling all major Windows 11 system settings through batch scripts.

## 📁 Files Overview

### Master Controller
- **MASTER_WINDOWS11_SETTINGS.bat** - Main menu to access all settings categories

### Individual Settings Modules

1. **display_settings.bat** - Display Configuration
   - Set resolution (1080p, 2K, 4K, custom)
   - Change display orientation (landscape/portrait)
   - Set refresh rate (60Hz, 120Hz, 144Hz, etc.)
   - Configure display scaling (100%-200%)
   - Toggle night light
   - Multiple monitor settings

2. **sound_settings.bat** - Audio Control
   - Set system volume
   - Mute/unmute system
   - List audio devices
   - Set default playback/recording devices
   - Configure spatial sound
   - Access sound control panel

3. **network_settings.bat** - Network Management
   - WiFi on/off control
   - Airplane mode toggle
   - View network information
   - Configure proxy settings
   - DNS configuration (Google, Cloudflare, OpenDNS)
   - Network reset
   - VPN settings

4. **bluetooth.bat** - Bluetooth Control
   - Turn Bluetooth on/off
   - List paired devices
   - Add/remove Bluetooth devices
   - Access Bluetooth settings

5. **privacy_security.bat** - Privacy & Security
   - Camera privacy controls
   - Microphone privacy controls
   - Location privacy settings
   - Windows Defender (scan, update)
   - Firewall configuration
   - App permissions
   - Telemetry settings
   - User Account Control (UAC)

6. **personalization.bat** - Appearance Customization
   - Dark/Light mode switching
   - Accent color configuration
   - Desktop wallpaper settings
   - Taskbar customization (alignment, auto-hide)
   - Start menu settings
   - Lock screen configuration
   - Themes

7. **system_settings.bat** - System Configuration
   - Notification management
   - Focus Assist settings
   - Clipboard history control
   - Storage Sense configuration
   - Remote Desktop enable/disable
   - Power & sleep settings
   - Startup apps management
   - Date & time synchronization

8. **windows_update.bat** - Update Management
   - Check for updates
   - Install all updates
   - Pause updates (1-5 weeks)
   - Resume updates
   - View update history
   - Advanced update options

9. **accessibility.bat** - Accessibility Features
   - Narrator control
   - Magnifier control
   - High contrast themes
   - Keyboard accessibility (Sticky Keys, Filter Keys, Toggle Keys)
   - Mouse accessibility (Mouse Keys)
   - Text size adjustment
   - Color filters

## 🚀 Quick Start

### Run Master Controller
```batch
cd batch_scripts\windows11_settings
MASTER_WINDOWS11_SETTINGS.bat
```

### Run Individual Module
```batch
cd batch_scripts\windows11_settings
display_settings.bat
```

## 📋 Features

### ✅ Display Settings
- ✓ Resolution control (Full HD, 2K, 4K, custom)
- ✓ Orientation rotation (0°, 90°, 180°, 270°)
- ✓ Refresh rate selection
- ✓ Display scaling (DPI)
- ✓ Night light toggle
- ✓ Display information viewer

### ✅ Sound Settings
- ✓ Volume control (0-100%)
- ✓ Mute/unmute toggle
- ✓ Audio device enumeration
- ✓ Spatial sound configuration
- ✓ Classic sound control panel access

### ✅ Network Settings
- ✓ WiFi enable/disable
- ✓ Airplane mode toggle
- ✓ IP configuration viewer
- ✓ Proxy enable/disable/configure
- ✓ DNS presets (Google, Cloudflare, OpenDNS)
- ✓ Complete network reset

### ✅ Privacy & Security
- ✓ Camera access control
- ✓ Microphone access control
- ✓ Location services toggle
- ✓ Windows Defender quick/full scan
- ✓ Firewall enable/disable
- ✓ Telemetry level control
- ✓ UAC enable/disable

### ✅ Personalization
- ✓ Dark/Light mode switching
- ✓ Accent color on taskbar/Start
- ✓ Taskbar alignment (center/left)
- ✓ Auto-hide taskbar
- ✓ Start menu layout
- ✓ Task View button toggle
- ✓ Widgets button toggle

### ✅ System Settings
- ✓ Notifications enable/disable
- ✓ Focus Assist modes
- ✓ Clipboard history toggle
- ✓ Storage Sense control
- ✓ Remote Desktop enable/disable
- ✓ Sleep timer configuration
- ✓ Time synchronization

### ✅ Windows Update
- ✓ Check for updates
- ✓ Install updates
- ✓ Pause updates (1-5 weeks)
- ✓ Resume updates
- ✓ Update history
- ✓ Automatic update control

### ✅ Accessibility
- ✓ Narrator start/stop
- ✓ Magnifier start/stop
- ✓ High contrast themes
- ✓ Sticky Keys toggle
- ✓ Filter Keys toggle
- ✓ Mouse Keys toggle
- ✓ Text size adjustment
- ✓ Color filters

## 🔧 Technical Details

### Registry Modifications
Many settings are controlled through Windows Registry modifications:
- Display scaling: `HKCU\Control Panel\Desktop`
- Dark mode: `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize`
- Privacy settings: `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager`
- Taskbar: `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced`

### PowerShell Integration
Advanced features use PowerShell commands:
- Display information retrieval
- Bluetooth control
- Windows Defender operations
- Audio device management

### Windows Settings URIs
Direct access to Windows Settings pages using `ms-settings:` protocol:
- `ms-settings:display`
- `ms-settings:sound`
- `ms-settings:network`
- `ms-settings:bluetooth`
- `ms-settings:privacy`
- And many more...

## ⚠️ Important Notes

### Administrator Rights
Some operations require administrator privileges:
- Network adapter changes
- Firewall modifications
- System-wide settings
- Windows Update control
- Remote Desktop enable/disable

**Run as Administrator when needed:**
```batch
Right-click batch file → Run as administrator
```

### System Compatibility
- Designed for **Windows 11**
- Some features may work on Windows 10
- Registry paths are Windows 11 specific

### Safety
- All scripts include confirmation prompts for destructive operations
- Network reset requires system restart
- Some changes take effect after sign-out/restart
- Backup important data before making system-wide changes

## 🔗 Integration with VATSAL

These batch files integrate seamlessly with the VATSAL AI Desktop Automation Controller:
- Voice command support through command executor
- Python wrapper functions in `Windows11SettingsController`
- GUI integration through batch utilities system
- Real-time monitoring and logging

## 📝 Usage Examples

### Example 1: Enable Dark Mode
```batch
Run: personalization.bat
Select: [1] Dark/Light Mode
Select: [1] Enable Dark Mode (System + Apps)
```

### Example 2: Change Display Resolution
```batch
Run: display_settings.bat
Select: [1] Set Resolution
Select: [1] 1920x1080 (Full HD)
```

### Example 3: Pause Windows Updates
```batch
Run: windows_update.bat
Select: [3] Pause Updates (7 days)
Select: [2] Pause for 2 weeks
```

### Example 4: Enable Airplane Mode
```batch
Run: network_settings.bat
Select: [2] Airplane Mode On/Off
Select: [1] Enable Airplane Mode
```

## 🎯 Voice Command Integration

When integrated with VATSAL, you can use voice commands like:
- "Set display to dark mode"
- "Turn on airplane mode"
- "Enable night light"
- "Set volume to 50"
- "Pause Windows updates"
- "Turn on Bluetooth"
- "Enable high contrast mode"

## 📚 Additional Resources

- Official Windows 11 documentation
- PowerShell documentation for advanced scripting
- Windows Registry editing best practices
- VATSAL AI documentation

## 🔄 Updates & Maintenance

This automation suite is actively maintained and includes:
- Bug fixes
- New feature additions
- Windows 11 update compatibility
- Performance optimizations

## 📞 Support

For issues or questions:
1. Check the VATSAL documentation
2. Review batch file comments
3. Test individual modules
4. Run with administrator rights if needed

---

**Version:** 1.0.0  
**Last Updated:** November 2025  
**Compatible with:** Windows 11 (22H2 and later)
