@echo off
title RAM Usage

echo ================================================
echo    RAM/Memory Usage
echo ================================================
echo.

echo Memory Status:
echo ---------------
powershell -Command "$os = Get-WmiObject Win32_OperatingSystem; $total = [math]::Round($os.TotalVisibleMemorySize/1MB,2); $free = [math]::Round($os.FreePhysicalMemory/1MB,2); $used = $total - $free; $percent = [math]::Round(($used/$total)*100,2); Write-Host \"Total RAM: $total GB\"; Write-Host \"Used RAM: $used GB ($percent%%)\"; Write-Host \"Free RAM: $free GB\""

echo.
echo Top memory-consuming processes:
echo -------------------------------
powershell -Command "Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 Name, @{Name='Memory (MB)';Expression={[math]::Round($_.WorkingSet64/1MB,2)}}, CPU | Format-Table -AutoSize"

echo.
pause
