@echo off
REM ========================================
REM  PHONE LINK AUTOMATOR - CALL CONTACT
REM ========================================
REM  This script finds a contact's mobile number
REM  from the contacts JSON file and calls
REM  using the Phone Link desktop app.
REM ========================================

title Phone Link - Call Contact

echo.
echo ========================================
echo   PHONE LINK AUTOMATOR - CALL CONTACT
echo ========================================
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

REM Check if contact name was provided as argument
if "%~1"=="" (
    REM No argument provided, ask user for contact name
    echo Enter the name of the contact you want to call.
    echo.
    echo Available contacts in your phonebook:
    python -c "import json; contacts=json.load(open('data/contacts.json')); [print(f'  - {c[\"name\"]}: {c.get(\"phone\", \"No number\")}') for c in contacts]"
    echo.
    set /p CONTACT_NAME="Enter contact name: "
) else (
    REM Use argument as contact name
    set "CONTACT_NAME=%*"
)

echo.
echo ----------------------------------------
echo.
echo This script will:
echo   1. Find %CONTACT_NAME%'s number from contacts.json
echo   2. Open Phone Link app on your desktop
echo   3. Dial and call automatically
echo.
echo Make sure:
echo   - Phone Link is connected to your phone
echo   - Your Android/iPhone is paired via Phone Link
echo.
echo ----------------------------------------
echo.

REM Run the Python script with contact name
echo Starting Phone Link automation...
echo.
python scripts/call_file.py %CONTACT_NAME%

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
