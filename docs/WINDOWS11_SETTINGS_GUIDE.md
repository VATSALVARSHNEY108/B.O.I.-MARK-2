# Windows 11 Settings Controller - Complete Guide

## Overview
The Windows 11 Settings Controller provides comprehensive control over **ALL** Windows 11 system settings through voice commands, Python API, and PowerShell automation.

## Features Summary
- ✅ **100+ Settings Functions** - Control every aspect of Windows 11
- ✅ **Voice Command Integration** - Control settings hands-free
- ✅ **PowerShell Automation** - Native Windows API access
- ✅ **Registry Management** - Direct registry modifications
- ✅ **Real-time Updates** - Instant settings changes

---

## 📺 Display Settings

### Get Display Information
```python
# Voice: "Get display information"
# Python: win11_settings.get_display_info()
```
Returns screen resolution, primary monitor, bit depth, etc.

### Set Display Resolution
```python
# Voice: "Set display resolution to 1920x1080"
# Python: win11_settings.set_display_resolution(1920, 1080)
```
**Supported resolutions**: 1280x720, 1920x1080, 2560x1440, 3840x2160

### Set Display Scaling
```python
# Voice: "Set display scaling to 125 percent"
# Python: win11_settings.set_display_scaling(125)
```
**Valid scales**: 100%, 125%, 150%, 175%, 200%
**Note**: Requires restart

### Enable/Disable Night Light
```python
# Voice: "Enable night light" / "Turn on night light at 4800 kelvin"
# Python: win11_settings.set_night_light(True, temperature=4800)
```
**Temperature range**: 1200K (warm) - 6500K (cool)

### Set Refresh Rate
```python
# Voice: "Set refresh rate to 144 hertz"
# Python: win11_settings.set_refresh_rate(144)
```
**Common rates**: 60Hz, 75Hz, 120Hz, 144Hz, 165Hz, 240Hz

---

## 🔊 Sound Settings

### List Audio Devices
```python
# Voice: "List audio devices" / "Show playback devices"
# Python: win11_settings.list_audio_devices("playback")
```
**Device types**: "playback", "recording"

### Set Default Audio Device
```python
# Voice: "Set default audio device to speakers"
# Python: win11_settings.set_default_audio_device("Speakers", "playback")
```

### Enable Spatial Sound
```python
# Voice: "Enable Windows Sonic spatial sound"
# Python: win11_settings.set_spatial_sound(True, "WindowsSonic")
```
**Formats**: "WindowsSonic", "DolbyAtmos", "DTS", "Off"

---

## 🌐 Network Settings

### Get Network Adapters
```python
# Voice: "Show network adapters" / "List network connections"
# Python: win11_settings.get_network_adapters()
```

### Enable/Disable WiFi
```python
# Voice: "Turn on WiFi" / "Disable WiFi"
# Python: win11_settings.set_wifi_state(True)
```

### Enable/Disable Airplane Mode
```python
# Voice: "Enable airplane mode" / "Turn on airplane mode"
# Python: win11_settings.set_airplane_mode(True)
```

### Mobile Hotspot
```python
# Voice: "Enable mobile hotspot with SSID MyHotspot"
# Python: win11_settings.set_mobile_hotspot(True, ssid="MyHotspot", password="password123")
```

### Configure Proxy
```python
# Voice: "Set proxy to 192.168.1.1 port 8080"
# Python: win11_settings.set_proxy(True, server="192.168.1.1", port=8080)
```

### Flush DNS Cache
```python
# Voice: "Flush DNS cache" / "Clear DNS"
# Python: win11_settings.flush_dns_cache()
```

### Reset Network Adapter
```python
# Voice: "Reset network adapter" / "Reset WiFi adapter"
# Python: win11_settings.reset_network_adapter()
```

---

## 📶 Bluetooth Settings

### Enable/Disable Bluetooth
```python
# Voice: "Turn on Bluetooth" / "Disable Bluetooth"
# Python: win11_settings.set_bluetooth_state(True)
```

### List Bluetooth Devices
```python
# Voice: "List Bluetooth devices" / "Show paired devices"
# Python: win11_settings.list_bluetooth_devices()
```

### Make Bluetooth Discoverable
```python
# Voice: "Make Bluetooth discoverable"
# Python: win11_settings.set_bluetooth_discoverable(True)
```

