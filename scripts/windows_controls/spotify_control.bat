@echo off
REM ==========================================
REM Spotify Control
REM Control Spotify playback from command line
REM ==========================================

title Spotify Control
color 0A

if "%1"=="" goto menu

REM Command line mode
set command=%1

if "%command%"=="play" goto play
if "%command%"=="pause" goto pause
if "%command%"=="next" goto next
if "%command%"=="prev" goto prev
if "%command%"=="previous" goto prev
if "%command%"=="volup" goto volup
if "%command%"=="voldown" goto voldown
if "%command%"=="shuffle" goto shuffle
if "%command%"=="repeat" goto repeat
if "%command%"=="open" goto open
goto unknown

:menu
cls
echo ========================================
echo        SPOTIFY CONTROL
echo ========================================
echo.
echo 1. Play / Pause
echo 2. Next Track
echo 3. Previous Track
echo 4. Volume Up
echo 5. Volume Down
echo 6. Toggle Shuffle
echo 7. Toggle Repeat
echo 8. Open Spotify
echo 9. Exit
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto play
if "%choice%"=="2" goto next
if "%choice%"=="3" goto prev
if "%choice%"=="4" goto volup
if "%choice%"=="5" goto voldown
if "%choice%"=="6" goto shuffle
if "%choice%"=="7" goto repeat
if "%choice%"=="8" goto open
if "%choice%"=="9" exit
goto menu

:play
echo ⏯️  Play/Pause
powershell -Command "(New-Object -ComObject WScript.Shell).SendKeys('{MEDIA_PLAY_PAUSE}')"
if "%1"=="" (
    timeout /t 1 >nul
    goto menu
) else (
    exit /b
)

:pause
echo ⏸️ Pause
powershell -Command "(New-Object -ComObject WScript.Shell).SendKeys('{MEDIA_PLAY_PAUSE}')"
if "%1"=="" (
    timeout /t 1 >nul
    goto menu
) else (
    exit /b
)

:next
echo ⏭️ Next Track
powershell -Command "(New-Object -ComObject WScript.Shell).SendKeys('{MEDIA_NEXT_TRACK}')"
if "%1"=="" (
    timeout /t 1 >nul
    goto menu
) else (
    exit /b
)

:prev
echo ⏮️ Previous Track
powershell -Command "(New-Object -ComObject WScript.Shell).SendKeys('{MEDIA_PREV_TRACK}')"
if "%1"=="" (
    timeout /t 1 >nul
    goto menu
) else (
    exit /b
)

:volup
echo 🔊 Volume Up
nircmd changesysvolume 2000
if "%1"=="" (
    timeout /t 1 >nul
    goto menu
) else (
    exit /b
)

:voldown
echo 🔉 Volume Down
nircmd changesysvolume -2000
if "%1"=="" (
    timeout /t 1 >nul
    goto menu
) else (
    exit /b
)

:shuffle
echo 🔀 Toggle Shuffle
REM Ctrl+S for Spotify
powershell -Command "$wshell = New-Object -ComObject wscript.shell; $wshell.SendKeys('^s')"
if "%1"=="" (
    timeout /t 1 >nul
    goto menu
) else (
    exit /b
)

:repeat
echo 🔁 Toggle Repeat
REM Ctrl+R for Spotify
powershell -Command "$wshell = New-Object -ComObject wscript.shell; $wshell.SendKeys('^r')"
if "%1"=="" (
    timeout /t 1 >nul
    goto menu
) else (
    exit /b
)

:open
echo 🎵 Opening Spotify...
start spotify:
if "%1"=="" (
    timeout /t 2 >nul
    goto menu
) else (
    exit /b
)

:unknown
echo ❌ Unknown command: %command%
echo.
echo Available commands:
echo   play, pause, next, prev, volup, voldown, shuffle, repeat, open
echo.
echo Example: spotify_control.bat play
exit /b

:end
