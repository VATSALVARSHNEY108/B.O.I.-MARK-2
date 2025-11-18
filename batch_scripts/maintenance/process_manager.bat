@echo off
REM ==========================================
REM Process Manager
REM View and manage running processes
REM ==========================================

title Process Manager

:menu
cls
echo ========================================
echo        PROCESS MANAGER
echo ========================================
echo.
echo 1. List All Processes
echo 2. Kill Process by Name
echo 3. Kill Process by PID
echo 4. Show CPU Usage
echo 5. Show Memory Usage
echo 6. Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto list
if "%choice%"=="2" goto killname
if "%choice%"=="3" goto killpid
if "%choice%"=="4" goto cpu
if "%choice%"=="5" goto memory
if "%choice%"=="6" exit
goto menu

:list
cls
echo Running Processes:
echo.
tasklist
echo.
pause
goto menu

:killname
cls
set /p process="Enter process name (e.g., chrome.exe): "
taskkill /IM "%process%" /F
echo.
echo Process killed (if it was running)
timeout /t 2 >nul
goto menu

:killpid
cls
set /p pid="Enter process PID: "
taskkill /PID %pid% /F
echo.
echo Process killed (if it existed)
timeout /t 2 >nul
goto menu

:cpu
cls
echo CPU Usage by Process:
echo.
wmic cpu get loadpercentage
wmic process get name,percentprocessortime | sort
echo.
pause
goto menu

:memory
cls
echo Memory Usage by Process:
echo.
tasklist /FI "MEMUSAGE gt 0" | sort
echo.
pause
goto menu
