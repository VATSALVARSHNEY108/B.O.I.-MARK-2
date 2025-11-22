@echo off
title Launch Task Manager

echo ================================================
echo    Launching Task Manager
echo ================================================
echo.

start taskmgr

echo Task Manager launched.
timeout /t 1 /nobreak >nul
