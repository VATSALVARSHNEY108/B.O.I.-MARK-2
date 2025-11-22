@echo off
title Restart Computer

echo ================================================
echo    Restart Computer
echo ================================================
echo.
echo WARNING: This will restart your computer!
echo.
set /p confirm="Are you sure you want to restart? (Y/N): "

if /i "%confirm%"=="Y" (
    echo.
    echo Your computer will restart in 10 seconds...
    echo Press Ctrl+C to cancel during countdown.
    echo.
    shutdown /r /t 10
) else (
    echo.
    echo Restart cancelled.
    timeout /t 2 /nobreak >nul
)
