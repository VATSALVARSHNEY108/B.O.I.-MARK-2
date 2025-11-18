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
echo      LAPTOP MASTER CONTROL
echo ========================================
echo.
echo === SYSTEM CONTROL ===
echo 1. System Information
echo 2. Volume Control
echo 3. Power Options
echo 4. Screenshot Tool
echo 5. Battery Info
echo 6. System Restore
echo 7. USB Manager
echo.
echo === FILE MANAGEMENT ===
echo 8. Search Files
echo 9. Organize Downloads
echo 10. Backup Tool
echo 11. Duplicate Finder
echo.
echo === NETWORK ===
echo 12. Network Information
echo 13. WiFi Control
echo 14. Speed Test
echo.
echo === MAINTENANCE ===
echo 15. Disk Cleanup
echo 16. Process Manager
echo 17. Startup Manager
echo 18. Browser Cleaner
echo.
echo === APPS ===
echo 19. Quick Launch
echo 20. Clipboard Manager
echo 21. Quick Notes
echo.
echo 22. Exit
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call system_control\system_info.bat
if "%choice%"=="2" call system_control\volume_control.bat
if "%choice%"=="3" call system_control\power_options.bat
if "%choice%"=="4" call system_control\screenshot_tool.bat
if "%choice%"=="5" call system_control\battery_info.bat
if "%choice%"=="6" call system_control\system_restore.bat
if "%choice%"=="7" call system_control\usb_manager.bat
if "%choice%"=="8" call file_management\search_files.bat
if "%choice%"=="9" call file_management\organize_downloads.bat
if "%choice%"=="10" call file_management\backup_tool.bat
if "%choice%"=="11" call file_management\duplicate_finder.bat
if "%choice%"=="12" call network\network_info.bat
if "%choice%"=="13" call network\wifi_control.bat
if "%choice%"=="14" call network\speed_test.bat
if "%choice%"=="15" call maintenance\disk_cleanup.bat
if "%choice%"=="16" call maintenance\process_manager.bat
if "%choice%"=="17" call maintenance\startup_manager.bat
if "%choice%"=="18" call maintenance\browser_cleaner.bat
if "%choice%"=="19" call apps\quick_launch.bat
if "%choice%"=="20" call apps\clipboard_manager.bat
if "%choice%"=="21" call apps\quick_notes.bat
if "%choice%"=="22" exit

goto menu
