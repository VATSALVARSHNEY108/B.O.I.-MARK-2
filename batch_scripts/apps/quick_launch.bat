@echo off
REM ==========================================
REM Quick Launch Menu
REM Launch common applications
REM ==========================================

title Quick Launch

:menu
cls
echo ========================================
echo        QUICK LAUNCH MENU
echo ========================================
echo.
echo 1. Chrome
echo 2. Firefox
echo 3. Edge
echo 4. Notepad
echo 5. Calculator
echo 6. File Explorer
echo 7. Task Manager
echo 8. Control Panel
echo 9. Command Prompt (Admin)
echo 10. PowerShell (Admin)
echo 11. Settings
echo 12. Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" start chrome.exe
if "%choice%"=="2" start firefox.exe
if "%choice%"=="3" start msedge.exe
if "%choice%"=="4" start notepad.exe
if "%choice%"=="5" start calc.exe
if "%choice%"=="6" start explorer.exe
if "%choice%"=="7" start taskmgr.exe
if "%choice%"=="8" start control.exe
if "%choice%"=="9" powershell -Command "Start-Process cmd -Verb RunAs"
if "%choice%"=="10" powershell -Command "Start-Process powershell -Verb RunAs"
if "%choice%"=="11" start ms-settings:
if "%choice%"=="12" exit

timeout /t 1 >nul
goto menu
