@echo off
title WiFi Status

echo ================================================
echo    WiFi Status and Available Networks
echo ================================================
echo.

echo Current WiFi Status:
echo -------------------
netsh wlan show interfaces

echo.
echo Available Networks:
echo -------------------
netsh wlan show networks

echo.
pause
