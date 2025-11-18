@echo off
REM ==========================================
REM USB Device Manager
REM View and safely eject USB devices
REM ==========================================

title USB Device Manager

:menu
cls
echo ========================================
echo       USB DEVICE MANAGER
echo ========================================
echo.
echo 1. List USB Devices
echo 2. Safely Eject USB Drive
echo 3. Show USB Drive Info
echo 4. Scan USB for Errors
echo 5. Format USB Drive
echo 6. Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto list
if "%choice%"=="2" goto eject
if "%choice%"=="3" goto info
if "%choice%"=="4" goto scan
if "%choice%"=="5" goto format
if "%choice%"=="6" exit
goto menu

:list
cls
echo USB Devices Connected:
echo ========================================
wmic logicaldisk where "drivetype=2" get caption,description,volumename,size,freespace
echo.
echo All Removable Drives:
wmic logicaldisk where "drivetype=2" get caption,volumename
echo.
pause
goto menu

:eject
cls
echo Available Drives:
wmic logicaldisk where "drivetype=2" get caption,volumename
echo.
set /p drive="Enter drive letter to eject (e.g., E): "
echo.
echo Ejecting drive %drive%:...
powershell -Command "(New-Object -ComObject Shell.Application).NameSpace(17).ParseName('%drive%:').InvokeVerb('Eject')"
echo Drive %drive%: can now be safely removed
timeout /t 3 >nul
goto menu

:info
cls
set /p drive="Enter drive letter (e.g., E): "
echo.
echo Drive %drive%: Information:
echo ========================================
wmic logicaldisk where "caption='%drive%:'" get caption,description,filesystem,freespace,size,volumename
fsutil fsinfo volumeinfo %drive%:
echo.
pause
goto menu

:scan
cls
set /p drive="Enter drive letter to scan (e.g., E): "
echo.
echo Scanning drive %drive%: for errors...
echo This may take a while...
chkdsk %drive%: /f /r
echo.
pause
goto menu

:format
cls
echo WARNING: This will erase ALL data on the drive!
echo.
wmic logicaldisk where "drivetype=2" get caption,volumename
echo.
set /p drive="Enter drive letter to format (e.g., E): "
set /p label="Enter volume label: "
set /p confirm="Are you sure? Type YES to confirm: "

if /i "%confirm%"=="YES" (
    echo.
    echo Formatting %drive%:...
    format %drive%: /FS:NTFS /V:%label% /Q
    echo.
    echo Format complete!
) else (
    echo Format cancelled
)
timeout /t 3 >nul
goto menu
