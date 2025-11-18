@echo off
REM Auto-update time every 60 seconds
REM Run this to continuously update the desktop time file
REM Compatible with modern Windows (uses PowerShell)

set desktop=%USERPROFILE%\Desktop
set timefile=%desktop%\CURRENT_TIME.txt

echo Starting VATSAL AI Auto Time Updater...
echo Time file will be updated every 60 seconds
echo Press Ctrl+C to stop
echo.

:LOOP
REM Get current date and time using PowerShell
for /f "tokens=*" %%i in ('powershell -Command "Get-Date -Format 'MM/dd/yyyy'"') do set formatted_date=%%i
for /f "tokens=*" %%i in ('powershell -Command "Get-Date -Format 'HH:mm:ss'"') do set formatted_time=%%i
for /f "tokens=*" %%i in ('powershell -Command "Get-Date -Format 'ddd'"') do set day_of_week=%%i
for /f "tokens=*" %%i in ('powershell -Command "Get-Date -Format 'MM/dd/yyyy hh:mm:ss tt'"') do set full_timestamp=%%i

REM Update file
echo ================================================ > "%timefile%"
echo           CURRENT DATE AND TIME                >> "%timefile%"
echo ================================================ >> "%timefile%"
echo. >> "%timefile%"
echo Date: %formatted_date% >> "%timefile%"
echo Time: %formatted_time% >> "%timefile%"
echo. >> "%timefile%"
echo Day of Week: %day_of_week% >> "%timefile%"
echo. >> "%timefile%"
echo Last Updated: %full_timestamp% >> "%timefile%"
echo ================================================ >> "%timefile%"

echo Updated at %formatted_time%
timeout /t 60 >nul
goto LOOP
