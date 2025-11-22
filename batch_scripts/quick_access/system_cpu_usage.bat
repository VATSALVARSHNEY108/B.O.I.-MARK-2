@echo off
title CPU Usage

echo ================================================
echo    CPU Usage Monitor
echo ================================================
echo.

echo Current CPU Usage:
echo -------------------
powershell -Command "Get-WmiObject Win32_Processor | Select-Object Name, LoadPercentage | Format-List"

echo.
echo Top CPU-consuming processes:
echo ----------------------------
powershell -Command "Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, CPU, @{Name='Memory (MB)';Expression={[math]::Round($_.WorkingSet64/1MB,2)}} | Format-Table -AutoSize"

echo.
pause
