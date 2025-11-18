@echo off
REM ==========================================
REM REGISTRY BACKUP & RESTORE
REM Backup and restore Windows Registry
REM ==========================================

color 0D
title Registry Backup & Restore

:menu
cls
echo ========================================
echo    REGISTRY BACKUP ^& RESTORE
echo ========================================
echo.
echo 1. Backup Entire Registry
echo 2. Backup Specific Key
echo 3. Restore Registry Backup
echo 4. View Backup Location
echo 5. Open Registry Editor
echo 6. Back to Main Menu
echo.
echo WARNING: Registry operations are sensitive!
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto backupall
if "%choice%"=="2" goto backupkey
if "%choice%"=="3" goto restore
if "%choice%"=="4" goto viewlocation
if "%choice%"=="5" start regedit & goto menu
if "%choice%"=="6" exit /b

goto menu

:backupall
echo.
echo Creating backup folder...
if not exist "%USERPROFILE%\Desktop\RegistryBackups" mkdir "%USERPROFILE%\Desktop\RegistryBackups"

set backupfile=%USERPROFILE%\Desktop\RegistryBackups\FullRegistry_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%.reg
set backupfile=%backupfile: =0%

echo.
echo Backing up entire registry...
echo This may take several minutes...
reg export HKLM "%backupfile%" /y
reg export HKCU "%backupfile%.HKCU" /y
reg export HKCR "%backupfile%.HKCR" /y

echo.
echo Registry backup completed!
echo Location: %USERPROFILE%\Desktop\RegistryBackups
pause
goto menu

:backupkey
set /p regkey="Enter registry key path (e.g., HKLM\Software\Microsoft): "
if not exist "%USERPROFILE%\Desktop\RegistryBackups" mkdir "%USERPROFILE%\Desktop\RegistryBackups"

set backupfile=%USERPROFILE%\Desktop\RegistryBackups\RegKey_%date:~-4,4%%date:~-10,2%%date:~-7,2%.reg
set backupfile=%backupfile: =0%

echo.
echo Backing up registry key...
reg export "%regkey%" "%backupfile%" /y
echo.
echo Backup completed!
echo File: %backupfile%
pause
goto menu

:restore
echo.
echo WARNING: Restoring registry can cause system issues if done incorrectly!
echo.
set /p backuppath="Enter full path to backup file: "
set /p confirm="Are you SURE you want to restore? (YES/NO): "

if /i "%confirm%"=="YES" (
    echo.
    echo Restoring registry...
    reg import "%backuppath%"
    echo.
    echo Registry restored! A system restart is recommended.
) else (
    echo Operation cancelled.
)
pause
goto menu

:viewlocation
echo.
echo Backup Location:
echo %USERPROFILE%\Desktop\RegistryBackups
echo.
if exist "%USERPROFILE%\Desktop\RegistryBackups" (
    explorer "%USERPROFILE%\Desktop\RegistryBackups"
) else (
    echo No backups folder exists yet.
)
pause
goto menu
