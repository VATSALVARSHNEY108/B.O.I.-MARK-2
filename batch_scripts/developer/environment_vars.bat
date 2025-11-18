@echo off
REM ==========================================
REM ENVIRONMENT VARIABLES MANAGER
REM View and manage system variables
REM ==========================================

color 0E
title Environment Variables Manager

:menu
cls
echo ========================================
echo   ENVIRONMENT VARIABLES MANAGER
echo ========================================
echo.
echo 1. View All Variables
echo 2. View User Variables
echo 3. View System Variables
echo 4. View PATH Variable
echo 5. Add to PATH (User)
echo 6. Add to PATH (System)
echo 7. Create User Variable
echo 8. Create System Variable
echo 9. Delete Variable
echo 10. Open Environment Variables
echo 11. Export Variables to File
echo 12. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto viewall
if "%choice%"=="2" goto viewuser
if "%choice%"=="3" goto viewsystem
if "%choice%"=="4" goto viewpath
if "%choice%"=="5" goto adduserpath
if "%choice%"=="6" goto addsystempath
if "%choice%"=="7" goto createuser
if "%choice%"=="8" goto createsystem
if "%choice%"=="9" goto delete
if "%choice%"=="10" goto openenv
if "%choice%"=="11" goto export
if "%choice%"=="12" exit /b

goto menu

:viewall
echo.
echo All Environment Variables:
set | more
echo.
pause
goto menu

:viewuser
echo.
echo User Environment Variables:
reg query "HKCU\Environment" | more
echo.
pause
goto menu

:viewsystem
echo.
echo System Environment Variables:
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" | more
echo.
pause
goto menu

:viewpath
echo.
echo Current PATH Variable:
echo %PATH%
echo.
pause
goto menu

:adduserpath
set /p newpath="Enter path to add: "
setx PATH "%PATH%;%newpath%"
echo.
echo Path added to user PATH! Restart terminal to apply.
pause
goto menu

:addsystempath
set /p newpath="Enter path to add: "
echo.
echo Adding to system PATH requires administrator privileges...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d "%PATH%;%newpath%" /f
echo.
echo Path added! Restart required to apply.
pause
goto menu

:createuser
set /p varname="Enter variable name: "
set /p varvalue="Enter variable value: "
setx %varname% "%varvalue%"
echo.
echo User variable created! Restart terminal to apply.
pause
goto menu

:createsystem
set /p varname="Enter variable name: "
set /p varvalue="Enter variable value: "
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v %varname% /t REG_SZ /d "%varvalue%" /f
echo.
echo System variable created! Restart required to apply.
pause
goto menu

:delete
echo.
echo WARNING: Be careful when deleting variables!
set /p varname="Enter variable name to delete: "
set /p vartype="Type (USER/SYSTEM): "

if /i "%vartype%"=="USER" (
    reg delete "HKCU\Environment" /v %varname% /f
    echo User variable deleted!
) else if /i "%vartype%"=="SYSTEM" (
    reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v %varname% /f
    echo System variable deleted!
) else (
    echo Invalid type!
)
pause
goto menu

:openenv
start sysdm.cpl
echo.
echo Go to: Advanced tab ^> Environment Variables
pause
goto menu

:export
set exportfile=%USERPROFILE%\Desktop\EnvironmentVariables_%date:~-4,4%%date:~-10,2%%date:~-7,2%.txt
set exportfile=%exportfile: =0%

echo.
echo Exporting environment variables...
set > "%exportfile%"
echo.
echo Variables exported to: %exportfile%
pause
goto menu
