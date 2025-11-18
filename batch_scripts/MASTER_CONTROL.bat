@echo off
REM ==========================================
REM MASTER CONTROL PANEL
REM Main menu to access all batch utilities
REM ==========================================

color 0E
title MASTER CONTROL PANEL

:menu
cls
echo ========================================
echo      WINDOWS MASTER CONTROL
echo ========================================
echo.
echo === CATEGORIES ===
echo.
echo 1.  System Control
echo 2.  Display ^& Appearance
echo 3.  File Management
echo 4.  Network
echo 5.  Maintenance
echo 6.  Security
echo 7.  Performance
echo 8.  Advanced System
echo 9.  Developer Tools
echo 10. Media Control
echo 11. Automation
echo 12. Apps ^& Utilities
echo.
echo 0. Exit
echo.
echo ========================================
set /p category="Select category: "

if "%category%"=="1" goto systemcontrol
if "%category%"=="2" goto display
if "%category%"=="3" goto filemanagement
if "%category%"=="4" goto network
if "%category%"=="5" goto maintenance
if "%category%"=="6" goto security
if "%category%"=="7" goto performance
if "%category%"=="8" goto advanced
if "%category%"=="9" goto developer
if "%category%"=="10" goto media
if "%category%"=="11" goto automation
if "%category%"=="12" goto apps
if "%category%"=="0" exit

goto menu

REM ==========================================
REM SYSTEM CONTROL CATEGORY
REM ==========================================
:systemcontrol
cls
echo ========================================
echo       SYSTEM CONTROL
echo ========================================
echo.
echo 1. System Information
echo 2. Volume Control
echo 3. Power Options
echo 4. Screenshot Tool
echo 5. Battery Info
echo 6. System Restore
echo 7. USB Manager
echo.
echo 0. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call system_control\system_info.bat & goto systemcontrol
if "%choice%"=="2" call system_control\volume_control.bat & goto systemcontrol
if "%choice%"=="3" call system_control\power_options.bat & goto systemcontrol
if "%choice%"=="4" call system_control\screenshot_tool.bat & goto systemcontrol
if "%choice%"=="5" call system_control\battery_info.bat & goto systemcontrol
if "%choice%"=="6" call system_control\system_restore.bat & goto systemcontrol
if "%choice%"=="7" call system_control\usb_manager.bat & goto systemcontrol
if "%choice%"=="0" goto menu

goto systemcontrol

REM ==========================================
REM DISPLAY & APPEARANCE CATEGORY
REM ==========================================
:display
cls
echo ========================================
echo     DISPLAY ^& APPEARANCE
echo ========================================
echo.
echo 1. Brightness Control
echo 2. Resolution Control
echo 3. Screen Rotation
echo 4. Night Light
echo 5. Theme Control (Dark/Light)
echo.
echo 0. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call display\brightness_control.bat & goto display
if "%choice%"=="2" call display\resolution_control.bat & goto display
if "%choice%"=="3" call display\screen_rotation.bat & goto display
if "%choice%"=="4" call display\night_light.bat & goto display
if "%choice%"=="5" call display\theme_control.bat & goto display
if "%choice%"=="0" goto menu

goto display

REM ==========================================
REM FILE MANAGEMENT CATEGORY
REM ==========================================
:filemanagement
cls
echo ========================================
echo      FILE MANAGEMENT
echo ========================================
echo.
echo 1. Search Files
echo 2. Organize Downloads
echo 3. Backup Tool
echo 4. Duplicate Finder
echo.
echo 0. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call file_management\search_files.bat & goto filemanagement
if "%choice%"=="2" call file_management\organize_downloads.bat & goto filemanagement
if "%choice%"=="3" call file_management\backup_tool.bat & goto filemanagement
if "%choice%"=="4" call file_management\duplicate_finder.bat & goto filemanagement
if "%choice%"=="0" goto menu

goto filemanagement

REM ==========================================
REM NETWORK CATEGORY
REM ==========================================
:network
cls
echo ========================================
echo          NETWORK
echo ========================================
echo.
echo 1. Network Information
echo 2. WiFi Control
echo 3. Speed Test
echo.
echo 0. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call network\network_info.bat & goto network
if "%choice%"=="2" call network\wifi_control.bat & goto network
if "%choice%"=="3" call network\speed_test.bat & goto network
if "%choice%"=="0" goto menu

goto network

REM ==========================================
REM MAINTENANCE CATEGORY
REM ==========================================
:maintenance
cls
echo ========================================
echo        MAINTENANCE
echo ========================================
echo.
echo 1. Disk Cleanup
echo 2. Process Manager
echo 3. Startup Manager
echo 4. Browser Cleaner
echo.
echo 0. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call maintenance\disk_cleanup.bat & goto maintenance
if "%choice%"=="2" call maintenance\process_manager.bat & goto maintenance
if "%choice%"=="3" call maintenance\startup_manager.bat & goto maintenance
if "%choice%"=="4" call maintenance\browser_cleaner.bat & goto maintenance
if "%choice%"=="0" goto menu

