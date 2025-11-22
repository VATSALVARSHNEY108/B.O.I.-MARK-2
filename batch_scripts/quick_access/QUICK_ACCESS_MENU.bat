@echo off
title BOI Quick Access Menu
color 0B

:main_menu
cls
echo ========================================================
echo           BOI QUICK ACCESS MENU
echo           Individual Feature Launcher
echo ========================================================
echo.
echo  [1] Bluetooth Controls
echo  [2] WiFi Controls
echo  [3] Volume Controls
echo  [4] Brightness Controls
echo  [5] Power Options
echo  [6] System Monitoring
echo  [7] Quick App Launchers
echo  [8] All Features List
echo  [0] Exit
echo.
echo ========================================================
set /p choice="Select category (0-8): "

if "%choice%"=="1" goto bluetooth_menu
if "%choice%"=="2" goto wifi_menu
if "%choice%"=="3" goto volume_menu
if "%choice%"=="4" goto brightness_menu
if "%choice%"=="5" goto power_menu
if "%choice%"=="6" goto system_menu
if "%choice%"=="7" goto app_menu
if "%choice%"=="8" goto all_features
if "%choice%"=="0" exit
goto main_menu

:bluetooth_menu
cls
echo ========================================================
echo           BLUETOOTH CONTROLS
echo ========================================================
echo.
echo  [1] Turn Bluetooth ON
echo  [2] Turn Bluetooth OFF
echo  [3] Check Bluetooth Status
echo  [4] Open Bluetooth Settings
echo  [0] Back to Main Menu
echo.
set /p bt_choice="Select option: "

if "%bt_choice%"=="1" call bluetooth_on.bat
if "%bt_choice%"=="2" call bluetooth_off.bat
if "%bt_choice%"=="3" call bluetooth_status.bat
if "%bt_choice%"=="4" call bluetooth_settings.bat
if "%bt_choice%"=="0" goto main_menu
goto bluetooth_menu

:wifi_menu
cls
echo ========================================================
echo           WIFI CONTROLS
echo ========================================================
echo.
echo  [1] Turn WiFi ON
echo  [2] Turn WiFi OFF
echo  [3] Check WiFi Status
echo  [4] Open WiFi Settings
echo  [0] Back to Main Menu
echo.
set /p wifi_choice="Select option: "

if "%wifi_choice%"=="1" call wifi_on.bat
if "%wifi_choice%"=="2" call wifi_off.bat
if "%wifi_choice%"=="3" call wifi_status.bat
if "%wifi_choice%"=="4" call wifi_settings.bat
if "%wifi_choice%"=="0" goto main_menu
goto wifi_menu

:volume_menu
cls
echo ========================================================
echo           VOLUME CONTROLS
echo ========================================================
echo.
echo  [1] Volume Up
echo  [2] Volume Down
echo  [3] Mute/Unmute (Toggle)
echo  [4] Set Volume to 25%%
echo  [5] Set Volume to 50%%
echo  [6] Set Volume to 75%%
echo  [7] Set Volume to 100%%
echo  [0] Back to Main Menu
echo.
set /p vol_choice="Select option: "

if "%vol_choice%"=="1" call volume_up.bat
if "%vol_choice%"=="2" call volume_down.bat
if "%vol_choice%"=="3" call volume_mute.bat
if "%vol_choice%"=="4" call volume_set_25.bat
if "%vol_choice%"=="5" call volume_set_50.bat
if "%vol_choice%"=="6" call volume_set_75.bat
if "%vol_choice%"=="7" call volume_set_100.bat
if "%vol_choice%"=="0" goto main_menu
goto volume_menu

:brightness_menu
cls
echo ========================================================
echo           BRIGHTNESS CONTROLS
echo ========================================================
echo.
echo  [1] Brightness Up (100%%)
echo  [2] Brightness Down (30%%)
echo  [3] Set Brightness to 25%%
echo  [4] Set Brightness to 50%%
echo  [5] Set Brightness to 75%%
echo  [6] Set Brightness to 100%%
echo  [0] Back to Main Menu
echo.
set /p bright_choice="Select option: "

if "%bright_choice%"=="1" call brightness_up.bat
if "%bright_choice%"=="2" call brightness_down.bat
if "%bright_choice%"=="3" call brightness_set_25.bat
if "%bright_choice%"=="4" call brightness_set_50.bat
if "%bright_choice%"=="5" call brightness_set_75.bat
if "%bright_choice%"=="6" call brightness_set_100.bat
if "%bright_choice%"=="0" goto main_menu
goto brightness_menu

