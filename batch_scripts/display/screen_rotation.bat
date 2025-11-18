@echo off
REM ==========================================
REM SCREEN ROTATION CONTROL
REM Rotate display orientation
REM ==========================================

color 0B
title Screen Rotation

:menu
cls
echo ========================================
echo      SCREEN ROTATION CONTROL
echo ========================================
echo.
echo 1. Landscape (Normal - 0 degrees)
echo 2. Portrait (90 degrees)
echo 3. Landscape Flipped (180 degrees)
echo 4. Portrait Flipped (270 degrees)
echo 5. Open Display Settings
echo 6. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" call :rotate 0
if "%choice%"=="2" call :rotate 1
if "%choice%"=="3" call :rotate 2
if "%choice%"=="4" call :rotate 3
if "%choice%"=="5" start ms-settings:display & goto menu
if "%choice%"=="6" exit /b

goto menu

:rotate
echo Setting screen orientation...
start ms-settings:display
echo.
echo Please use the opened Display Settings to change orientation.
echo Or use graphics driver hotkeys (if available):
echo - Intel: Ctrl+Alt+Arrow Keys
echo - AMD/NVIDIA: Check graphics control panel
echo.
pause
goto menu
