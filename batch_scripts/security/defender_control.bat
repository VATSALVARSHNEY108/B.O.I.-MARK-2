@echo off
REM ==========================================
REM WINDOWS DEFENDER CONTROL
REM Manage Windows Defender settings
REM ==========================================

color 0C
title Windows Defender Control

:menu
cls
echo ========================================
echo    WINDOWS DEFENDER CONTROL
echo ========================================
echo.
echo 1. Quick Scan
echo 2. Full Scan
echo 3. Custom Scan
echo 4. Update Definitions
echo 5. View Protection Status
echo 6. View Threat History
echo 7. Open Windows Security
echo 8. Exclusions Management
echo 9. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto quickscan
if "%choice%"=="2" goto fullscan
if "%choice%"=="3" goto customscan
if "%choice%"=="4" goto update
if "%choice%"=="5" goto status
if "%choice%"=="6" goto history
if "%choice%"=="7" start windowsdefender: & goto menu
if "%choice%"=="8" goto exclusions
if "%choice%"=="9" exit /b

goto menu

:quickscan
echo.
echo Starting Quick Scan...
"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -Scan -ScanType 1
echo.
echo Quick scan completed!
pause
goto menu

:fullscan
echo.
echo Starting Full Scan (This may take a while)...
"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -Scan -ScanType 2
echo.
echo Full scan completed!
pause
goto menu

:customscan
set /p scanpath="Enter path to scan: "
echo.
echo Scanning %scanpath%...
"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -Scan -ScanType 3 -File "%scanpath%"
echo.
echo Custom scan completed!
pause
goto menu

:update
echo.
echo Updating virus definitions...
"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -SignatureUpdate
echo.
echo Definitions updated!
pause
goto menu

:status
echo.
echo Windows Defender Status:
powershell Get-MpComputerStatus
echo.
pause
goto menu

:history
echo.
echo Threat History:
powershell Get-MpThreatDetection
echo.
pause
goto menu

:exclusions
cls
echo ========================================
echo      EXCLUSION MANAGEMENT
echo ========================================
echo.
echo 1. Add Folder Exclusion
echo 2. Add File Exclusion
echo 3. View Current Exclusions
echo 4. Back
echo.
set /p exchoice="Select option: "

if "%exchoice%"=="1" goto addfolder
if "%exchoice%"=="2" goto addfile
if "%exchoice%"=="3" goto viewexclusions
if "%exchoice%"=="4" goto menu

:addfolder
set /p folder="Enter folder path: "
powershell Add-MpPreference -ExclusionPath "%folder%"
echo Folder added to exclusions!
pause
goto exclusions

:addfile
set /p file="Enter file path: "
powershell Add-MpPreference -ExclusionPath "%file%"
echo File added to exclusions!
pause
goto exclusions

:viewexclusions
echo.
echo Current Exclusions:
powershell Get-MpPreference ^| Select-Object ExclusionPath
echo.
pause
goto exclusions
