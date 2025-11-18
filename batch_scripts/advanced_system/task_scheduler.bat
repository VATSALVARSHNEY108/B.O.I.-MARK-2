@echo off
REM ==========================================
REM TASK SCHEDULER MANAGER
REM Manage scheduled tasks
REM ==========================================

color 0D
title Task Scheduler Manager

:menu
cls
echo ========================================
echo    TASK SCHEDULER MANAGER
echo ========================================
echo.
echo 1. List All Tasks
echo 2. List Running Tasks
echo 3. Create New Task
echo 4. Delete Task
echo 5. Enable Task
echo 6. Disable Task
echo 7. Run Task Now
echo 8. Open Task Scheduler
echo 9. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto listtasks
if "%choice%"=="2" goto runningtasks
if "%choice%"=="3" goto createtask
if "%choice%"=="4" goto deletetask
if "%choice%"=="5" goto enabletask
if "%choice%"=="6" goto disabletask
if "%choice%"=="7" goto runtask
if "%choice%"=="8" start taskschd.msc & goto menu
if "%choice%"=="9" exit /b

goto menu

:listtasks
echo.
echo All Scheduled Tasks:
schtasks /query /fo LIST | more
echo.
pause
goto menu

:runningtasks
echo.
echo Currently Running Tasks:
schtasks /query /fo LIST /v | findstr "Running" | more
echo.
pause
goto menu

:createtask
echo.
echo === CREATE NEW TASK ===
set /p taskname="Enter task name: "
set /p program="Enter program path: "
set /p triggertype="Trigger type (DAILY/WEEKLY/MONTHLY/ONCE/ONLOGON): "
set /p starttime="Start time (HH:MM format, e.g., 14:30): "

echo.
echo Creating task...
schtasks /create /tn "%taskname%" /tr "%program%" /sc %triggertype% /st %starttime%
echo.
echo Task created successfully!
pause
goto menu

:deletetask
set /p taskname="Enter task name to delete: "
echo.
set /p confirm="Delete task '%taskname%'? (Y/N): "
if /i "%confirm%"=="Y" (
    schtasks /delete /tn "%taskname%" /f
    echo Task deleted!
) else (
    echo Operation cancelled.
)
pause
goto menu

:enabletask
set /p taskname="Enter task name to enable: "
schtasks /change /tn "%taskname%" /enable
echo.
echo Task enabled!
pause
goto menu

:disabletask
set /p taskname="Enter task name to disable: "
schtasks /change /tn "%taskname%" /disable
echo.
echo Task disabled!
pause
goto menu

:runtask
set /p taskname="Enter task name to run: "
schtasks /run /tn "%taskname%"
echo.
echo Task started!
pause
goto menu
