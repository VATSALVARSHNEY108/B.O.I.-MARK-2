@echo off
title Battery Status

echo ================================================
echo    Battery Status
echo ================================================
echo.

echo Battery Information:
echo --------------------
powershell -Command "$battery = Get-WmiObject Win32_Battery; if ($battery) { Write-Host \"Battery Status: $($battery.Status)\"; Write-Host \"Charge Remaining: $($battery.EstimatedChargeRemaining)%%\"; Write-Host \"Estimated Runtime: $($battery.EstimatedRunTime) minutes\"; Write-Host \"Battery Health: $($battery.BatteryStatus)\" } else { Write-Host 'No battery detected (Desktop PC)' }"

echo.
pause
