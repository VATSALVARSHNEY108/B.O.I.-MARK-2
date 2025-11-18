@echo off
REM ==========================================
REM Disk Cleanup & Optimization
REM Clean temporary files and optimize disk
REM ==========================================

title Disk Cleanup

echo ========================================
echo      DISK CLEANUP & OPTIMIZATION
echo ========================================
echo.
echo This will clean temporary files and optimize your disk
echo.
pause

echo.
echo [1/5] Cleaning Windows Temp folder...
del /f /s /q %windir%\temp\*.* >nul 2>&1
rd /s /q %windir%\temp >nul 2>&1
mkdir %windir%\temp

echo [2/5] Cleaning User Temp folder...
del /f /s /q %temp%\*.* >nul 2>&1
rd /s /q %temp% >nul 2>&1
mkdir %temp%

echo [3/5] Cleaning Prefetch...
del /f /s /q %windir%\Prefetch\*.* >nul 2>&1

echo [4/5] Cleaning Recycle Bin...
rd /s /q %systemdrive%\$Recycle.bin >nul 2>&1

echo [5/5] Running Disk Cleanup utility...
cleanmgr /sagerun:1

echo.
echo ========================================
echo Cleanup complete!
echo ========================================
pause
