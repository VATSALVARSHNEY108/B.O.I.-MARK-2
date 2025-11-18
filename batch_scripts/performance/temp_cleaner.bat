@echo off
REM ==========================================
REM TEMP FILES CLEANER
REM Remove temporary and junk files
REM ==========================================

color 0A
title Temp Files Cleaner

:menu
cls
echo ========================================
echo      TEMP FILES CLEANER
echo ========================================
echo.
echo 1. Clean Windows Temp Files
echo 2. Clean User Temp Files
echo 3. Clean Prefetch Files
echo 4. Clean Recent Files List
echo 5. Clean Recycle Bin
echo 6. Clean Windows Update Cache
echo 7. Clean ALL (Recommended)
echo 8. View Temp Folder Sizes
echo 9. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto wintemp
if "%choice%"=="2" goto usertemp
if "%choice%"=="3" goto prefetch
if "%choice%"=="4" goto recent
if "%choice%"=="5" goto recycle
if "%choice%"=="6" goto wutemp
if "%choice%"=="7" goto cleanall
if "%choice%"=="8" goto viewsizes
if "%choice%"=="9" exit /b

goto menu

:wintemp
echo.
echo Cleaning Windows Temp Files...
del /f /s /q %windir%\temp\*.* 2>nul
echo Windows temp cleaned!
timeout /t 2 >nul
goto menu

:usertemp
echo.
echo Cleaning User Temp Files...
del /f /s /q %temp%\*.* 2>nul
echo User temp cleaned!
timeout /t 2 >nul
goto menu

:prefetch
echo.
echo Cleaning Prefetch Files...
del /f /s /q %windir%\Prefetch\*.* 2>nul
echo Prefetch cleaned!
timeout /t 2 >nul
goto menu

:recent
echo.
echo Cleaning Recent Files...
del /f /s /q %appdata%\Microsoft\Windows\Recent\*.* 2>nul
echo Recent files list cleared!
timeout /t 2 >nul
goto menu

:recycle
echo.
echo Emptying Recycle Bin...
rd /s /q %systemdrive%\$Recycle.bin 2>nul
echo Recycle Bin emptied!
timeout /t 2 >nul
goto menu

:wutemp
echo.
echo Cleaning Windows Update Cache...
net stop wuauserv
del /f /s /q %windir%\SoftwareDistribution\Download\*.* 2>nul
net start wuauserv
echo Windows Update cache cleaned!
timeout /t 2 >nul
goto menu

:cleanall
echo.
echo ========================================
echo     CLEANING ALL TEMP FILES
echo ========================================
echo.
echo This will clean:
echo - Windows Temp
echo - User Temp
echo - Prefetch
echo - Recent Files
echo - Recycle Bin
echo - Windows Update Cache
echo.
set /p confirm="Continue? (Y/N): "
if /i not "%confirm%"=="Y" goto menu

echo.
echo Cleaning in progress...
del /f /s /q %windir%\temp\*.* 2>nul
del /f /s /q %temp%\*.* 2>nul
del /f /s /q %windir%\Prefetch\*.* 2>nul
del /f /s /q %appdata%\Microsoft\Windows\Recent\*.* 2>nul
rd /s /q %systemdrive%\$Recycle.bin 2>nul
net stop wuauserv 2>nul
del /f /s /q %windir%\SoftwareDistribution\Download\*.* 2>nul
net start wuauserv 2>nul

echo.
echo All temp files cleaned successfully!
echo System should be faster now.
pause
goto menu

:viewsizes
echo.
echo Calculating temp folder sizes...
echo.
echo Windows Temp:
powershell "'{0:N2} MB' -f ((Get-ChildItem -Path $env:windir\temp -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB)"
echo.
echo User Temp:
powershell "'{0:N2} MB' -f ((Get-ChildItem -Path $env:temp -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB)"
echo.
echo Prefetch:
powershell "'{0:N2} MB' -f ((Get-ChildItem -Path $env:windir\Prefetch -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB)"
echo.
pause
goto menu
