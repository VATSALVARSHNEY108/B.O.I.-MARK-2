@echo off
setlocal EnableDelayedExpansion

:: ================================================
:: Windows 11 System Settings Automation
:: ================================================

:menu
cls
echo ================================================
echo    Windows 11 System Settings Controller
echo ================================================
echo.
echo [1] Notifications
echo [2] Focus Assist
echo [3] Clipboard History
echo [4] Storage Sense
echo [5] Remote Desktop
echo [6] Power ^& Sleep
echo [7] Startup Apps
echo [8] Date ^& Time
echo [9] Back to Main Menu
echo.
set /p choice="Select option (1-9): "

if "%choice%"=="1" goto notifications
if "%choice%"=="2" goto focus_assist
if "%choice%"=="3" goto clipboard
if "%choice%"=="4" goto storage
if "%choice%"=="5" goto remote_desktop
if "%choice%"=="6" goto power_sleep
if "%choice%"=="7" goto startup_apps
if "%choice%"=="8" goto datetime
if "%choice%"=="9" exit /b
goto menu

:notifications
cls
echo ================================================
echo Notification Settings
echo ================================================
echo.
echo [1] Enable All Notifications
echo [2] Disable All Notifications
echo [3] Open Notification Settings
echo.
set /p notif_choice="Select option (1-3): "

if "%notif_choice%"=="1" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\PushNotifications" /v ToastEnabled /t REG_DWORD /d 1 /f
    echo All notifications enabled!
) else if "%notif_choice%"=="2" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\PushNotifications" /v ToastEnabled /t REG_DWORD /d 0 /f
    echo All notifications disabled!
) else if "%notif_choice%"=="3" (
    start ms-settings:notifications
)
pause
goto menu

:focus_assist
cls
echo ================================================
echo Focus Assist Settings
echo ================================================
echo.
echo [1] Turn OFF Focus Assist
echo [2] Priority Only
echo [3] Alarms Only
echo [4] Open Focus Assist Settings
echo.
set /p focus_choice="Select option (1-4): "

if "%focus_choice%"=="1" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\CloudStore\Store\Cache\DefaultAccount\$$windows.data.notifications.quiethourssettings\Current" /v Data /t REG_BINARY /d 02000000d76f77fb4e45d60198f6a3d9e168d801000000000000000000000000 /f
    echo Focus Assist turned OFF!
) else if "%focus_choice%"=="2" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\CloudStore\Store\Cache\DefaultAccount\$$windows.data.notifications.quiethourssettings\Current" /v Data /t REG_BINARY /d 02000000d76f77fb4e45d60198f6a3d9e168d801000000000000000001000000 /f
    echo Focus Assist set to Priority Only!
) else if "%focus_choice%"=="3" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\CloudStore\Store\Cache\DefaultAccount\$$windows.data.notifications.quiethourssettings\Current" /v Data /t REG_BINARY /d 02000000d76f77fb4e45d60198f6a3d9e168d801000000000000000002000000 /f
    echo Focus Assist set to Alarms Only!
) else if "%focus_choice%"=="4" (
    start ms-settings:quiethours
)
pause
goto menu

:clipboard
cls
echo ================================================
echo Clipboard History Settings
echo ================================================
echo.
echo [1] Enable Clipboard History
echo [2] Disable Clipboard History
echo [3] Clear Clipboard History
echo [4] Open Clipboard Settings
echo.
set /p clip_choice="Select option (1-4): "

if "%clip_choice%"=="1" (
    reg add "HKCU\SOFTWARE\Microsoft\Clipboard" /v EnableClipboardHistory /t REG_DWORD /d 1 /f
    echo Clipboard history enabled!
) else if "%clip_choice%"=="2" (
    reg add "HKCU\SOFTWARE\Microsoft\Clipboard" /v EnableClipboardHistory /t REG_DWORD /d 0 /f
    echo Clipboard history disabled!
) else if "%clip_choice%"=="3" (
    echo Clearing clipboard history...
    echo off | clip
    echo Clipboard cleared!
) else if "%clip_choice%"=="4" (
    start ms-settings:clipboard
)
pause
goto menu

