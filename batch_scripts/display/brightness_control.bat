@echo off
REM ==========================================
REM BRIGHTNESS CONTROL
REM Quick brightness adjustment tool
REM ==========================================

color 0B
title Brightness Control

:menu
cls
echo ========================================
echo       BRIGHTNESS CONTROL
echo ========================================
echo.
echo 1. Set Brightness to 100%%
echo 2. Set Brightness to 75%%
echo 3. Set Brightness to 50%%
echo 4. Set Brightness to 25%%
echo 5. Set Brightness to 10%%
echo 6. Custom Brightness
echo 7. View Current Brightness
echo 8. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,100) & goto success
if "%choice%"=="2" powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,75) & goto success
if "%choice%"=="3" powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,50) & goto success
if "%choice%"=="4" powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,25) & goto success
if "%choice%"=="5" powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,10) & goto success
if "%choice%"=="6" goto custom
if "%choice%"=="7" goto view
if "%choice%"=="8" exit /b

goto menu

:custom
set /p level="Enter brightness level (0-100): "
powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,%level%)
goto success

:view
powershell Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness ^| Select-Object CurrentBrightness
pause
goto menu

:success
echo.
echo Brightness adjusted successfully!
timeout /t 2 >nul
goto menu
