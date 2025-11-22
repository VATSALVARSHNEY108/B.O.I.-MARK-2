================================================================================
                    BOI QUICK ACCESS BATCH FILES
                     Individual Feature Launchers
================================================================================

OVERVIEW:
These batch files provide direct access to individual BOI features without 
needing to go through menus. Each file performs a specific action and can be 
run independently.

LOCATION:
batch_scripts/quick_access/

HOW TO USE:
1. Double-click any .bat file to run that specific feature
2. Run QUICK_ACCESS_MENU.bat for an organized menu interface
3. Create desktop shortcuts to your most-used batch files for instant access

================================================================================
                           AVAILABLE BATCH FILES
================================================================================

BLUETOOTH CONTROLS:
------------------
bluetooth_on.bat              - Turn Bluetooth ON
bluetooth_off.bat             - Turn Bluetooth OFF
bluetooth_status.bat          - Check Bluetooth status and paired devices
bluetooth_settings.bat        - Open Windows Bluetooth settings

WIFI CONTROLS:
-------------
wifi_on.bat                   - Turn WiFi ON
wifi_off.bat                  - Turn WiFi OFF
wifi_status.bat               - Check WiFi status and available networks
wifi_settings.bat             - Open Windows WiFi settings

VOLUME CONTROLS:
---------------
volume_up.bat                 - Increase volume by one step
volume_down.bat               - Decrease volume by one step
volume_mute.bat               - Toggle mute/unmute
volume_set_25.bat             - Set volume to ~25% (approximate)
volume_set_50.bat             - Set volume to ~50% (approximate)
volume_set_75.bat             - Set volume to ~75% (approximate)
volume_set_100.bat            - Set volume to 100% (maximum)
NOTE: Volume levels are approximate due to system variations.

BRIGHTNESS CONTROLS:
-------------------
brightness_up.bat             - Set brightness to maximum (100%)
brightness_down.bat           - Set brightness to low (30%)
brightness_set_25.bat         - Set brightness to 25%
brightness_set_50.bat         - Set brightness to 50%
brightness_set_75.bat         - Set brightness to 75%
brightness_set_100.bat        - Set brightness to 100%
NOTE: Brightness control requires WMI support. Opens display settings as fallback.

POWER OPTIONS:
-------------
power_shutdown.bat            - Shutdown computer (requires confirmation, 10s delay)
power_restart.bat             - Restart computer (requires confirmation, 10s delay)
power_sleep.bat               - Put computer to sleep
power_hibernate.bat           - Hibernate computer
power_lock.bat                - Lock computer screen
power_cancel_shutdown.bat    - Cancel scheduled shutdown/restart

SYSTEM MONITORING:
-----------------
system_cpu_usage.bat          - View CPU usage and top processes
system_ram_usage.bat          - View RAM usage and memory-consuming processes
system_disk_usage.bat         - View disk space usage for all drives
system_battery_status.bat    - Check battery status (laptops only)
system_full_info.bat          - View complete system information
system_network_info.bat       - View network configuration and connections

QUICK APP LAUNCHERS:
-------------------
app_notepad.bat               - Launch Notepad
app_calculator.bat            - Launch Calculator
app_chrome.bat                - Launch Google Chrome
app_task_manager.bat          - Launch Task Manager
app_file_explorer.bat         - Launch File Explorer
app_cmd.bat                   - Launch Command Prompt
app_powershell.bat            - Launch PowerShell
app_control_panel.bat         - Launch Control Panel
app_settings.bat              - Launch Windows Settings

MASTER MENU:
-----------
QUICK_ACCESS_MENU.bat         - Interactive menu to access all features

================================================================================
                              TIPS & TRICKS
================================================================================

CREATING DESKTOP SHORTCUTS:
1. Right-click on any .bat file
2. Select "Send to" > "Desktop (create shortcut)"
3. Rename the shortcut to something simple (e.g., "Bluetooth OFF")
4. Optionally, right-click the shortcut > Properties > Change Icon

KEYBOARD SHORTCUTS:
- Create shortcuts with hotkeys by setting them in shortcut properties
- Example: Right-click shortcut > Properties > Shortcut Key

TROUBLESHOOTING:
- If Bluetooth/WiFi commands fail, they will automatically open Windows settings
- All batch files include error handling and user feedback
- Some features require administrator privileges
- Volume preset levels are approximate and may vary by system
- Brightness controls require WMI support (laptops); desktops open display settings
- Shutdown/Restart require confirmation to prevent accidental execution

INTEGRATION WITH BOI:
- These batch files complement the main BOI AI system
- Use them when you want instant access without voice/text commands
- Perfect for creating custom automation workflows

================================================================================
                              EXAMPLES
================================================================================

QUICK BLUETOOTH TOGGLE:
- Create two desktop shortcuts: bluetooth_on.bat and bluetooth_off.bat
- Assign keyboard shortcuts (e.g., Ctrl+Alt+B for ON, Ctrl+Shift+B for OFF)
- Toggle Bluetooth instantly with keyboard!

POWER USER WORKFLOW:
1. Run system_cpu_usage.bat to check performance
2. If high usage, run app_task_manager.bat to investigate
3. Kill problematic processes
4. Verify with system_ram_usage.bat

PRESENTATION MODE:
1. Run brightness_set_100.bat (full brightness)
2. Run volume_set_75.bat (audible volume)
3. Run power_cancel_shutdown.bat (ensure no interruptions)

BEDTIME ROUTINE:
1. Run brightness_set_25.bat (dim screen)
2. Run volume_set_25.bat (lower volume)
3. Run wifi_off.bat (save battery)
4. Run power_sleep.bat when ready

================================================================================
                           ADDITIONAL NOTES
================================================================================

COMPATIBILITY:
- Designed for Windows 10/11
- Some features may require administrator rights
- Bluetooth/WiFi controls use Windows Runtime and PowerShell

SECURITY:
- All batch files are safe and only perform the stated actions
- No data is collected or transmitted
- Review the code in any .bat file with a text editor

CUSTOMIZATION:
- Feel free to edit any batch file to customize behavior
- Use a text editor to modify timings, messages, or actions
- Backup files before making changes

FOR MORE HELP:
- Run the main BOI AI application (vatsal.py)
- Type "help" for comprehensive command reference
- Check ALL_COMMANDS_REFERENCE.txt for 275+ features

================================================================================
                          END OF DOCUMENTATION
================================================================================

Created as part of the BOI (Barely Obeys Instructions) Desktop Automation
Project by Vatsal

Enjoy your quick access to system features!
