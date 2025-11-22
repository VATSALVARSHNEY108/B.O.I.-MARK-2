@echo off
title Set Volume to 100%%

echo ================================================
echo    Setting Volume to 100%%
echo ================================================
echo.

powershell -Command "$obj = New-Object -ComObject WScript.Shell; for ($i=0; $i -lt 50; $i++) { $obj.SendKeys([char]175) }; Write-Host 'Volume set to maximum (100%%)' -ForegroundColor Green"

echo.
timeout /t 2 /nobreak >nul
