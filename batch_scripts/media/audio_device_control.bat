@echo off
REM ==========================================
REM AUDIO DEVICE CONTROL
REM Manage audio devices and settings
REM ==========================================

color 0B
title Audio Device Control

:menu
cls
echo ========================================
echo     AUDIO DEVICE CONTROL
echo ========================================
echo.
echo 1. View Audio Devices
echo 2. Set Default Playback Device
echo 3. Set Default Recording Device
echo 4. Mute/Unmute System
echo 5. Increase Volume
echo 6. Decrease Volume
echo 7. Open Sound Settings
echo 8. Open Volume Mixer
echo 9. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto viewdevices
if "%choice%"=="2" goto setplayback
if "%choice%"=="3" goto setrecording
if "%choice%"=="4" goto mute
if "%choice%"=="5" goto volup
if "%choice%"=="6" goto voldown
if "%choice%"=="7" goto soundsettings
if "%choice%"=="8" goto volumemixer
if "%choice%"=="9" exit /b

goto menu

:viewdevices
echo.
echo Audio Playback Devices:
powershell "Get-AudioDevice -List | Format-Table -AutoSize"
echo.
pause
goto menu

:setplayback
echo.
echo Available Playback Devices:
powershell "Get-AudioDevice -List | Where-Object {$_.Type -eq 'Playback'} | Format-Table Index, Name -AutoSize"
set /p deviceid="Enter device index: "
powershell "Set-AudioDevice -Index %deviceid%"
echo.
echo Default playback device set!
pause
goto menu

:setrecording
echo.
echo Available Recording Devices:
powershell "Get-AudioDevice -List | Where-Object {$_.Type -eq 'Recording'} | Format-Table Index, Name -AutoSize"
set /p deviceid="Enter device index: "
powershell "Set-AudioDevice -Index %deviceid%"
echo.
echo Default recording device set!
pause
goto menu

:mute
powershell "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"
echo.
echo System mute toggled!
timeout /t 1 >nul
goto menu

:volup
powershell "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"
echo.
echo Volume increased!
timeout /t 1 >nul
goto menu

:voldown
powershell "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"
echo.
echo Volume decreased!
timeout /t 1 >nul
goto menu

:soundsettings
start ms-settings:sound
goto menu

:volumemixer
start sndvol
goto menu
