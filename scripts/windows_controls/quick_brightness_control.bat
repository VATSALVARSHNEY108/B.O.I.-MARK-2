@echo off
REM Quick Brightness Control - Simple commands without menu
REM Usage: quick_brightness_control.bat [value]
REM 
REM value: 0-100 (brightness percentage)
REM
REM Examples:
REM   quick_brightness_control.bat 50
REM   quick_brightness_control.bat 100

if "%1"=="" goto USAGE

set /a level=%1
if %level% LSS 0 set level=0
if %level% GTR 100 set level=100

echo Setting brightness to %level%%%...
powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,%level%)
echo Done!
goto END

:USAGE
echo.
echo Quick Brightness Control
echo ========================
echo Usage: quick_brightness_control.bat [value]
echo.
echo value: 0-100 (brightness percentage)
echo.
echo Examples:
echo   quick_brightness_control.bat 50
echo   quick_brightness_control.bat 100
echo.

:END
