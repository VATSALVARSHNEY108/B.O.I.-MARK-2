@echo off
title Cancel Shutdown

echo ================================================
echo    Cancel Shutdown/Restart
echo ================================================
echo.

shutdown /a

if %errorlevel% equ 0 (
    echo SUCCESS: Shutdown/Restart cancelled!
) else (
    echo No shutdown or restart was scheduled.
)

echo.
pause
