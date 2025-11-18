@echo off
REM ==========================================
REM LEGACY UTILITIES MENU
REM Desktop time/date and reminder utilities
REM ==========================================

color 0D
title Legacy Utilities

:menu
cls
echo ========================================
echo       LEGACY UTILITIES
echo ========================================
echo.
echo These are older utilities for creating
echo desktop files that VATSAL AI can read.
echo.
echo 1. Show Time/Date on Desktop
echo 2. Auto-Update Time (Runs continuously)
echo 3. Reminder System
echo 4. View Documentation
echo.
echo 0. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call show_time_date.bat & goto menu
if "%choice%"=="2" call auto_update_time.bat & goto menu
if "%choice%"=="3" call reminder_system.bat & goto menu
if "%choice%"=="4" goto docs
if "%choice%"=="0" exit /b

goto menu

:docs
cls
type README.md | more
pause
goto menu
