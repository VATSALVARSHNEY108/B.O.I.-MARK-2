@echo off
REM ==========================================
REM Battery Information & Power Management
REM Display battery status and create reports
REM ==========================================

color 0A
title Battery Information

:menu
cls
echo ========================================
echo     BATTERY INFORMATION
echo ========================================
echo.
echo 1. Current Battery Status
echo 2. Generate Battery Report
echo 3. Power Efficiency Report
echo 4. Show Power Plans
echo 5. Switch to High Performance
echo 6. Switch to Balanced
echo 7. Switch to Power Saver
echo 8. Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto status
if "%choice%"=="2" goto report
if "%choice%"=="3" goto efficiency
if "%choice%"=="4" goto plans
if "%choice%"=="5" goto high
if "%choice%"=="6" goto balanced
if "%choice%"=="7" goto saver
if "%choice%"=="8" exit
goto menu

:status
cls
echo Current Battery Status:
echo.
WMIC Path Win32_Battery Get BatteryStatus,EstimatedChargeRemaining,EstimatedRunTime
echo.
powercfg /batteryreport /output "%TEMP%\battery-report.html" >nul
start %TEMP%\battery-report.html
echo.
echo Battery report opened in browser
pause
goto menu

:report
echo Generating detailed battery report...
powercfg /batteryreport /output "%USERPROFILE%\Desktop\battery-report.html"
echo.
echo Report saved to: %USERPROFILE%\Desktop\battery-report.html
start %USERPROFILE%\Desktop\battery-report.html
timeout /t 2 >nul
goto menu

:efficiency
echo Generating power efficiency report...
powercfg /energy /output "%USERPROFILE%\Desktop\energy-report.html"
echo.
echo Report saved to: %USERPROFILE%\Desktop\energy-report.html
start %USERPROFILE%\Desktop\energy-report.html
timeout /t 2 >nul
goto menu

:plans
cls
echo Available Power Plans:
echo.
powercfg /list
echo.
pause
goto menu

:high
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
echo Switched to High Performance mode
timeout /t 2 >nul
goto menu

:balanced
powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e
echo Switched to Balanced mode
timeout /t 2 >nul
goto menu

:saver
powercfg /setactive a1841308-3541-4fab-bc81-f71556f20b4a
echo Switched to Power Saver mode
timeout /t 2 >nul
goto menu
