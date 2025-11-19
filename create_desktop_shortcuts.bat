@echo off
REM Create Desktop Shortcuts for AI Phone Link Controller
REM This creates convenient shortcuts on your Windows desktop

title Create Desktop Shortcuts
color 0B

echo.
echo ========================================
echo  CREATE DESKTOP SHORTCUTS
echo ========================================
echo.
echo This will create shortcuts on your desktop for:
echo   1. AI Phone Controller (Interactive)
echo   2. Quick Dial
echo.
pause

REM Get current directory
set "CURRENT_DIR=%~dp0"

REM Get desktop path
set "DESKTOP=%USERPROFILE%\Desktop"

echo.
echo Creating shortcuts...
echo.

REM Create shortcut for AI Phone Controller
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESKTOP%\AI Phone Controller.lnk'); $s.TargetPath = '%CURRENT_DIR%launchers\ai_phone_controller.bat'; $s.WorkingDirectory = '%CURRENT_DIR%'; $s.IconLocation = 'shell32.dll,21'; $s.Description = 'AI-powered Phone Link controller'; $s.Save()"

echo [1/2] AI Phone Controller shortcut created!

REM Create shortcut for Quick Dial
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESKTOP%\Quick Dial.lnk'); $s.TargetPath = '%CURRENT_DIR%launchers\quick_dial.bat'; $s.WorkingDirectory = '%CURRENT_DIR%'; $s.IconLocation = 'shell32.dll,23'; $s.Description = 'Quick dial your favorite number'; $s.Save()"

echo [2/2] Quick Dial shortcut created!

echo.
echo ========================================
echo  SUCCESS!
echo ========================================
echo.
echo Check your desktop for:
echo   - AI Phone Controller.lnk
echo   - Quick Dial.lnk
echo.
echo Remember to edit Quick Dial.bat to set
echo your phone number before using it.
echo.
pause
