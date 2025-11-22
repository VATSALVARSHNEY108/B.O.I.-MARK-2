@echo off
title Bluetooth Status

echo ================================================
echo    Bluetooth Status
echo ================================================
echo.

powershell -Command "Get-PnpDevice | Where-Object {$_.Class -eq 'Bluetooth'} | Select-Object FriendlyName, Status | Format-Table -AutoSize"

echo.
pause
