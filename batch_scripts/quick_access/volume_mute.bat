@echo off
title Mute Volume

echo ================================================
echo    Muting Volume
echo ================================================
echo.

powershell -Command "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"

echo Volume muted/unmuted (toggle).
timeout /t 1 /nobreak >nul
