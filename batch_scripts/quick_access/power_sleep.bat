@echo off
title Sleep Computer

echo ================================================
echo    Sleep Computer
echo ================================================
echo.

rundll32.exe powrprof.dll,SetSuspendState 0,1,0

echo Computer going to sleep...
timeout /t 2 /nobreak >nul
