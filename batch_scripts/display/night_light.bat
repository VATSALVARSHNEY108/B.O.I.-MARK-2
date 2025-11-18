@echo off
REM ==========================================
REM NIGHT LIGHT CONTROL
REM Control Windows Night Light feature
REM ==========================================

color 0B
title Night Light Control

:menu
cls
echo ========================================
echo       NIGHT LIGHT CONTROL
echo ========================================
echo.
echo 1. Enable Night Light
echo 2. Disable Night Light
echo 3. Open Night Light Settings
echo 4. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto enable
if "%choice%"=="2" goto disable
if "%choice%"=="3" start ms-settings:nightlight & goto menu
if "%choice%"=="4" exit /b

goto menu

:enable
echo Enabling Night Light...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Current\default$windows.data.bluelightreduction.settings\windows.data.bluelightreduction.settings" /v Data /t REG_BINARY /d "02000000f46cb0c96780da0110000000430042010843420908420000000000000000000000000000000000" /f >nul 2>&1
echo.
echo Night Light enabled! You may need to restart for changes to take effect.
timeout /t 2 >nul
goto menu

:disable
echo Disabling Night Light...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Current\default$windows.data.bluelightreduction.settings\windows.data.bluelightreduction.settings" /v Data /t REG_BINARY /d "02000000f46cb0c96780da0100000000430042010843420908420000000000000000000000000000000000" /f >nul 2>&1
echo.
echo Night Light disabled!
timeout /t 2 >nul
goto menu
