@echo off
REM ========================================
REM  PHONE LINK AUTOMATOR - CALL VATSAL
REM ========================================
REM  This script finds Vatsal's mobile number
REM  from the contacts JSON file and calls
REM  using the Phone Link desktop app.
REM ========================================

title Phone Link - Call Vatsal

echo.
echo ========================================
echo   PHONE LINK AUTOMATOR - CALL VATSAL
echo ========================================
echo.
echo This script will:
echo   1. Find Vatsal's number from contacts.json
echo   2. Open Phone Link app on your desktop
echo   3. Dial and call Vatsal automatically
echo.
echo Make sure:
echo   - Phone Link is connected to your phone
echo   - Your Android/iPhone is paired via Phone Link
echo.
echo ----------------------------------------
echo.

REM Navigate to project root
cd /d "%~dp0.."

REM Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from python.org
    pause
    exit /b 1
)

REM Run the Python script
echo Starting Phone Link automation...
echo.
python scripts/call_vatsal.py

echo.
echo ----------------------------------------
echo.
if %ERRORLEVEL% equ 0 (
    echo Call initiated successfully!
) else (
    echo There was an issue with the call.
    echo Please check if Phone Link is connected.
)
echo.
pause
