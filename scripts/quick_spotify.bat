@echo off
REM Quick Spotify Controls - No menu

if "%1"=="play" goto play
if "%1"=="pause" goto pause
if "%1"=="next" goto next
if "%1"=="prev" goto prev
if "%1"=="open" goto open

echo Usage: quick_spotify.bat [play^|pause^|next^|prev^|open]
exit /b

:play
powershell -Command "(New-Object -ComObject WScript.Shell).SendKeys('{MEDIA_PLAY_PAUSE}')"
echo ⏯️  Play/Pause
exit /b

:pause
powershell -Command "(New-Object -ComObject WScript.Shell).SendKeys('{MEDIA_PLAY_PAUSE}')"
echo ⏸️ Paused
exit /b

:next
powershell -Command "(New-Object -ComObject WScript.Shell).SendKeys('{MEDIA_NEXT_TRACK}')"
echo ⏭️ Next track
exit /b

:prev
powershell -Command "(New-Object -ComObject WScript.Shell).SendKeys('{MEDIA_PREV_TRACK}')"
echo ⏮️ Previous track
exit /b

:open
start spotify:
echo 🎵 Opening Spotify...
exit /b
