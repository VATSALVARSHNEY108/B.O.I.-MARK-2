@echo off
title Set Volume to 50%%

echo ================================================
echo    Setting Volume to 50%%
echo ================================================
echo.

powershell -Command "$obj = New-Object -ComObject WScript.Shell; for ($i=0; $i -lt 50; $i++) { $obj.SendKeys([char]174) }; Start-Sleep -Milliseconds 100; for ($i=0; $i -lt 25; $i++) { $obj.SendKeys([char]175) }; Write-Host 'Volume set to approximately 50%%' -ForegroundColor Green"

echo.
timeout /t 2 /nobreak >nul
