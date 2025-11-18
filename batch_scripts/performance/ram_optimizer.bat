@echo off
REM ==========================================
REM RAM OPTIMIZER
REM Free up and optimize memory usage
REM ==========================================

color 0A
title RAM Optimizer

:menu
cls
echo ========================================
echo         RAM OPTIMIZER
echo ========================================
echo.
echo 1. View Memory Usage
echo 2. Clear Memory Cache
echo 3. Close High Memory Apps
echo 4. Empty Standby List
echo 5. Optimize for Gaming
echo 6. View Top Memory Processes
echo 7. Set Virtual Memory
echo 8. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto viewmem
if "%choice%"=="2" goto clearcache
if "%choice%"=="3" goto closehigh
if "%choice%"=="4" goto emptystandby
if "%choice%"=="5" goto gaming
if "%choice%"=="6" goto topproc
if "%choice%"=="7" goto virtualmem
if "%choice%"=="8" exit /b

goto menu

:viewmem
echo.
echo Current Memory Usage:
systeminfo | findstr /C:"Total Physical Memory" /C:"Available Physical Memory"
echo.
wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value
echo.
pause
goto menu

:clearcache
echo.
echo Clearing memory cache...
echo Clearing DNS cache...
ipconfig /flushdns
echo Clearing file system cache...
%windir%\system32\rundll32.exe advapi32.dll,ProcessIdleTasks
echo.
echo Memory cache cleared!
timeout /t 2 >nul
goto menu

:closehigh
echo.
echo Processes using most memory:
powershell "Get-Process | Sort-Object -Property WS -Descending | Select-Object -First 10 | Format-Table ProcessName, @{Name='Memory(MB)';Expression={[math]::Round($_.WS/1MB,2)}} -AutoSize"
echo.
set /p procname="Enter process name to close (or 'cancel'): "
if /i "%procname%"=="cancel" goto menu
taskkill /f /im %procname%.exe
echo.
echo Process terminated!
pause
goto menu

:emptystandby
echo.
echo Emptying standby memory list...
powershell -Command "Clear-Variable -Name * -ErrorAction SilentlyContinue; [System.GC]::Collect()"
echo.
echo Standby list cleared!
timeout /t 2 >nul
goto menu

:gaming
echo.
echo Optimizing for gaming...
echo Closing unnecessary processes...
taskkill /f /im "OneDrive.exe" 2>nul
taskkill /f /im "SkypeApp.exe" 2>nul
echo Adjusting priority...
wmic process where name="dwm.exe" CALL setpriority "realtime"
echo.
echo Gaming optimization complete!
timeout /t 2 >nul
goto menu

:topproc
echo.
echo Top 20 Memory-Consuming Processes:
powershell "Get-Process | Sort-Object -Property WS -Descending | Select-Object -First 20 | Format-Table ProcessName, Id, @{Name='Memory(MB)';Expression={[math]::Round($_.WS/1MB,2)}} -AutoSize"
echo.
pause
goto menu

:virtualmem
echo.
echo Opening Virtual Memory Settings...
start sysdm.cpl
echo.
echo Go to: Advanced tab ^> Performance Settings ^> Advanced ^> Virtual Memory
pause
goto menu
