@echo off
REM AI Phone Controller - Call with number as argument
REM Usage: ai_phone_with_number.bat "+1234567890"
REM Or drag this file and type the number when prompted

title AI Phone Link - Quick Call
color 0E

if "%~1"=="" (
    REM No argument provided, ask for number
    echo.
    echo ========================================
    echo  AI PHONE LINK - QUICK CALL
    echo ========================================
    echo.
    set /p PHONE_NUMBER="Enter phone number to dial: "
) else (
    REM Use provided argument
    set PHONE_NUMBER=%~1
)

echo.
echo Calling %PHONE_NUMBER% with AI...
echo.

REM Use AI controller to dial
python ai_phone_link_controller.py "Call %PHONE_NUMBER%"

echo.
pause
