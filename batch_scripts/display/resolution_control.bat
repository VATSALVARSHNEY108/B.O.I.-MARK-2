@echo off
REM ==========================================
REM DISPLAY RESOLUTION CONTROL
REM Change screen resolution settings
REM ==========================================

color 0B
title Resolution Control

:menu
cls
echo ========================================
echo     DISPLAY RESOLUTION CONTROL
echo ========================================
echo.
echo 1. Set to 1920x1080 (Full HD)
echo 2. Set to 1366x768 (HD)
echo 3. Set to 1280x720 (HD Ready)
echo 4. Set to 2560x1440 (2K)
echo 5. Set to 3840x2160 (4K)
echo 6. View Current Resolution
echo 7. Display Settings
echo 8. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call :setres 1920 1080
if "%choice%"=="2" call :setres 1366 768
if "%choice%"=="3" call :setres 1280 720
if "%choice%"=="4" call :setres 2560 1440
if "%choice%"=="5" call :setres 3840 2160
if "%choice%"=="6" goto viewres
if "%choice%"=="7" start ms-settings:display & goto menu
if "%choice%"=="8" exit /b

goto menu

:setres
powershell -Command "& {Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SystemInformation]::PrimaryMonitorSize}"
echo Setting resolution to %1x%2...
start ms-settings:display
echo.
echo Please manually adjust resolution in the opened settings window.
pause
goto menu

:viewres
echo.
echo Current Display Information:
powershell Get-WmiObject -Class Win32_VideoController ^| Select-Object CurrentHorizontalResolution, CurrentVerticalResolution, CurrentRefreshRate
echo.
pause
goto menu
