@echo off
title Brightness Up

echo ================================================
echo    Increasing Brightness
echo ================================================
echo.

powershell -Command "try { $brightness = Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods -ErrorAction Stop; $brightness.WmiSetBrightness(1,100); Write-Host 'SUCCESS: Brightness set to maximum (100%%)' -ForegroundColor Green } catch { Write-Host 'WARNING: Unable to control brightness via WMI' -ForegroundColor Yellow; Write-Host 'This feature may not be supported on your display.' -ForegroundColor Yellow; Write-Host 'Opening display settings for manual adjustment...' -ForegroundColor Cyan; Start-Process 'ms-settings:display' }"

echo.
timeout /t 2 /nobreak >nul
