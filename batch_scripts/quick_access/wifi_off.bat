@echo off
title Turn WiFi OFF

echo ================================================
echo    Turning WiFi OFF
echo ================================================
echo.

netsh interface set interface name="Wi-Fi" admin=disabled 2>nul
if %errorlevel% equ 0 (
    echo SUCCESS: WiFi turned OFF!
) else (
    netsh interface set interface name="WiFi" admin=disabled 2>nul
    if %errorlevel% equ 0 (
        echo SUCCESS: WiFi turned OFF!
    ) else (
        echo ERROR: Failed to disable WiFi
        echo Opening WiFi settings...
        start ms-settings:network-wifi
    )
)

echo.
pause