goto maintenance

REM ==========================================
REM SECURITY CATEGORY
REM ==========================================
:security
cls
echo ========================================
echo         SECURITY
echo ========================================
echo.
echo 1. Firewall Control
echo 2. Windows Defender Control
echo 3. User Account Management
echo 4. Encryption Tools (BitLocker/EFS)
echo.
echo 0. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call security\firewall_control.bat & goto security
if "%choice%"=="2" call security\defender_control.bat & goto security
if "%choice%"=="3" call security\user_accounts.bat & goto security
if "%choice%"=="4" call security\encryption_tools.bat & goto security
if "%choice%"=="0" goto menu

goto security

REM ==========================================
REM PERFORMANCE CATEGORY
REM ==========================================
:performance
cls
echo ========================================
echo        PERFORMANCE
echo ========================================
echo.
echo 1. RAM Optimizer
echo 2. Temp Files Cleaner
echo 3. Service Manager
echo 4. Disk Defragmentation
echo.
echo 0. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call performance\ram_optimizer.bat & goto performance
if "%choice%"=="2" call performance\temp_cleaner.bat & goto performance
if "%choice%"=="3" call performance\service_manager.bat & goto performance
if "%choice%"=="4" call performance\disk_defrag.bat & goto performance
if "%choice%"=="0" goto menu

goto performance

REM ==========================================
REM ADVANCED SYSTEM CATEGORY
REM ==========================================
:advanced
cls
echo ========================================
echo      ADVANCED SYSTEM
echo ========================================
echo.
echo 1. Registry Backup ^& Restore
echo 2. Event Viewer Tools
echo 3. Task Scheduler Manager
echo 4. Driver Manager
echo.
echo 0. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call advanced_system\registry_backup.bat & goto advanced
if "%choice%"=="2" call advanced_system\event_viewer.bat & goto advanced
if "%choice%"=="3" call advanced_system\task_scheduler.bat & goto advanced
if "%choice%"=="4" call advanced_system\driver_manager.bat & goto advanced
if "%choice%"=="0" goto menu

goto advanced

REM ==========================================
REM DEVELOPER TOOLS CATEGORY
REM ==========================================
:developer
cls
echo ========================================
echo       DEVELOPER TOOLS
echo ========================================
echo.
echo 1. Git Tools
echo 2. Environment Variables Manager
echo 3. Python Tools
echo 4. Node.js Tools
echo.
echo 0. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call developer\git_tools.bat & goto developer
if "%choice%"=="2" call developer\environment_vars.bat & goto developer
if "%choice%"=="3" call developer\python_tools.bat & goto developer
if "%choice%"=="4" call developer\node_tools.bat & goto developer
if "%choice%"=="0" goto menu

goto developer

REM ==========================================
REM MEDIA CONTROL CATEGORY
REM ==========================================
:media
cls
echo ========================================
echo       MEDIA CONTROL
echo ========================================
echo.
echo 1. Audio Device Control
echo 2. Webcam Control
echo 3. Display Mirroring ^& Projection
echo.
echo 0. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call media\audio_device_control.bat & goto media
if "%choice%"=="2" call media\webcam_control.bat & goto media
if "%choice%"=="3" call media\display_mirror.bat & goto media
if "%choice%"=="0" goto menu

goto media

REM ==========================================
REM AUTOMATION CATEGORY
REM ==========================================
:automation
cls
echo ========================================
echo        AUTOMATION
echo ========================================
echo.
echo 1. Auto Shutdown Scheduler
echo 2. Quick App Launcher
echo 3. Macro Recorder
echo 4. Folder Watcher
echo.
echo 0. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call automation\auto_shutdown.bat & goto automation
if "%choice%"=="2" call automation\app_launcher.bat & goto automation
if "%choice%"=="3" call automation\macro_recorder.bat & goto automation
if "%choice%"=="4" call automation\folder_watcher.bat & goto automation
if "%choice%"=="0" goto menu

goto automation

REM ==========================================
REM APPS & UTILITIES CATEGORY
REM ==========================================
:apps
cls
echo ========================================
echo      APPS ^& UTILITIES
echo ========================================
echo.
echo 1. Quick Launch
echo 2. Clipboard Manager
echo 3. Quick Notes
echo.
echo 0. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call apps\quick_launch.bat & goto apps
if "%choice%"=="2" call apps\clipboard_manager.bat & goto apps
if "%choice%"=="3" call apps\quick_notes.bat & goto apps
if "%choice%"=="0" goto menu

goto apps
