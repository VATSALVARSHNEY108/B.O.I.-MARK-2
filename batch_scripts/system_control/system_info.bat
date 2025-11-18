@echo off
REM ==========================================
REM System Information Display
REM Shows detailed system info
REM ==========================================

color 0A
title System Information

echo ========================================
echo        SYSTEM INFORMATION
echo ========================================
echo.

echo [Computer Name]
echo %COMPUTERNAME%
echo.

echo [Username]
echo %USERNAME%
echo.

echo [Operating System]
systeminfo | findstr /C:"OS Name"
systeminfo | findstr /C:"OS Version"
echo.

echo [System Type]
systeminfo | findstr /C:"System Type"
echo.

echo [Total Physical Memory]
systeminfo | findstr /C:"Total Physical Memory"
echo.

echo [Available Memory]
systeminfo | findstr /C:"Available Physical Memory"
echo.

echo [Processor]
wmic cpu get name
echo.

echo [IP Address]
ipconfig | findstr /C:"IPv4"
echo.

echo [Disk Information]
wmic logicaldisk get caption,description,freespace,size
echo.

echo ========================================
echo Press any key to exit...
pause >nul
