@echo off
REM ==========================================
REM WEBCAM CONTROL
REM Manage webcam and camera settings
REM ==========================================

color 0B
title Webcam Control

:menu
cls
echo ========================================
echo       WEBCAM CONTROL
echo ========================================
echo.
echo 1. Open Camera App
echo 2. View Camera Devices
echo 3. Enable Webcam
echo 4. Disable Webcam
echo 5. Camera Privacy Settings
echo 6. Test Webcam
echo 7. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto opencamera
if "%choice%"=="2" goto viewcameras
if "%choice%"=="3" goto enable
if "%choice%"=="4" goto disable
if "%choice%"=="5" goto privacy
if "%choice%"=="6" goto test
if "%choice%"=="7" exit /b

goto menu

:opencamera
start microsoft.windows.camera:
goto menu

:viewcameras
echo.
echo Camera Devices:
powershell "Get-PnpDevice -Class Camera | Format-Table -AutoSize"
echo.
pause
goto menu

:enable
echo.
echo Available Camera Devices:
powershell "Get-PnpDevice -Class Camera | Format-Table FriendlyName, Status -AutoSize"
set /p devicename="Enter device friendly name: "
powershell "Enable-PnpDevice -FriendlyName '%devicename%' -Confirm:$false"
echo.
echo Webcam enabled!
pause
goto menu

:disable
echo.
echo Available Camera Devices:
powershell "Get-PnpDevice -Class Camera | Format-Table FriendlyName, Status -AutoSize"
set /p devicename="Enter device friendly name: "
powershell "Disable-PnpDevice -FriendlyName '%devicename%' -Confirm:$false"
echo.
echo Webcam disabled!
pause
goto menu

:privacy
start ms-settings:privacy-webcam
goto menu

:test
echo.
echo Opening Camera app for testing...
start microsoft.windows.camera:
echo.
echo Check if your webcam is working in the Camera app.
pause
goto menu