:power_menu
cls
echo ========================================================
echo           POWER OPTIONS
echo ========================================================
echo.
echo  [1] Shutdown Computer (10s delay)
echo  [2] Restart Computer (10s delay)
echo  [3] Sleep Computer
echo  [4] Hibernate Computer
echo  [5] Lock Computer
echo  [6] Cancel Shutdown/Restart
echo  [0] Back to Main Menu
echo.
set /p power_choice="Select option: "

if "%power_choice%"=="1" call power_shutdown.bat
if "%power_choice%"=="2" call power_restart.bat
if "%power_choice%"=="3" call power_sleep.bat
if "%power_choice%"=="4" call power_hibernate.bat
if "%power_choice%"=="5" call power_lock.bat
if "%power_choice%"=="6" call power_cancel_shutdown.bat
if "%power_choice%"=="0" goto main_menu
goto power_menu

:system_menu
cls
echo ========================================================
echo           SYSTEM MONITORING
echo ========================================================
echo.
echo  [1] Check CPU Usage
echo  [2] Check RAM Usage
echo  [3] Check Disk Usage
echo  [4] Check Battery Status
echo  [5] Full System Information
echo  [6] Network Information
echo  [0] Back to Main Menu
echo.
set /p sys_choice="Select option: "

if "%sys_choice%"=="1" call system_cpu_usage.bat
if "%sys_choice%"=="2" call system_ram_usage.bat
if "%sys_choice%"=="3" call system_disk_usage.bat
if "%sys_choice%"=="4" call system_battery_status.bat
if "%sys_choice%"=="5" call system_full_info.bat
if "%sys_choice%"=="6" call system_network_info.bat
if "%sys_choice%"=="0" goto main_menu
goto system_menu

:app_menu
cls
echo ========================================================
echo           QUICK APP LAUNCHERS
echo ========================================================
echo.
echo  [1] Notepad
echo  [2] Calculator
echo  [3] Google Chrome
echo  [4] Task Manager
echo  [5] File Explorer
echo  [6] Command Prompt
echo  [7] PowerShell
echo  [8] Control Panel
echo  [9] Windows Settings
echo  [0] Back to Main Menu
echo.
set /p app_choice="Select option: "

if "%app_choice%"=="1" call app_notepad.bat
if "%app_choice%"=="2" call app_calculator.bat
if "%app_choice%"=="3" call app_chrome.bat
if "%app_choice%"=="4" call app_task_manager.bat
if "%app_choice%"=="5" call app_file_explorer.bat
if "%app_choice%"=="6" call app_cmd.bat
if "%app_choice%"=="7" call app_powershell.bat
if "%app_choice%"=="8" call app_control_panel.bat
if "%app_choice%"=="9" call app_settings.bat
if "%app_choice%"=="0" goto main_menu
goto app_menu

:all_features
cls
echo ========================================================
echo           ALL QUICK ACCESS FEATURES
echo ========================================================
echo.
echo BLUETOOTH:
echo   - bluetooth_on.bat
echo   - bluetooth_off.bat
echo   - bluetooth_status.bat
echo   - bluetooth_settings.bat
echo.
echo WIFI:
echo   - wifi_on.bat
echo   - wifi_off.bat
echo   - wifi_status.bat
echo   - wifi_settings.bat
echo.
echo VOLUME:
echo   - volume_up.bat
echo   - volume_down.bat
echo   - volume_mute.bat
echo   - volume_set_25.bat / 50 / 75 / 100
echo.
echo BRIGHTNESS:
echo   - brightness_up.bat
echo   - brightness_down.bat
echo   - brightness_set_25.bat / 50 / 75 / 100
echo.
echo POWER:
echo   - power_shutdown.bat
echo   - power_restart.bat
echo   - power_sleep.bat
echo   - power_hibernate.bat
echo   - power_lock.bat
echo   - power_cancel_shutdown.bat
echo.
echo SYSTEM MONITORING:
echo   - system_cpu_usage.bat
echo   - system_ram_usage.bat
echo   - system_disk_usage.bat
echo   - system_battery_status.bat
echo   - system_full_info.bat
echo   - system_network_info.bat
echo.
echo APPS:
echo   - app_notepad.bat
echo   - app_calculator.bat
echo   - app_chrome.bat
echo   - app_task_manager.bat
echo   - app_file_explorer.bat
echo   - app_cmd.bat
echo   - app_powershell.bat
echo   - app_control_panel.bat
echo   - app_settings.bat
echo.
echo ========================================================
echo You can run any of these .bat files directly!
echo They are located in: batch_scripts/quick_access/
echo ========================================================
echo.
pause
goto main_menu
