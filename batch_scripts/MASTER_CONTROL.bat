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
echo.
echo === FILE MANAGEMENT ===
echo 4. Search Files
echo 5. Organize Downloads
echo.
echo === NETWORK ===
echo 6. Network Information
echo 7. WiFi Control
echo.
echo === MAINTENANCE ===
echo 8. Disk Cleanup
echo 9. Process Manager
echo.
echo === APPS ===
echo 10. Quick Launch
echo.
echo 11. Exit
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call system_control\system_info.bat
if "%choice%"=="2" call system_control\volume_control.bat
if "%choice%"=="3" call system_control\power_options.bat
if "%choice%"=="4" call file_management\search_files.bat
if "%choice%"=="5" call file_management\organize_downloads.bat
if "%choice%"=="6" call network\network_info.bat
if "%choice%"=="7" call network\wifi_control.bat
if "%choice%"=="8" call maintenance\disk_cleanup.bat
if "%choice%"=="9" call maintenance\process_manager.bat
if "%choice%"=="10" call apps\quick_launch.bat
if "%choice%"=="11" exit

goto menu
