@echo off
REM ==========================================
REM DISK DEFRAGMENTATION
REM Optimize and defragment drives
REM ==========================================

color 0A
title Disk Defragmentation

:menu
cls
echo ========================================
echo     DISK DEFRAGMENTATION
echo ========================================
echo.
echo 1. Analyze C: Drive
echo 2. Defragment C: Drive
echo 3. Analyze All Drives
echo 4. Defragment All Drives
echo 5. Optimize SSD (TRIM)
echo 6. View Defrag Schedule
echo 7. Open Defragment Tool
echo 8. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto analyzec
if "%choice%"=="2" goto defragc
if "%choice%"=="3" goto analyzeall
if "%choice%"=="4" goto defragall
if "%choice%"=="5" goto ssd
if "%choice%"=="6" goto schedule
if "%choice%"=="7" start dfrgui & goto menu
if "%choice%"=="8" exit /b

goto menu

:analyzec
echo.
echo Analyzing C: drive...
defrag C: /A
echo.
pause
goto menu

:defragc
echo.
echo Defragmenting C: drive...
echo This may take a while depending on disk size and fragmentation.
defrag C: /U /V
echo.
echo Defragmentation complete!
pause
goto menu

:analyzeall
echo.
echo Analyzing all drives...
defrag /C /A
echo.
pause
goto menu

:defragall
echo.
echo WARNING: This will defragment all drives!
set /p confirm="Continue? (Y/N): "
if /i not "%confirm%"=="Y" goto menu
echo.
echo Defragmenting all drives...
defrag /C /U /V
echo.
echo All drives defragmented!
pause
goto menu

:ssd
echo.
echo Optimizing SSD drives (TRIM)...
defrag C: /L /O
echo.
echo SSD optimization complete!
pause
goto menu

:schedule
echo.
echo Current Defragmentation Schedule:
powershell Get-ScheduledTask -TaskName "ScheduledDefrag"
echo.
pause
goto menu
