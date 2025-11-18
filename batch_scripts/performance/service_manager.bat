@echo off
REM ==========================================
REM SERVICE MANAGER
REM Manage Windows services
REM ==========================================

color 0A
title Service Manager

:menu
cls
echo ========================================
echo       SERVICE MANAGER
echo ========================================
echo.
echo 1. List All Services
echo 2. List Running Services
echo 3. List Stopped Services
echo 4. Start a Service
echo 5. Stop a Service
echo 6. Restart a Service
echo 7. Disable a Service
echo 8. Enable a Service
echo 9. Open Services Manager
echo 10. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto listall
if "%choice%"=="2" goto listrunning
if "%choice%"=="3" goto liststopped
if "%choice%"=="4" goto startservice
if "%choice%"=="5" goto stopservice
if "%choice%"=="6" goto restartservice
if "%choice%"=="7" goto disableservice
if "%choice%"=="8" goto enableservice
if "%choice%"=="9" start services.msc & goto menu
if "%choice%"=="10" exit /b

goto menu

:listall
echo.
echo All Services:
sc query type= service state= all | findstr "SERVICE_NAME DISPLAY_NAME STATE" | more
echo.
pause
goto menu

:listrunning
echo.
echo Running Services:
net start
echo.
pause
goto menu

:liststopped
echo.
echo Stopped Services:
sc query type= service state= all | findstr "SERVICE_NAME STATE" | findstr "STOPPED" | more
echo.
pause
goto menu

:startservice
set /p servicename="Enter service name: "
echo.
echo Starting %servicename%...
net start "%servicename%"
echo.
pause
goto menu

:stopservice
set /p servicename="Enter service name: "
echo.
echo Stopping %servicename%...
net stop "%servicename%"
echo.
pause
goto menu

:restartservice
set /p servicename="Enter service name: "
echo.
echo Restarting %servicename%...
net stop "%servicename%"
timeout /t 2 >nul
net start "%servicename%"
echo.
echo Service restarted!
pause
goto menu

:disableservice
set /p servicename="Enter service name: "
echo.
echo Disabling %servicename%...
sc config "%servicename%" start= disabled
echo.
echo Service disabled!
pause
goto menu

:enableservice
set /p servicename="Enter service name: "
echo.
echo Enabling %servicename%...
sc config "%servicename%" start= auto
echo.
echo Service enabled!
pause
goto menu
