# Windows Control Utilities - Complete Batch Script Collection

A comprehensive collection of 40+ batch files to control and manage every aspect of Windows.

## 📂 Quick Navigation

Run **`MASTER_CONTROL.bat`** to access all utilities through an organized menu system.

## 🎯 Complete Feature List

### 1️⃣ Display & Appearance (5 utilities)
- **Brightness Control** - Adjust screen brightness (10%, 25%, 50%, 75%, 100%, custom)
- **Resolution Control** - Change screen resolution (1080p, 720p, 2K, 4K)
- **Screen Rotation** - Rotate display (0°, 90°, 180°, 270°)
- **Night Light** - Enable/disable blue light filter
- **Theme Control** - Switch Dark/Light modes instantly

### 2️⃣ Security (4 utilities)
- **Firewall Control** - Enable/disable firewall, manage rules, block/allow apps
- **Windows Defender** - Quick/full scans, update definitions, manage exclusions
- **User Accounts** - Create/delete users, change passwords, manage permissions
- **Encryption Tools** - BitLocker management, file/folder encryption (EFS)

### 3️⃣ Performance (4 utilities)
- **RAM Optimizer** - Free memory, close high-memory apps, gaming mode
- **Temp Cleaner** - Remove temp files, clear cache, clean Windows Update files
- **Service Manager** - Start/stop/disable Windows services
- **Disk Defrag** - Analyze and defragment drives, optimize SSDs

### 4️⃣ Advanced System (4 utilities)
- **Registry Backup** - Backup/restore entire registry or specific keys
- **Event Viewer** - View system/app errors, security logs, export logs
- **Task Scheduler** - Create/delete/manage scheduled tasks
- **Driver Manager** - List drivers, backup all drivers, check for updates

### 5️⃣ Developer Tools (4 utilities)
- **Git Tools** - Status, commit, push, pull, branch management
- **Environment Variables** - View/edit PATH, create system/user variables
- **Python Tools** - Package management, virtual environments, pip operations
- **Node.js Tools** - npm commands, package installation, project initialization

### 6️⃣ Media Control (3 utilities)
- **Audio Devices** - Switch playback/recording devices, volume control
- **Webcam Control** - Enable/disable camera, privacy settings
- **Display Mirror** - Screen projection modes (duplicate, extend, second screen only)

### 7️⃣ Automation (4 utilities)
- **Auto Shutdown** - Schedule shutdown (custom time, timer, cancel)
- **App Launcher** - Launch multiple apps at once with presets (Work, Dev, Gaming, Media)
- **Macro Recorder** - Record and replay command sequences
- **Folder Watcher** - Monitor folders for changes, auto-organize downloads

### 8️⃣ System Control (7 utilities)
- System Information
- Volume Control
- Power Options
- Screenshot Tool
- Battery Info
- System Restore
- USB Manager

### 9️⃣ File Management (4 utilities)
- Search Files
- Organize Downloads
- Backup Tool
- Duplicate Finder

### 🔟 Network (3 utilities)
- Network Information
- WiFi Control
- Speed Test

### 1️⃣1️⃣ Maintenance (4 utilities)
- Disk Cleanup
- Process Manager
- Startup Manager
- Browser Cleaner

### 1️⃣2️⃣ Apps & Utilities (3 utilities)
- Quick Launch
- Clipboard Manager
- Quick Notes

## 🚀 Getting Started

### Method 1: Master Control (Recommended)
```batch
cd batch_scripts
MASTER_CONTROL.bat
```
Navigate through organized categories using number keys.

### Method 2: Direct Access
```batch
cd batch_scripts\display
brightness_control.bat
```
Run any utility directly from its category folder.

## 📋 Common Use Cases

### Quick System Optimization
1. Performance → RAM Optimizer → Clean cache
2. Performance → Temp Cleaner → Clean ALL
3. Maintenance → Disk Cleanup

### Setup Dark Mode + Night Light
1. Display & Appearance → Theme Control → Dark Mode
2. Display & Appearance → Night Light → Enable

