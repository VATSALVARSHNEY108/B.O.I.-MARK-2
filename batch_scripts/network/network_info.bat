@echo off
REM ==========================================
REM Network Information
REM Display network configuration
REM ==========================================

color 0B
title Network Information

echo ========================================
echo      NETWORK INFORMATION
echo ========================================
echo.

echo [IP Configuration]
ipconfig /all
echo.

echo ========================================
echo [Active Connections]
netstat -an | findstr ESTABLISHED
echo.

echo ========================================
echo [Wi-Fi Networks]
netsh wlan show networks
echo.

echo ========================================
echo [DNS Cache]
ipconfig /displaydns | more
echo.

echo ========================================
pause