---

## 🔒 Privacy & Security Settings

### Camera Access Control
```python
# Voice: "Disable camera access" / "Allow camera for Zoom"
# Python: win11_settings.set_camera_access(False)  # Global
# Python: win11_settings.set_camera_access(True, app_specific="Zoom")  # Per-app
```

### Microphone Access Control
```python
# Voice: "Enable microphone access"
# Python: win11_settings.set_microphone_access(True)
```

### Location Access
```python
# Voice: "Disable location access"
# Python: win11_settings.set_location_access(False)
```

### Windows Telemetry
```python
# Voice: "Set telemetry to security level"
# Python: win11_settings.set_telemetry_level("security")
```
**Levels**: "security", "basic", "enhanced", "full"

### Windows Defender
```python
# Voice: "Enable Windows Defender" / "Turn on real-time protection"
# Python: win11_settings.set_windows_defender(True)
```

### Windows Firewall
```python
# Voice: "Enable firewall for all profiles"
# Python: win11_settings.set_firewall_state(True, profile="all")
```
**Profiles**: "domain", "private", "public", "all"

---

## 🎨 Personalization Settings

### Dark Mode / Light Mode
```python
# Voice: "Enable dark mode" / "Switch to dark theme"
# Python: win11_settings.set_dark_mode(True)
```

### Set Wallpaper
```python
# Voice: "Set wallpaper to C:/Images/wallpaper.jpg"
# Python: win11_settings.set_wallpaper("C:/Images/wallpaper.jpg")
```

