@echo off
REM Quick Volume Control - Simple commands without menu
REM Usage: quick_volume_control.bat [command] [value]
REM 
REM Commands:
REM   set [0-100]     - Set volume to specific percentage
REM   up [amount]     - Increase volume (default 10)
REM   down [amount]   - Decrease volume (default 10)
REM   mute            - Toggle mute
REM   get             - Show current volume
REM
REM Examples:
REM   quick_volume_control.bat set 80
REM   quick_volume_control.bat up 5
REM   quick_volume_control.bat down 10
REM   quick_volume_control.bat mute

if "%1"=="" goto USAGE

if /i "%1"=="set" goto SET_VOLUME
if /i "%1"=="up" goto VOL_UP
if /i "%1"=="down" goto VOL_DOWN
if /i "%1"=="mute" goto MUTE
if /i "%1"=="get" goto GET_VOLUME

:USAGE
echo.
echo Quick Volume Control
echo ====================
echo Usage: quick_volume_control.bat [command] [value]
echo.
echo Commands:
echo   set [0-100]     - Set volume to specific percentage
echo   up [amount]     - Increase volume (default 10)
echo   down [amount]   - Decrease volume (default 10)
echo   mute            - Toggle mute
echo   get             - Show current volume
echo.
echo Examples:
echo   quick_volume_control.bat set 80
echo   quick_volume_control.bat up 5
echo   quick_volume_control.bat mute
echo.
goto END

:SET_VOLUME
if "%2"=="" (
    echo Error: Please specify volume level (0-100)
    goto END
)
set /a level=%2
if %level% LSS 0 set level=0
if %level% GTR 100 set level=100
set /a volvalue=%level% * 655
echo Setting volume to %level%%%...
nircmd.exe setsysvolume %volvalue%
echo Done!
goto END

:VOL_UP
set amount=10
if not "%2"=="" set amount=%2
set /a volvalue=%amount% * 655
echo Increasing volume by %amount%%%...
nircmd.exe changesysvolume %volvalue%
echo Done!
goto END

:VOL_DOWN
set amount=10
if not "%2"=="" set amount=%2
set /a volvalue=%amount% * 655
echo Decreasing volume by %amount%%%...
nircmd.exe changesysvolume -%volvalue%
echo Done!
goto END

:MUTE
echo Toggling mute...
nircmd.exe mutesysvolume 2
echo Done!
goto END

:GET_VOLUME
for /f "delims=" %%i in ('nircmd.exe getsysvolume') do set volraw=%%i
set /a volpercent=%volraw% / 655
echo Current Volume: %volpercent%%%
goto END

:END
