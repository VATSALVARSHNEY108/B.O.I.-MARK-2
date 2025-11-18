@echo off
REM ==========================================
REM Clipboard Manager
REM Save and manage clipboard history
REM ==========================================

setlocal enabledelayedexpansion
title Clipboard Manager

set clipboard_dir=%TEMP%\ClipboardHistory
if not exist "%clipboard_dir%" mkdir "%clipboard_dir%"

:menu
cls
echo ========================================
echo       CLIPBOARD MANAGER
echo ========================================
echo.
echo 1. Save Current Clipboard
echo 2. View Saved Clips
echo 3. Load Saved Clip
echo 4. Clear All Clips
echo 5. Save Clipboard to File
echo 6. Load File to Clipboard
echo 7. Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto save
if "%choice%"=="2" goto view
if "%choice%"=="3" goto load
if "%choice%"=="4" goto clear
if "%choice%"=="5" goto savefile
if "%choice%"=="6" goto loadfile
if "%choice%"=="7" exit
goto menu

:save
set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%
powershell -command "Get-Clipboard | Out-File '%clipboard_dir%\clip_%timestamp%.txt'"
echo Clipboard saved as clip_%timestamp%.txt
timeout /t 2 >nul
goto menu

:view
cls
echo Saved Clips:
echo.
dir /b "%clipboard_dir%\*.txt" 2>nul
if errorlevel 1 echo No saved clips found
echo.
pause
goto menu

:load
cls
echo Available Clips:
echo.
dir /b "%clipboard_dir%\*.txt" 2>nul
echo.
set /p clipfile="Enter clip filename to load: "
if exist "%clipboard_dir%\%clipfile%" (
    type "%clipboard_dir%\%clipfile%" | clip
    echo Clipboard loaded!
) else (
    echo File not found!
)
timeout /t 2 >nul
goto menu

:clear
del /q "%clipboard_dir%\*.txt" 2>nul
echo All clips cleared!
timeout /t 2 >nul
goto menu

:savefile
set /p filepath="Enter path to save clipboard: "
powershell -command "Get-Clipboard | Out-File '%filepath%'"
echo Clipboard saved to %filepath%
timeout /t 2 >nul
goto menu

:loadfile
set /p filepath="Enter file path to load: "
if exist "%filepath%" (
    type "%filepath%" | clip
    echo File loaded to clipboard!
) else (
    echo File not found!
)
timeout /t 2 >nul
goto menu