### Set Accent Color
```python
# Voice: "Set accent color to blue"
# Python: win11_settings.set_accent_color("#0078D4")
```
**Format**: Hex color codes (#RRGGBB)

### Transparency Effects
```python
# Voice: "Enable transparency effects"
# Python: win11_settings.set_transparency_effects(True)
```

### Taskbar Position
```python
# Voice: "Move taskbar to top"
# Python: win11_settings.set_taskbar_position("top")
```
**Positions**: "bottom", "top", "left", "right"
**Note**: Restarts Explorer

### Taskbar Auto-Hide
```python
# Voice: "Enable taskbar auto-hide"
# Python: win11_settings.set_taskbar_auto_hide(True)
```

### Start Menu Layout
```python
# Voice: "Set start menu to more pins layout"
# Python: win11_settings.set_start_menu_layout("more_pins")
```
**Layouts**: "default", "more_pins", "more_recommendations"

---

## ⚙️ System Settings

### Notifications
```python
# Voice: "Disable all notifications" / "Turn off notifications for Chrome"
# Python: win11_settings.set_notifications(False)  # Global
# Python: win11_settings.set_notifications(False, app_specific="Chrome")  # Per-app
```

### Focus Assist
```python
# Voice: "Set focus assist to priority only"
# Python: win11_settings.set_focus_assist("priority_only")
```
**Modes**: "off", "priority_only", "alarms_only"

### Clipboard History
```python
# Voice: "Enable clipboard history"
# Python: win11_settings.set_clipboard_history(True)
```

### Storage Sense
```python
# Voice: "Enable storage sense" / "Turn on automatic cleanup"
# Python: win11_settings.set_storage_sense(True)
```

### Remote Desktop
```python
# Voice: "Enable remote desktop"
# Python: win11_settings.set_remote_desktop(True)
```

### Get Storage Usage
```python
# Voice: "Show storage usage" / "Get disk space"
# Python: win11_settings.get_storage_usage()
```

---

## ♿ Accessibility Settings

### Narrator
```python
# Voice: "Enable narrator" / "Start narrator"
# Python: win11_settings.set_narrator(True)
```

### Magnifier
```python
# Voice: "Enable magnifier at 200 percent zoom"
# Python: win11_settings.set_magnifier(True, zoom_level=200)
```
**Zoom range**: 100% - 1600%

### High Contrast Mode
```python
# Voice: "Enable high contrast mode"
# Python: win11_settings.set_high_contrast(True)
```

### Sticky Keys
```python
# Voice: "Enable sticky keys"
# Python: win11_settings.set_sticky_keys(True)
```

### Filter Keys
```python
# Voice: "Enable filter keys"
# Python: win11_settings.set_filter_keys(True)
```

### Mouse Pointer Size
```python
# Voice: "Set mouse pointer size to 5"
# Python: win11_settings.set_mouse_pointer_size(5)
```
**Size range**: 1-15

---

## 🔄 Windows Update Settings

### Check for Updates
```python
# Voice: "Check for Windows updates"
# Python: win11_settings.check_windows_updates()
```

### Install Updates
```python
# Voice: "Install Windows updates"
# Python: win11_settings.install_windows_updates()
```

### Pause Updates
```python
# Voice: "Pause updates for 14 days"
# Python: win11_settings.pause_windows_updates(days=14)
```
**Range**: 1-35 days

### Resume Updates
```python
# Voice: "Resume Windows updates"
# Python: win11_settings.resume_windows_updates()
```

---

## 📱 Apps & Startup Settings

### List Startup Apps
```python
# Voice: "List startup applications" / "Show startup apps"
# Python: win11_settings.list_startup_apps()
```

### Disable Startup App
```python
# Voice: "Disable Skype from startup"
# Python: win11_settings.disable_startup_app("Skype")
```

### Set Default Browser
```python
# Voice: "Set default browser to Chrome"
# Python: win11_settings.set_default_browser("chrome")
```
**Browsers**: "chrome", "firefox", "edge", "opera"

---

## 🌍 Time & Language Settings

### Set Timezone
```python
# Voice: "Set timezone to Pacific Standard Time"
# Python: win11_settings.set_time_zone("Pacific Standard Time")
```

### List Timezones
```python
# Voice: "List all timezones"
# Python: win11_settings.list_timezones()
```

### Set Date/Time Format
```python
# Voice: "Set short date format"
# Python: win11_settings.set_date_time_format("short_date", "MM/dd/yyyy")
```
**Format types**: "short_date", "long_date", "short_time", "long_time"

---

## 🎮 Gaming Settings

### Game Mode
```python
# Voice: "Enable game mode"
# Python: win11_settings.set_game_mode(True)
```

### Xbox Game Bar
```python
# Voice: "Disable Xbox Game Bar"
# Python: win11_settings.set_game_bar(False)
```

---

## 🔋 Power Settings

### Set Power Plan
```python
# Voice: "Set power plan to high performance"
# Python: win11_settings.set_power_plan("high_performance")
```
**Plans**: "balanced", "high_performance", "power_saver"

### Set Sleep Timeout
```python
# Voice: "Set sleep timeout to 30 minutes when plugged in"
# Python: win11_settings.set_sleep_timeout(minutes=30, on_battery=False)
```

### Set Screen Timeout
```python
# Voice: "Set screen timeout to 10 minutes on battery"
# Python: win11_settings.set_screen_timeout(minutes=10, on_battery=True)
```

---

## 🚀 Advanced System Settings

### Virtual Memory (Page File)
```python
# Voice: "Set virtual memory to 4096 MB on C drive"
# Python: win11_settings.set_virtual_memory(drive="C", initial_mb=2048, maximum_mb=4096)
```

### Performance Options
```python
# Voice: "Set performance to best performance"
# Python: win11_settings.set_performance_options("best_performance")
```
**Options**: "best_appearance", "best_performance", "custom"

### Optimize System Performance
```python
# Voice: "Optimize system performance"
# Python: win11_settings.optimize_system_performance()
```
**Applies**:
- Disables visual effects
- Stops Windows Search indexing
- Disables Superfetch/SysMain
- Sets high performance power plan
- Disables hibernation

---

## 📊 Get All Settings Summary
```python
# Voice: "Get all Windows settings summary"
# Python: win11_settings.get_all_settings_summary()
```
Returns comprehensive summary of:
- Display settings
- Network adapters
- Storage usage
- Bluetooth devices
- Startup applications
- Available updates

---

## Voice Command Examples

### Display
- "Show display information"
- "Set resolution to 1920 by 1080"
- "Enable night light"
- "Set screen scaling to 150 percent"

### Sound
- "List audio devices"
- "Enable Windows Sonic"
- "Set default speaker to headphones"

### Network
- "Turn on WiFi"
- "Enable airplane mode"
- "Start mobile hotspot"
- "Flush DNS cache"
- "Reset network adapter"

### Bluetooth
- "Turn on Bluetooth"
- "Make Bluetooth discoverable"
- "List Bluetooth devices"

### Privacy
- "Disable camera access"
- "Enable microphone access globally"
- "Turn off location services"
- "Enable Windows Defender"

### Personalization
- "Switch to dark mode"
- "Move taskbar to left"
- "Enable transparency effects"
- "Set accent color to red"

### System
- "Disable notifications"
- "Set focus assist to priority only"
- "Enable clipboard history"
- "Turn on storage sense"

### Updates
- "Check for Windows updates"
- "Pause updates for 7 days"
- "Install pending updates"

### Power
- "Set power plan to high performance"
- "Set sleep timeout to 15 minutes"

## Requirements
- **OS**: Windows 11 (Windows 10 partially supported)
- **Permissions**: Administrator privileges for most settings
- **Python**: 3.7+
- **Dependencies**: pywin32, winreg (built-in)

## Notes
⚠️ **Important Considerations**:
1. Many settings require **Administrator** privileges
2. Some settings require **system restart** to take effect
3. Registry modifications are **permanent** - use with caution
4. PowerShell execution policy must allow script execution
5. Some features may not work on Windows 10

## Troubleshooting

### "Access Denied" Errors
- Run the application as Administrator
- Check UAC settings
- Verify user has admin privileges

### Settings Not Taking Effect
- Restart Windows Explorer (or full system)
- Check if feature is available in your Windows edition
- Verify PowerShell execution policy

### PowerShell Command Timeout
- Increase timeout in settings controller
- Check if Windows services are running
- Verify network connectivity for network-related settings

---

## Complete Feature List (100+ Functions)

### Display (8 functions)
1. Get display info
2. Set resolution
3. Set scaling
4. Set night light
5. Set orientation
6. Set refresh rate
7. Enable HDR
8. Configure multiple monitors

### Sound (5 functions)
1. List audio devices
2. Set default device
3. Enable spatial sound
4. Set app volumes
5. Configure audio enhancements

### Network (8 functions)
1. Get network adapters
2. Enable/disable WiFi
3. Enable/disable airplane mode
4. Configure mobile hotspot
5. Set proxy settings
6. Flush DNS cache
7. Reset network adapter
8. Manage VPN connections

### Bluetooth (4 functions)
1. Enable/disable Bluetooth
2. List paired devices
3. Set discoverable
4. Pair new device

### Privacy & Security (7 functions)
1. Camera access control
2. Microphone access control
3. Location access control
4. Set telemetry level
5. Windows Defender control
6. Firewall control
7. App permissions management

### Personalization (10 functions)
1. Dark/Light mode
2. Set wallpaper
3. Set accent color
4. Transparency effects
5. Taskbar position
6. Taskbar auto-hide
7. Start menu layout
8. Desktop icon settings
9. Theme management
10. Font settings

### System (10 functions)
1. Notifications control
2. Focus assist
3. Clipboard history
4. Storage sense
5. Remote desktop
6. Storage usage
7. System restore
8. Environment variables
9. System properties
10. Device manager

### Accessibility (8 functions)
1. Narrator
2. Magnifier
3. High contrast
4. Sticky keys
5. Filter keys
6. Toggle keys
7. Mouse pointer size
8. Keyboard shortcuts

### Windows Update (5 functions)
1. Check updates
2. Install updates
3. Pause updates
4. Resume updates
5. Update history

### Apps & Startup (5 functions)
1. List startup apps
2. Disable startup app
3. Set default apps
4. Manage optional features
5. Uninstall apps

### Time & Language (5 functions)
1. Set timezone
2. List timezones
3. Set date/time format
4. Manage languages
5. Keyboard layouts

### Gaming (3 functions)
1. Game mode
2. Xbox Game Bar
3. Game captures settings

### Power (5 functions)
1. Set power plan
2. Sleep timeout
3. Screen timeout
4. Battery saver
5. Hibernate settings

### Devices (6 functions)
1. Printer management
2. Mouse settings
3. Keyboard settings
4. Pen & touch
5. AutoPlay
6. USB settings

### Advanced (15+ functions)
1. Virtual memory
2. Performance options
3. System optimization
4. Registry backup
5. Service management
6. Scheduled tasks
7. Event viewer
8. Group policy
9. Local security policy
10. User accounts
11. Disk management
12. Device drivers
13. System restore points
14. System file checker
15. Performance monitor

**Total: 100+ comprehensive Windows 11 settings controls!**
