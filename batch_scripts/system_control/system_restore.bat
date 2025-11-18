@echo off
REM ==========================================
REM System Restore Manager
REM Create and manage restore points
REM ==========================================

title System Restore Manager

:menu
cls
echo ========================================
echo     SYSTEM RESTORE MANAGER
echo ========================================
echo.
echo 1. Create Restore Point
echo 2. List Restore Points
echo 3. Open System Restore
echo 4. Enable System Protection
echo 5. Disable System Protection
echo 6. Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto create
if "%choice%"=="2" goto list
if "%choice%"=="3" goto open
if "%choice%"=="4" goto enable
if "%choice%"=="5" goto disable
if "%choice%"=="6" exit
goto menu

:create
cls
set /p description="Enter restore point description: "
echo.
echo Creating restore point...
powershell -Command "Checkpoint-Computer -Description '%description%' -RestorePointType 'MODIFY_SETTINGS'"
echo.
echo Restore point created!
timeout /t 3 >nul
goto menu

:list
cls
echo Available Restore Points:
echo.
powershell -Command "Get-ComputerRestorePoint | Format-Table -AutoSize"
echo.
pause
goto menu

:open
rstrui.exe
goto menu

:enable
echo Enabling System Protection...
powershell -Command "Enable-ComputerRestore -Drive 'C:\'"
echo System Protection enabled!
timeout /t 2 >nul
goto menu

:disable
echo Disabling System Protection...
powershell -Command "Disable-ComputerRestore -Drive 'C:\'"
echo System Protection disabled!
timeout /t 2 >nul
goto menu
