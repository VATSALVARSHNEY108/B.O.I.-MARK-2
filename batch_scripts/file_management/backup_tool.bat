@echo off
REM ==========================================
REM Backup Tool
REM Backup important folders
REM ==========================================

title Backup Tool

echo ========================================
echo          BACKUP TOOL
echo ========================================
echo.

set backup_date=%date:~-4,4%%date:~-10,2%%date:~-7,2%
set backup_time=%time:~0,2%%time:~3,2%
set backup_time=%backup_time: =0%

set backup_folder=D:\Backups\Backup_%backup_date%_%backup_time%

echo Creating backup folder: %backup_folder%
mkdir "%backup_folder%" 2>nul

echo.
echo Select what to backup:
echo.
echo 1. Documents
echo 2. Pictures
echo 3. Videos
echo 4. Music
echo 5. Desktop
echo 6. All of the above
echo 7. Custom folder
echo 8. Cancel
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto documents
if "%choice%"=="2" goto pictures
if "%choice%"=="3" goto videos
if "%choice%"=="4" goto music
if "%choice%"=="5" goto desktop
if "%choice%"=="6" goto all
if "%choice%"=="7" goto custom
if "%choice%"=="8" exit

:documents
echo Backing up Documents...
xcopy "%USERPROFILE%\Documents" "%backup_folder%\Documents" /E /I /H /Y
goto done

:pictures
echo Backing up Pictures...
xcopy "%USERPROFILE%\Pictures" "%backup_folder%\Pictures" /E /I /H /Y
goto done

:videos
echo Backing up Videos...
xcopy "%USERPROFILE%\Videos" "%backup_folder%\Videos" /E /I /H /Y
goto done

:music
echo Backing up Music...
xcopy "%USERPROFILE%\Music" "%backup_folder%\Music" /E /I /H /Y
goto done

:desktop
echo Backing up Desktop...
xcopy "%USERPROFILE%\Desktop" "%backup_folder%\Desktop" /E /I /H /Y
goto done

:all
echo Backing up all folders...
echo [1/5] Documents...
xcopy "%USERPROFILE%\Documents" "%backup_folder%\Documents" /E /I /H /Y >nul
echo [2/5] Pictures...
xcopy "%USERPROFILE%\Pictures" "%backup_folder%\Pictures" /E /I /H /Y >nul
echo [3/5] Videos...
xcopy "%USERPROFILE%\Videos" "%backup_folder%\Videos" /E /I /H /Y >nul
echo [4/5] Music...
xcopy "%USERPROFILE%\Music" "%backup_folder%\Music" /E /I /H /Y >nul
echo [5/5] Desktop...
xcopy "%USERPROFILE%\Desktop" "%backup_folder%\Desktop" /E /I /H /Y >nul
goto done

:custom
set /p custom_path="Enter folder path to backup: "
echo Backing up %custom_path%...
for %%F in ("%custom_path%") do set folder_name=%%~nxF
xcopy "%custom_path%" "%backup_folder%\%folder_name%" /E /I /H /Y
goto done

:done
echo.
echo ========================================
echo Backup complete!
echo Location: %backup_folder%
echo ========================================
start explorer "%backup_folder%"
pause
