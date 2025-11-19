@echo off
REM ============================================================
REM Quick WhatsApp Sender
REM Send WhatsApp message in one command
REM Usage: quick_whatsapp.bat <phone/name> <message>
REM ============================================================

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "PYTHON_SCRIPT=%PROJECT_ROOT%\scripts\whatsapp_cli.py"

if "%~1"=="" (
    echo.
    echo 📱 Quick WhatsApp Sender
    echo.
    echo Usage:
    echo    quick_whatsapp.bat ^<phone/name^> ^<message^>
    echo.
    echo Examples:
    echo    quick_whatsapp.bat +1234567890 "Hello there!"
    echo    quick_whatsapp.bat "John Doe" "How are you?"
    echo.
    echo For interactive menu, use: automation\whatsapp_messenger.bat
    echo.
    pause
    exit /b 1
)

if "%~2"=="" (
    echo.
    echo ❌ Error: Message is required
    echo.
    echo Usage: quick_whatsapp.bat ^<phone/name^> ^<message^>
    echo.
    pause
    exit /b 1
)

set "recipient=%~1"
shift
set "message=%~1"

:build_message
shift
if "%~1"=="" goto send_message
set "message=%message% %~1"
goto build_message

:send_message
echo.
echo 📱 Sending WhatsApp message...
echo 📞 To: %recipient%
echo 💬 Message: %message%
echo.

python "%PYTHON_SCRIPT%" send "%recipient%" "%message%"

echo.
echo ✅ Done!
echo.
timeout /t 3
exit /b 0
