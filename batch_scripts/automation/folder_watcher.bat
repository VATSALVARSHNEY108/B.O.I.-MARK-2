@echo off
REM ==========================================
REM FOLDER WATCHER
REM Monitor folder for changes
REM ==========================================

color 0F
title Folder Watcher

:menu
cls
echo ========================================
echo       FOLDER WATCHER
echo ========================================
echo.
echo 1. Watch Downloads Folder
echo 2. Watch Desktop
echo 3. Watch Custom Folder
echo 4. Auto-Organize Downloads
echo 5. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto watchdownloads
if "%choice%"=="2" goto watchdesktop
if "%choice%"=="3" goto watchcustom
if "%choice%"=="4" goto autoorganize
if "%choice%"=="5" exit /b

goto menu

:watchdownloads
echo.
echo Watching Downloads folder...
echo Press Ctrl+C to stop
powershell -Command "& {$watcher = New-Object System.IO.FileSystemWatcher; $watcher.Path = '%USERPROFILE%\Downloads'; $watcher.EnableRaisingEvents = $true; while($true){$result = $watcher.WaitForChanged([System.IO.WatcherChangeTypes]::All, 5000); if($result.TimedOut -eq $false){Write-Host 'Change detected: ' $result.ChangeType ' - ' $result.Name}}}"
pause
goto menu

:watchdesktop
echo.
echo Watching Desktop folder...
echo Press Ctrl+C to stop
powershell -Command "& {$watcher = New-Object System.IO.FileSystemWatcher; $watcher.Path = '%USERPROFILE%\Desktop'; $watcher.EnableRaisingEvents = $true; while($true){$result = $watcher.WaitForChanged([System.IO.WatcherChangeTypes]::All, 5000); if($result.TimedOut -eq $false){Write-Host 'Change detected: ' $result.ChangeType ' - ' $result.Name}}}"
pause
goto menu

:watchcustom
set /p folderpath="Enter folder path to watch: "
echo.
echo Watching %folderpath%...
echo Press Ctrl+C to stop
powershell -Command "& {$watcher = New-Object System.IO.FileSystemWatcher; $watcher.Path = '%folderpath%'; $watcher.EnableRaisingEvents = $true; while($true){$result = $watcher.WaitForChanged([System.IO.WatcherChangeTypes]::All, 5000); if($result.TimedOut -eq $false){Write-Host 'Change detected: ' $result.ChangeType ' - ' $result.Name}}}"
pause
goto menu

:autoorganize
echo.
echo Auto-organizing Downloads folder...
echo Creating folders...
if not exist "%USERPROFILE%\Downloads\Documents" mkdir "%USERPROFILE%\Downloads\Documents"
if not exist "%USERPROFILE%\Downloads\Images" mkdir "%USERPROFILE%\Downloads\Images"
if not exist "%USERPROFILE%\Downloads\Videos" mkdir "%USERPROFILE%\Downloads\Videos"
if not exist "%USERPROFILE%\Downloads\Music" mkdir "%USERPROFILE%\Downloads\Music"
if not exist "%USERPROFILE%\Downloads\Archives" mkdir "%USERPROFILE%\Downloads\Archives"
if not exist "%USERPROFILE%\Downloads\Programs" mkdir "%USERPROFILE%\Downloads\Programs"

echo Organizing files...
move "%USERPROFILE%\Downloads\*.pdf" "%USERPROFILE%\Downloads\Documents" 2>nul
move "%USERPROFILE%\Downloads\*.docx" "%USERPROFILE%\Downloads\Documents" 2>nul
move "%USERPROFILE%\Downloads\*.txt" "%USERPROFILE%\Downloads\Documents" 2>nul
move "%USERPROFILE%\Downloads\*.jpg" "%USERPROFILE%\Downloads\Images" 2>nul
move "%USERPROFILE%\Downloads\*.png" "%USERPROFILE%\Downloads\Images" 2>nul
move "%USERPROFILE%\Downloads\*.gif" "%USERPROFILE%\Downloads\Images" 2>nul
move "%USERPROFILE%\Downloads\*.mp4" "%USERPROFILE%\Downloads\Videos" 2>nul
move "%USERPROFILE%\Downloads\*.avi" "%USERPROFILE%\Downloads\Videos" 2>nul
move "%USERPROFILE%\Downloads\*.mp3" "%USERPROFILE%\Downloads\Music" 2>nul
move "%USERPROFILE%\Downloads\*.zip" "%USERPROFILE%\Downloads\Archives" 2>nul
move "%USERPROFILE%\Downloads\*.rar" "%USERPROFILE%\Downloads\Archives" 2>nul
move "%USERPROFILE%\Downloads\*.exe" "%USERPROFILE%\Downloads\Programs" 2>nul
move "%USERPROFILE%\Downloads\*.msi" "%USERPROFILE%\Downloads\Programs" 2>nul

echo.
echo Downloads folder organized!
pause
goto menu
