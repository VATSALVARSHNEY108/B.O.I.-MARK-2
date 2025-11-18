@echo off
REM ==========================================
REM Power Options
REM Control system power settings
REM ==========================================

title Power Options

:menu
cls
echo ========================================
echo          POWER OPTIONS
echo ========================================
echo.
echo 1. Shutdown Computer
echo 2. Restart Computer
echo 3. Sleep Mode
echo 4. Hibernate
echo 5. Lock Computer
echo 6. Logoff
echo 7. Cancel
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto shutdown
if "%choice%"=="2" goto restart
if "%choice%"=="3" goto sleep
if "%choice%"=="4" goto hibernate
if "%choice%"=="5" goto lock
if "%choice%"=="6" goto logoff
if "%choice%"=="7" exit
goto menu

:shutdown
echo Shutting down in 5 seconds...
shutdown /s /t 5
goto end

:restart
echo Restarting in 5 seconds...
shutdown /r /t 5
goto end

:sleep
echo Going to sleep...
rundll32.exe powrprof.dll,SetSuspendState 0,1,0
goto end

:hibernate
echo Hibernating...
shutdown /h
goto end

:lock
echo Locking computer...
rundll32.exe user32.dll,LockWorkStation
goto end

:logoff
echo Logging off...
shutdown /l
goto end

:end
exit
