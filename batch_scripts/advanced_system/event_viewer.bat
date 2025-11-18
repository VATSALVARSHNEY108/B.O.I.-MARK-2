@echo off
REM ==========================================
REM EVENT VIEWER TOOLS
REM Quick access to system logs
REM ==========================================

color 0D
title Event Viewer Tools

:menu
cls
echo ========================================
echo       EVENT VIEWER TOOLS
echo ========================================
echo.
echo 1. View System Errors
echo 2. View Application Errors
echo 3. View Security Logs
echo 4. View Windows Update Logs
echo 5. View Startup Events
echo 6. View Recent Critical Events
echo 7. Clear All Event Logs
echo 8. Open Event Viewer
echo 9. Export Logs
echo 10. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto syserrors
if "%choice%"=="2" goto apperrors
if "%choice%"=="3" goto security
if "%choice%"=="4" goto wupdates
if "%choice%"=="5" goto startup
if "%choice%"=="6" goto critical
if "%choice%"=="7" goto clearlogs
if "%choice%"=="8" start eventvwr.msc & goto menu
if "%choice%"=="9" goto exportlogs
if "%choice%"=="10" exit /b

goto menu

:syserrors
echo.
echo Recent System Errors:
wevtutil qe System /c:20 /rd:true /f:text /q:"*[System[(Level=2)]]"
echo.
pause
goto menu

:apperrors
echo.
echo Recent Application Errors:
wevtutil qe Application /c:20 /rd:true /f:text /q:"*[System[(Level=2)]]"
echo.
pause
goto menu

:security
echo.
echo Recent Security Events:
wevtutil qe Security /c:20 /rd:true /f:text
echo.
pause
goto menu

:wupdates
echo.
echo Windows Update Events:
wevtutil qe System /c:20 /rd:true /f:text /q:"*[System[Provider[@Name='Microsoft-Windows-WindowsUpdateClient']]]"
echo.
pause
goto menu

:startup
echo.
echo Recent Startup Events:
wevtutil qe System /c:10 /rd:true /f:text /q:"*[System[EventID=6005]]"
echo.
pause
goto menu

:critical
echo.
echo Recent Critical Events:
wevtutil qe System /c:10 /rd:true /f:text /q:"*[System[(Level=1)]]"
echo.
pause
goto menu

:clearlogs
echo.
echo WARNING: This will clear ALL event logs!
set /p confirm="Are you sure? (Y/N): "
if /i "%confirm%"=="Y" (
    echo.
    echo Clearing event logs...
    for /f "tokens=*" %%i in ('wevtutil el') do wevtutil cl "%%i"
    echo.
    echo All event logs cleared!
) else (
    echo Operation cancelled.
)
pause
goto menu

:exportlogs
if not exist "%USERPROFILE%\Desktop\EventLogs" mkdir "%USERPROFILE%\Desktop\EventLogs"
set exportfile=%USERPROFILE%\Desktop\EventLogs\Events_%date:~-4,4%%date:~-10,2%%date:~-7,2%.evtx
set exportfile=%exportfile: =0%

echo.
echo Exporting System Log...
wevtutil epl System "%exportfile%"
echo.
echo Log exported to: %exportfile%
pause
goto menu
