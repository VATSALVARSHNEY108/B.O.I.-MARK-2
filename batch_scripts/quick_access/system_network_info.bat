@echo off
title Network Information

echo ================================================
echo    Network Information
echo ================================================
echo.

echo IP Configuration:
echo -----------------
ipconfig

echo.
echo Network Adapters:
echo -----------------
powershell -Command "Get-NetAdapter | Select-Object Name, Status, LinkSpeed | Format-Table -AutoSize"

echo.
echo Active Connections:
echo -------------------
netstat -an | findstr "ESTABLISHED"

echo.
pause
