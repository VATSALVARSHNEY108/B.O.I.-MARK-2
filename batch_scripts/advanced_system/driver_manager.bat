@echo off
REM ==========================================
REM DRIVER MANAGER
REM Manage and view system drivers
REM ==========================================

color 0D
title Driver Manager

:menu
cls
echo ========================================
echo        DRIVER MANAGER
echo ========================================
echo.
echo 1. List All Drivers
echo 2. List Running Drivers
echo 3. Backup All Drivers
echo 4. View Driver Details
echo 5. Check Driver Updates
echo 6. Open Device Manager
echo 7. Export Driver List
echo 8. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto listall
if "%choice%"=="2" goto listrunning
if "%choice%"=="3" goto backup
if "%choice%"=="4" goto details
if "%choice%"=="5" goto checkupdate
if "%choice%"=="6" start devmgmt.msc & goto menu
if "%choice%"=="7" goto export
if "%choice%"=="8" exit /b

goto menu

:listall
echo.
echo All Installed Drivers:
driverquery | more
echo.
pause
goto menu

:listrunning
echo.
echo Running Drivers:
driverquery /v | findstr "Running" | more
echo.
pause
goto menu

:backup
if not exist "%USERPROFILE%\Desktop\DriverBackup" mkdir "%USERPROFILE%\Desktop\DriverBackup"
echo.
echo Backing up drivers...
echo This may take several minutes...
dism /online /export-driver /destination:"%USERPROFILE%\Desktop\DriverBackup"
echo.
echo Drivers backed up to: %USERPROFILE%\Desktop\DriverBackup
pause
goto menu

:details
echo.
echo Detailed Driver Information:
driverquery /v /fo list | more
echo.
pause
goto menu

:checkupdate
echo.
echo Opening Windows Update - Driver Updates...
start ms-settings:windowsupdate
echo.
echo Check for driver updates in Windows Update.
pause
goto menu

:export
set exportfile=%USERPROFILE%\Desktop\DriverList_%date:~-4,4%%date:~-10,2%%date:~-7,2%.txt
set exportfile=%exportfile: =0%

echo.
echo Exporting driver list...
driverquery /v > "%exportfile%"
echo.
echo Driver list exported to: %exportfile%
pause
goto menu