### Developer Environment Setup
1. Developer Tools → Git Tools → Clone repository
2. Developer Tools → Python Tools → Create virtual environment
3. Developer Tools → Environment Variables → Add to PATH

### Security Checkup
1. Security → Windows Defender → Quick Scan
2. Security → Firewall Control → View Status
3. Advanced System → Event Viewer → View Errors

### Auto-Organize Downloads
1. Automation → Folder Watcher → Auto-Organize Downloads
   (Automatically sorts files by type: Images, Videos, Documents, etc.)

## ⚠️ Important Safety Notes

### Requires Administrator for:
- Firewall Control
- Windows Defender operations
- User Account Management
- Service Manager
- Driver operations
- Registry modifications

### Always Backup Before:
- Registry operations
- System service changes
- Driver updates
- BitLocker encryption

## 🎯 Pro Tips

1. **Create Desktop Shortcuts** for frequently used utilities
2. **Pin MASTER_CONTROL.bat** to taskbar for quick access
3. **Schedule maintenance tasks** using Task Scheduler utility
4. **Backup registry** before installing new software
5. **Use automation** for repetitive daily tasks

## 🔒 Security Best Practices

✅ **DO:**
- Review scripts before running
- Keep Windows updated
- Create system restore points
- Backup important data regularly

❌ **DON'T:**
- Run unknown batch files
- Disable security features permanently
- Delete important system services
- Modify registry without knowledge

## 🛠️ Troubleshooting

**"Access Denied" errors:**
- Run as Administrator (Right-click → Run as administrator)

**Scripts not working:**
- Check Windows version (designed for Windows 10/11)
- Verify PowerShell is enabled
- Ensure paths are correct

**Changes not visible:**
- Restart the application
- Log out and log back in
- Restart Windows if needed

## 📚 Technical Details

### Requirements
- **OS:** Windows 10 or Windows 11
- **PowerShell:** Enabled (default)
- **Permissions:** Standard user (Administrator for some features)

### File Structure
```
batch_scripts/
├── MASTER_CONTROL.bat
├── display/
│   ├── brightness_control.bat
│   ├── resolution_control.bat
│   ├── screen_rotation.bat
│   ├── night_light.bat
│   └── theme_control.bat
├── security/
│   ├── firewall_control.bat
│   ├── defender_control.bat
│   ├── user_accounts.bat
│   └── encryption_tools.bat
├── performance/
│   ├── ram_optimizer.bat
│   ├── temp_cleaner.bat
│   ├── service_manager.bat
│   └── disk_defrag.bat
├── advanced_system/
│   ├── registry_backup.bat
│   ├── event_viewer.bat
│   ├── task_scheduler.bat
│   └── driver_manager.bat
├── developer/
│   ├── git_tools.bat
│   ├── environment_vars.bat
│   ├── python_tools.bat
│   └── node_tools.bat
├── media/
│   ├── audio_device_control.bat
│   ├── webcam_control.bat
│   └── display_mirror.bat
├── automation/
│   ├── auto_shutdown.bat
│   ├── app_launcher.bat
│   ├── macro_recorder.bat
│   └── folder_watcher.bat
└── [existing categories...]
```

## 📝 Customization

Add your own scripts by:
1. Creating a `.bat` file in the appropriate category folder
2. Following the existing format for consistency
3. Updating the category menu in MASTER_CONTROL.bat

## 🌟 Feature Highlights

- **40+ utilities** covering all Windows functions
- **Organized categories** for easy navigation
- **Interactive menus** with clear instructions
- **Error handling** and confirmations for dangerous operations
- **PowerShell integration** for advanced features
- **No installation required** - just run the batch files

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review Windows Event Viewer for errors
- Ensure you have proper permissions
- Verify Windows version compatibility

---

**Total Utilities:** 45+ batch scripts
**Categories:** 12 organized sections
**Compatibility:** Windows 10/11
**Installation:** Not required - portable scripts

**Made with ❤️ for Windows power users**
