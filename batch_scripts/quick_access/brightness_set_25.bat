@echo off
title Set Brightness to 25%%

echo ================================================
echo    Setting Brightness to 25%%
echo ================================================
echo.

powershell -Command "try { $brightness = Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods -ErrorAction Stop; $brightness.WmiSetBrightness(1,25); Write-Host 'SUCCESS: Brightness set to 25%%' -ForegroundColor Green } catch { Write-Host 'WARNING: Unable to control brightness via WMI' -ForegroundColor Yellow; Write-Host 'This feature may not be supported on your display.' -ForegroundColor Yellow; Write-Host 'Opening display settings for manual adjustment...' -ForegroundColor Cyan; Start-Process 'ms-settings:display' }"

echo.
timeout /t 2 /nobreak >nul
