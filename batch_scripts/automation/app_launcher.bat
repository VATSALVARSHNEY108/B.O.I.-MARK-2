@echo off
REM ==========================================
REM QUICK APP LAUNCHER
REM Launch multiple apps at once
REM ==========================================

color 0F
title Quick App Launcher

:menu
cls
echo ========================================
echo      QUICK APP LAUNCHER
echo ========================================
echo.
echo === PRESETS ===
echo 1. Work Setup (Browser, Email, Office)
echo 2. Development Setup (VSCode, Terminal, Browser)
echo 3. Gaming Setup (Steam, Discord)
echo 4. Media Setup (Spotify, VLC)
echo 5. Study Setup (OneNote, Browser)
echo.
echo === CUSTOM ===
echo 6. Launch Single App
echo 7. Create Custom Preset
echo 8. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto work
if "%choice%"=="2" goto dev
if "%choice%"=="3" goto gaming
if "%choice%"=="4" goto media
if "%choice%"=="5" goto study
if "%choice%"=="6" goto single
if "%choice%"=="7" goto custom
if "%choice%"=="8" exit /b

goto menu

:work
echo.
echo Launching Work Setup...
start chrome.exe
start outlook.exe
start winword.exe
echo Work apps launched!
timeout /t 2 >nul
goto menu

:dev
echo.
echo Launching Development Setup...
start code
start cmd
start chrome.exe
echo Development apps launched!
timeout /t 2 >nul
goto menu

:gaming
echo.
echo Launching Gaming Setup...
start steam://open/bigpicture
start discord
echo Gaming apps launched!
timeout /t 2 >nul
goto menu

:media
echo.
echo Launching Media Setup...
start spotify:
start vlc
echo Media apps launched!
timeout /t 2 >nul
goto menu

:study
echo.
echo Launching Study Setup...
start onenote:
start chrome.exe
echo Study apps launched!
timeout /t 2 >nul
goto menu

:single
set /p appname="Enter application name or path: "
start "" "%appname%"
echo.
pause
goto menu

:custom
echo.
echo Custom Preset Creator
echo Enter app names/paths (one per line, enter 'done' to finish):
set count=1
:inputloop
set /p app%count%="App %count%: "
if "!app%count%!"=="done" goto launchcustom
set /a count+=1
goto inputloop

:launchcustom
set /a count-=1
echo.
echo Launching custom preset...
for /L %%i in (1,1,%count%) do (
    start "" "!app%%i!"
)
echo Custom apps launched!
pause
goto menu