:storage
cls
echo ================================================
echo Storage Sense Settings
echo ================================================
echo.
echo [1] Enable Storage Sense
echo [2] Disable Storage Sense
echo [3] Run Storage Sense Now
echo [4] Open Storage Settings
echo.
set /p storage_choice="Select option (1-4): "

if "%storage_choice%"=="1" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\StorageSense\Parameters\StoragePolicy" /v 01 /t REG_DWORD /d 1 /f
    echo Storage Sense enabled!
) else if "%storage_choice%"=="2" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\StorageSense\Parameters\StoragePolicy" /v 01 /t REG_DWORD /d 0 /f
    echo Storage Sense disabled!
) else if "%storage_choice%"=="3" (
    echo Running Storage Sense...
    cleanmgr /sagerun:1
) else if "%storage_choice%"=="4" (
    start ms-settings:storagesense
)
pause
goto menu

:remote_desktop
cls
echo ================================================
echo Remote Desktop Settings
echo ================================================
echo.
echo [1] Enable Remote Desktop
echo [2] Disable Remote Desktop
echo [3] Open Remote Desktop Settings
echo.
set /p rdp_choice="Select option (1-3): "

if "%rdp_choice%"=="1" (
    reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
    netsh advfirewall firewall set rule group="remote desktop" new enable=Yes
    echo Remote Desktop enabled!
) else if "%rdp_choice%"=="2" (
    reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 1 /f
    echo Remote Desktop disabled!
) else if "%rdp_choice%"=="3" (
    start ms-settings:remotedesktop
)
pause
goto menu

:power_sleep
cls
echo ================================================
echo Power ^& Sleep Settings
echo ================================================
echo.
echo [1] Never Sleep
echo [2] Sleep After 15 Minutes
echo [3] Sleep After 30 Minutes
echo [4] Sleep After 1 Hour
echo [5] Open Power Settings
echo.
set /p power_choice="Select option (1-5): "

if "%power_choice%"=="1" (
    powercfg -change -standby-timeout-ac 0
    powercfg -change -standby-timeout-dc 0
    echo Sleep disabled!
) else if "%power_choice%"=="2" (
    powercfg -change -standby-timeout-ac 15
    powercfg -change -standby-timeout-dc 15
    echo Sleep set to 15 minutes!
) else if "%power_choice%"=="3" (
    powercfg -change -standby-timeout-ac 30
    powercfg -change -standby-timeout-dc 30
    echo Sleep set to 30 minutes!
) else if "%power_choice%"=="4" (
    powercfg -change -standby-timeout-ac 60
    powercfg -change -standby-timeout-dc 60
    echo Sleep set to 1 hour!
) else if "%power_choice%"=="5" (
    start ms-settings:powersleep
)
pause
goto menu

:startup_apps
cls
echo ================================================
echo Startup Apps Management
echo ================================================
echo.
echo Opening Startup Apps settings...
start ms-settings:startupapps
pause
goto menu

:datetime
cls
echo ================================================
echo Date ^& Time Settings
echo ================================================
echo.
echo [1] Enable Auto Time Sync
echo [2] Disable Auto Time Sync
echo [3] Sync Time Now
echo [4] Open Date ^& Time Settings
echo.
set /p time_choice="Select option (1-4): "

if "%time_choice%"=="1" (
    reg add "HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Parameters" /v Type /t REG_SZ /d NTP /f
    net start w32time
    w32tm /config /syncfromflags:manual /manualpeerlist:"time.windows.com"
    echo Auto time sync enabled!
) else if "%time_choice%"=="2" (
    net stop w32time
    echo Auto time sync disabled!
) else if "%time_choice%"=="3" (
    w32tm /resync
    echo Time synchronized!
) else if "%time_choice%"=="4" (
    start ms-settings:dateandtime
)
pause
goto menu
