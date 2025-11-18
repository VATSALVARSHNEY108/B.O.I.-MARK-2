@echo off
REM ==========================================
REM FIREWALL CONTROL
REM Manage Windows Firewall settings
REM ==========================================

color 0C
title Firewall Control

:menu
cls
echo ========================================
echo       FIREWALL CONTROL
echo ========================================
echo.
echo 1. Enable Firewall (All Profiles)
echo 2. Disable Firewall (All Profiles)
echo 3. View Firewall Status
echo 4. View Firewall Rules
echo 5. Block an Application
echo 6. Allow an Application
echo 7. Open Firewall Settings
echo 8. Reset Firewall to Default
echo 9. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto enable
if "%choice%"=="2" goto disable
if "%choice%"=="3" goto status
if "%choice%"=="4" goto rules
if "%choice%"=="5" goto block
if "%choice%"=="6" goto allow
if "%choice%"=="7" start firewall.cpl & goto menu
if "%choice%"=="8" goto reset
if "%choice%"=="9" exit /b

goto menu

:enable
echo Enabling Windows Firewall...
netsh advfirewall set allprofiles state on
echo.
echo Firewall enabled for all profiles!
pause
goto menu

:disable
echo.
echo WARNING: Disabling firewall reduces system security!
set /p confirm="Are you sure? (Y/N): "
if /i "%confirm%"=="Y" (
    netsh advfirewall set allprofiles state off
    echo Firewall disabled!
) else (
    echo Operation cancelled.
)
pause
goto menu

:status
echo.
echo Current Firewall Status:
netsh advfirewall show allprofiles
echo.
pause
goto menu

:rules
echo.
echo Firewall Rules:
netsh advfirewall firewall show rule name=all | more
echo.
pause
goto menu

:block
set /p app="Enter full path to application: "
set /p rulename="Enter rule name: "
netsh advfirewall firewall add rule name="%rulename%" dir=out action=block program="%app%"
echo.
echo Application blocked!
pause
goto menu

:allow
set /p app="Enter full path to application: "
set /p rulename="Enter rule name: "
netsh advfirewall firewall add rule name="%rulename%" dir=in action=allow program="%app%"
netsh advfirewall firewall add rule name="%rulename%" dir=out action=allow program="%app%"
echo.
echo Application allowed through firewall!
pause
goto menu

:reset
echo Resetting firewall to default settings...
netsh advfirewall reset
echo.
echo Firewall reset complete!
pause
goto menu
