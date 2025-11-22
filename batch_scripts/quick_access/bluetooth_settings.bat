@echo off
title Bluetooth Settings

echo ================================================
echo    Opening Bluetooth Settings
echo ================================================
echo.

start ms-settings:bluetooth

echo Bluetooth settings opened.
timeout /t 2 /nobreak >nul
