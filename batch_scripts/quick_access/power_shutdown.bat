@echo off
title Shutdown Computer

echo ================================================
echo    Shutdown Computer
echo ================================================
echo.
echo WARNING: This will shutdown your computer!
echo.
set /p confirm="Are you sure you want to shutdown? (Y/N): "

if /i "%confirm%"=="Y" (
    echo.
    echo Your computer will shutdown in 10 seconds...
    echo Press Ctrl+C to cancel during countdown.
    echo.
    shutdown /s /t 10
) else (
    echo.
    echo Shutdown cancelled.
    timeout /t 2 /nobreak >nul
)
