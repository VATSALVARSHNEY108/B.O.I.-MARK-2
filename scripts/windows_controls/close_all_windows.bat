@echo off
REM ==========================================
REM Close All Open Windows/Tabs
REM Closes all application windows except system critical ones
REM ==========================================

title Close All Windows
color 0C

echo.
echo ========================================
echo    CLOSE ALL WINDOWS
echo ========================================
echo.
echo This will close all open applications
echo and browser tabs.
echo.
echo Press Ctrl+C to cancel
timeout /t 5

echo.
echo Closing all windows...

REM Close all browser windows (Chrome, Firefox, Edge)
taskkill /F /IM chrome.exe 2>nul
taskkill /F /IM firefox.exe 2>nul
taskkill /F /IM msedge.exe 2>nul
taskkill /F /IM opera.exe 2>nul
taskkill /F /IM brave.exe 2>nul

REM Close common applications
taskkill /F /IM notepad.exe 2>nul
taskkill /F /IM mspaint.exe 2>nul
taskkill /F /IM WINWORD.EXE 2>nul
taskkill /F /IM EXCEL.EXE 2>nul
taskkill /F /IM POWERPNT.EXE 2>nul
taskkill /F /IM Code.exe 2>nul
taskkill /F /IM Discord.exe 2>nul
taskkill /F /IM Spotify.exe 2>nul
taskkill /F /IM Telegram.exe 2>nul
taskkill /F /IM WhatsApp.exe 2>nul

REM Use PowerShell to close remaining non-system windows gracefully
powershell -Command "Get-Process | Where-Object {$_.MainWindowTitle -ne ''} | Where-Object {$_.ProcessName -notin @('explorer','taskmgr','SystemSettings')} | Stop-Process -ErrorAction SilentlyContinue"

echo.
echo ========================================
echo    ALL WINDOWS CLOSED
echo ========================================
echo.

timeout /t 3
exit
