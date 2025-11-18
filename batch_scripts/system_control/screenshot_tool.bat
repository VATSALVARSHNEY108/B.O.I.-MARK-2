@echo off
REM ==========================================
REM Screenshot Tool
REM Capture screenshots with options
REM ==========================================

title Screenshot Tool

:menu
cls
echo ========================================
echo        SCREENSHOT TOOL
echo ========================================
echo.
echo 1. Take Screenshot Now
echo 2. Take Screenshot in 5 seconds
echo 3. Take Screenshot in 10 seconds
echo 4. Open Screenshots Folder
echo 5. Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto now
if "%choice%"=="2" goto delay5
if "%choice%"=="3" goto delay10
if "%choice%"=="4" goto open
if "%choice%"=="5" exit
goto menu

:now
set filename=Screenshot_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.png
set filename=%filename: =0%
powershell -command "Add-Type -AssemblyName System.Windows.Forms; $screen = [System.Windows.Forms.SystemInformation]::VirtualScreen; $bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height; $graphics = [System.Drawing.Graphics]::FromImage($bitmap); $graphics.CopyFromScreen($screen.Left, $screen.Top, 0, 0, $bitmap.Size); $bitmap.Save('%USERPROFILE%\Pictures\%filename%'); $bitmap.Dispose(); $graphics.Dispose()"
echo Screenshot saved to: %USERPROFILE%\Pictures\%filename%
timeout /t 2 >nul
goto menu

:delay5
echo Taking screenshot in 5 seconds...
timeout /t 5 >nul
goto now

:delay10
echo Taking screenshot in 10 seconds...
timeout /t 10 >nul
goto now

:open
start %USERPROFILE%\Pictures
goto menu
