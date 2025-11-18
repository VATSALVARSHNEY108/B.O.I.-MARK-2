@echo off
REM ==========================================
REM DISPLAY MIRRORING & PROJECTION
REM Control screen mirroring and projection
REM ==========================================

color 0B
title Display Mirroring

:menu
cls
echo ========================================
echo   DISPLAY MIRRORING ^& PROJECTION
echo ========================================
echo.
echo 1. PC Screen Only
echo 2. Duplicate (Mirror)
echo 3. Extend Display
echo 4. Second Screen Only
echo 5. Open Project Settings
echo 6. Connect to Wireless Display
echo 7. Display Settings
echo 8. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto pconly
if "%choice%"=="2" goto duplicate
if "%choice%"=="3" goto extend
if "%choice%"=="4" goto secondonly
if "%choice%"=="5" goto project
if "%choice%"=="6" goto wireless
if "%choice%"=="7" goto displaysettings
if "%choice%"=="8" exit /b

goto menu

:pconly
echo.
echo Setting to PC Screen Only...
displayswitch.exe /internal
echo Done!
timeout /t 2 >nul
goto menu

:duplicate
echo.
echo Setting to Duplicate (Mirror) mode...
displayswitch.exe /clone
echo Done!
timeout /t 2 >nul
goto menu

:extend
echo.
echo Setting to Extend Display mode...
displayswitch.exe /extend
echo Done!
timeout /t 2 >nul
goto menu

:secondonly
echo.
echo Setting to Second Screen Only...
displayswitch.exe /external
echo Done!
timeout /t 2 >nul
goto menu

:project
echo.
echo Opening Project settings...
start ms-settings:project
goto menu

:wireless
echo.
echo Opening Wireless Display connection...
start ms-availablenetworks:
goto menu

:displaysettings
start ms-settings:display
goto menu
