@echo off
title Disk Usage

echo ================================================
echo    Disk Space Usage
echo ================================================
echo.

echo Disk Space Information:
echo -----------------------
powershell -Command "Get-WmiObject Win32_LogicalDisk -Filter \"DriveType=3\" | Select-Object DeviceID, VolumeName, @{Name='Size (GB)';Expression={[math]::Round($_.Size/1GB,2)}}, @{Name='Free (GB)';Expression={[math]::Round($_.FreeSpace/1GB,2)}}, @{Name='Used %%';Expression={[math]::Round((($_.Size-$_.FreeSpace)/$_.Size)*100,2)}} | Format-Table -AutoSize"

echo.
pause
