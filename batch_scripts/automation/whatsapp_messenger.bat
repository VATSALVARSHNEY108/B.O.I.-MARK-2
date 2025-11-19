@echo off
REM ============================================================
REM WhatsApp Messenger Control
REM Send WhatsApp messages from command line
REM ============================================================

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%..\.."
set "PYTHON_SCRIPT=%PROJECT_ROOT%\scripts\whatsapp_cli.py"

REM Color definitions
set "GREEN=[92m"
set "BLUE=[94m"
set "YELLOW=[93m"
set "RED=[91m"
set "RESET=[0m"

:MENU
cls
echo.
echo %BLUE%============================================================%RESET%
echo %GREEN%                📱 WHATSAPP MESSENGER                      %RESET%
echo %BLUE%============================================================%RESET%
echo.
echo  1. Send Instant Message
echo  2. Send Scheduled Message
echo  3. Send Image/Photo
echo  4. Send to Group
echo  5. List Contacts
echo  6. Quick Send (Contact Name)
echo  7. Quick Send (Phone Number)
echo  8. Help / Usage Guide
echo  9. Exit
echo.
echo %BLUE%============================================================%RESET%
echo.

set /p choice="Select option (1-9): "

if "%choice%"=="1" goto SEND_INSTANT
if "%choice%"=="2" goto SEND_SCHEDULED
if "%choice%"=="3" goto SEND_IMAGE
if "%choice%"=="4" goto SEND_GROUP
if "%choice%"=="5" goto LIST_CONTACTS
if "%choice%"=="6" goto QUICK_SEND_NAME
if "%choice%"=="7" goto QUICK_SEND_PHONE
if "%choice%"=="8" goto SHOW_HELP
if "%choice%"=="9" goto END

echo %RED%Invalid option!%RESET%
timeout /t 2 >nul
goto MENU

:SEND_INSTANT
cls
echo.
echo %GREEN%=== Send Instant Message ===%RESET%
echo.
set /p recipient="Enter phone number or contact name: "
echo.
set /p message="Enter message: "
echo.
echo %YELLOW%Sending message...%RESET%
python "%PYTHON_SCRIPT%" send "%recipient%" "%message%"
echo.
pause
goto MENU

:SEND_SCHEDULED
cls
echo.
echo %GREEN%=== Schedule WhatsApp Message ===%RESET%
echo.
set /p recipient="Enter phone number or contact name: "
echo.
set /p hour="Enter hour (0-23): "
set /p minute="Enter minute (0-59): "
echo.
set /p message="Enter message: "
echo.
echo %YELLOW%Scheduling message for %hour%:%minute%...%RESET%
python "%PYTHON_SCRIPT%" schedule "%recipient%" %hour% %minute% "%message%"
echo.
pause
goto MENU

:SEND_IMAGE
cls
echo.
echo %GREEN%=== Send Image/Photo ===%RESET%
echo.
set /p recipient="Enter phone number or contact name: "
echo.
set /p image_path="Enter image path: "
echo.
set /p caption="Enter caption (optional): "
echo.
echo %YELLOW%Sending image...%RESET%
if "%caption%"=="" (
    python "%PYTHON_SCRIPT%" image "%recipient%" "%image_path%"
) else (
    python "%PYTHON_SCRIPT%" image "%recipient%" "%image_path%" "%caption%"
)
echo.
pause
goto MENU

:SEND_GROUP
cls
echo.
echo %GREEN%=== Send to WhatsApp Group ===%RESET%
echo.
set /p group_id="Enter group ID: "
echo.
set /p message="Enter message: "
echo.
echo %YELLOW%Sending to group...%RESET%
python "%PYTHON_SCRIPT%" group "%group_id%" "%message%"
echo.
pause
goto MENU

:LIST_CONTACTS
cls
echo.
echo %GREEN%=== Your Contacts ===%RESET%
echo.
python "%PYTHON_SCRIPT%" contacts
echo.
pause
goto MENU

:QUICK_SEND_NAME
cls
echo.
echo %GREEN%=== Quick Send (Contact Name) ===%RESET%
echo.
set /p name="Enter contact name: "
echo.
set /p message="Enter message: "
echo.
echo %YELLOW%Sending message to %name%...%RESET%
python "%PYTHON_SCRIPT%" send "%name%" "%message%"
echo.
pause
goto MENU

:QUICK_SEND_PHONE
cls
echo.
echo %GREEN%=== Quick Send (Phone Number) ===%RESET%
echo.
echo %YELLOW%Format: +1234567890 (include country code)%RESET%
echo.
set /p phone="Enter phone number: "
echo.
set /p message="Enter message: "
echo.
echo %YELLOW%Sending message to %phone%...%RESET%
python "%PYTHON_SCRIPT%" send "%phone%" "%message%"
echo.
pause
goto MENU

:SHOW_HELP
cls
python "%PYTHON_SCRIPT%" help
echo.
pause
goto MENU

:END
echo.
echo %GREEN%Thank you for using WhatsApp Messenger!%RESET%
echo.
timeout /t 2 >nul
exit /b 0
