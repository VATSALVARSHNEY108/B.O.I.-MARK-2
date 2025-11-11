@echo off
REM Reminder System for VATSAL AI
REM This batch file allows adding and viewing reminders

set desktop=%USERPROFILE%\Desktop
set reminderfile=%desktop%\REMINDERS.txt

:MENU
cls
echo ================================================
echo          VATSAL AI REMINDER SYSTEM
echo ================================================
echo.
echo 1. Add New Reminder
echo 2. View All Reminders
echo 3. Clear All Reminders
echo 4. Exit
echo.
echo ================================================
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto ADD_REMINDER
if "%choice%"=="2" goto VIEW_REMINDERS
if "%choice%"=="3" goto CLEAR_REMINDERS
if "%choice%"=="4" goto EXIT
goto MENU

:ADD_REMINDER
cls
echo ================================================
echo            ADD NEW REMINDER
echo ================================================
echo.
set /p reminder_text="Enter your reminder: "
set /p reminder_time="Enter time/date (optional): "

REM Get current timestamp
echo. >> "%reminderfile%"
echo [%date% %time%] >> "%reminderfile%"
echo Reminder: %reminder_text% >> "%reminderfile%"
if not "%reminder_time%"=="" (
    echo Due: %reminder_time% >> "%reminderfile%"
)
echo ------------------------------------------------ >> "%reminderfile%"

echo.
echo Reminder added successfully!
echo.
timeout /t 2 >nul
goto MENU

:VIEW_REMINDERS
cls
echo ================================================
echo           YOUR REMINDERS
echo ================================================
echo.
if not exist "%reminderfile%" (
    echo No reminders found.
) else (
    type "%reminderfile%"
)
echo.
echo ================================================
echo Press any key to return to menu...
pause >nul
goto MENU

:CLEAR_REMINDERS
cls
echo ================================================
echo         CLEAR ALL REMINDERS
echo ================================================
echo.
echo Are you sure you want to clear all reminders?
set /p confirm="Type YES to confirm: "
if /i "%confirm%"=="YES" (
    if exist "%reminderfile%" del "%reminderfile%"
    echo All reminders cleared!
) else (
    echo Operation cancelled.
)
echo.
timeout /t 2 >nul
goto MENU

:EXIT
echo.
echo Thank you for using VATSAL AI Reminder System!
timeout /t 1 >nul
exit
