@echo off
REM Display current date and time on desktop
REM This batch file creates a desktop file with current time/date
REM Compatible with modern Windows (uses PowerShell fallback when wmic is unavailable)

REM Get current date and time using PowerShell (works on all modern Windows)
for /f "tokens=*" %%i in ('powershell -Command "Get-Date -Format 'MM/dd/yyyy'"') do set formatted_date=%%i
for /f "tokens=*" %%i in ('powershell -Command "Get-Date -Format 'HH:mm:ss'"') do set formatted_time=%%i
for /f "tokens=*" %%i in ('powershell -Command "Get-Date -Format 'ddd'"') do set day_of_week=%%i
for /f "tokens=*" %%i in ('powershell -Command "Get-Date -Format 'MM/dd/yyyy hh:mm:ss tt'"') do set full_timestamp=%%i

REM Create/update desktop time file
set desktop=%USERPROFILE%\Desktop
set timefile=%desktop%\CURRENT_TIME.txt

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

REM Show message
echo Time and date saved to: %timefile%
echo.
type "%timefile%"
echo.
echo Press any key to close...
pause >nul
