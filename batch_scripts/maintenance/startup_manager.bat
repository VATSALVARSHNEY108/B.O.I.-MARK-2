@echo off
REM ==========================================
REM Startup Programs Manager
REM View and manage startup programs
REM ==========================================

title Startup Manager

:menu
cls
echo ========================================
echo     STARTUP PROGRAMS MANAGER
echo ========================================
echo.
echo 1. List Startup Programs
echo 2. Disable Startup Program
echo 3. Open Startup Folder
echo 4. Open Task Manager (Startup Tab)
echo 5. Create Startup Entry
echo 6. Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto list
if "%choice%"=="2" goto disable
if "%choice%"=="3" goto openfolder
if "%choice%"=="4" goto taskmgr
if "%choice%"=="5" goto create
if "%choice%"=="6" exit
goto menu

:list
cls
echo Startup Programs:
echo.
echo === User Startup Programs ===
dir /b "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
echo.
echo === All Users Startup Programs ===
dir /b "%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
echo.
echo === Registry Startup Programs ===
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
echo.
pause
goto menu

:disable
cls
echo Current startup programs:
dir /b "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
echo.
set /p program="Enter exact filename to disable (e.g., program.lnk): "
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\%program%" (
    move "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\%program%" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\%program%.disabled"
    echo Program disabled
) else (
    echo Program not found
)
timeout /t 2 >nul
goto menu

:openfolder
start "" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
goto menu

:taskmgr
start taskmgr /0 /startup
goto menu

:create
cls
set /p program_path="Enter full path to program: "
set /p program_name="Enter shortcut name: "
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\%program_name%.lnk');$s.TargetPath='%program_path%';$s.Save()"
echo Startup entry created
timeout /t 2 >nul
goto menu
