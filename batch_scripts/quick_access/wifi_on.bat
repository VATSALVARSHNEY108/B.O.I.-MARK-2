@echo off
title Turn WiFi ON

echo ================================================
echo    Turning WiFi ON
echo ================================================
echo.

netsh interface set interface name="Wi-Fi" admin=enabled 2>nul
if %errorlevel% equ 0 (
    echo SUCCESS: WiFi turned ON!
) else (
    netsh interface set interface name="WiFi" admin=enabled 2>nul
    if %errorlevel% equ 0 (
        echo SUCCESS: WiFi turned ON!
    ) else (
        echo ERROR: Failed to enable WiFi
        echo Opening WiFi settings...
        start ms-settings:network-wifi
    )
)

echo.
pause
