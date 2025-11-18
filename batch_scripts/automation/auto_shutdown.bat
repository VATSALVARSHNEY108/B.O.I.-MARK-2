@echo off
REM ==========================================
REM AUTO SHUTDOWN SCHEDULER
REM Schedule automatic shutdown
REM ==========================================

color 0F
title Auto Shutdown Scheduler

:menu
cls
echo ========================================
echo    AUTO SHUTDOWN SCHEDULER
echo ========================================
echo.
echo 1. Shutdown in 1 Hour
echo 2. Shutdown in 2 Hours
echo 3. Shutdown in 30 Minutes
echo 4. Shutdown at Specific Time
echo 5. Custom Timer (Minutes)
echo 6. Cancel Scheduled Shutdown
echo 7. View Scheduled Shutdown
echo 8. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto onehour
if "%choice%"=="2" goto twohours
if "%choice%"=="3" goto halfhour
if "%choice%"=="4" goto specifictime
if "%choice%"=="5" goto custom
if "%choice%"=="6" goto cancel
if "%choice%"=="7" goto view
if "%choice%"=="8" exit /b

goto menu

:onehour
shutdown /s /t 3600
echo.
echo Shutdown scheduled in 1 hour!
pause
goto menu

:twohours
shutdown /s /t 7200
echo.
echo Shutdown scheduled in 2 hours!
pause
goto menu

:halfhour
shutdown /s /t 1800
echo.
echo Shutdown scheduled in 30 minutes!
pause
goto menu

:specifictime
set /p shuttime="Enter time (HH:MM format, e.g., 23:30): "
schtasks /create /tn "AutoShutdown" /tr "shutdown /s /f" /sc once /st %shuttime% /f
echo.
echo Shutdown scheduled at %shuttime%!
pause
goto menu

:custom
set /p minutes="Enter minutes until shutdown: "
set /a seconds=%minutes%*60
shutdown /s /t %seconds%
echo.
echo Shutdown scheduled in %minutes% minutes!
pause
goto menu

:cancel
shutdown /a
schtasks /delete /tn "AutoShutdown" /f 2>nul
echo.
echo Scheduled shutdown cancelled!
pause
goto menu

:view
echo.
schtasks /query /tn "AutoShutdown" 2>nul
if errorlevel 1 (
    echo No scheduled shutdown found.
) else (
    echo Scheduled shutdown task found above.
)
pause
goto menu
