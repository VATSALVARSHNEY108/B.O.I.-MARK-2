@echo off
title Volume Up

echo ================================================
echo    Increasing Volume
echo ================================================
echo.

powershell -Command "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"

echo Volume increased.
timeout /t 1 /nobreak >nul
