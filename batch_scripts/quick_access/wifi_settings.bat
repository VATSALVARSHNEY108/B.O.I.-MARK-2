@echo off
title WiFi Settings

echo ================================================
echo    Opening WiFi Settings
echo ================================================
echo.

start ms-settings:network-wifi

echo WiFi settings opened.
timeout /t 2 /nobreak >nul
