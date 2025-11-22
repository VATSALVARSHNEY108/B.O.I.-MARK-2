@echo off
title Lock Computer

echo ================================================
echo    Lock Computer
echo ================================================
echo.

rundll32.exe user32.dll,LockWorkStation

echo Computer locked.
timeout /t 1 /nobreak >nul
