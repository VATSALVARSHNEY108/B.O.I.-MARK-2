@echo off
title Volume Down

echo ================================================
echo    Decreasing Volume
echo ================================================
echo.

powershell -Command "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"

echo Volume decreased.
timeout /t 1 /nobreak >nul
