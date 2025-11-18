@echo off
REM ==========================================
REM Volume Control
REM Control system volume
REM ==========================================

title Volume Control

:menu
cls
echo ========================================
echo          VOLUME CONTROL
echo ========================================
echo.
echo 1. Volume Up
echo 2. Volume Down
echo 3. Mute/Unmute
echo 4. Set to 50%%
echo 5. Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto volup
if "%choice%"=="2" goto voldown
if "%choice%"=="3" goto mute
if "%choice%"=="4" goto vol50
if "%choice%"=="5" exit
goto menu

:volup
nircmd.exe changesysvolume 2000
echo Volume increased
timeout /t 1 >nul
goto menu

:voldown
nircmd.exe changesysvolume -2000
echo Volume decreased
timeout /t 1 >nul
goto menu

:mute
nircmd.exe mutesysvolume 2
echo Mute toggled
timeout /t 1 >nul
goto menu

:vol50
nircmd.exe setsysvolume 32768
echo Volume set to 50%%
timeout /t 1 >nul
goto menu
