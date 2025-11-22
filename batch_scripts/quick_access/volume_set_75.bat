@echo off
title Set Volume to 75%%

echo ================================================
echo    Setting Volume to 75%%
echo ================================================
echo.

powershell -Command "$obj = New-Object -ComObject WScript.Shell; for ($i=0; $i -lt 50; $i++) { $obj.SendKeys([char]174) }; Start-Sleep -Milliseconds 100; for ($i=0; $i -lt 38; $i++) { $obj.SendKeys([char]175) }; Write-Host 'Volume set to approximately 75%%' -ForegroundColor Green"

echo.
timeout /t 2 /nobreak >nul
