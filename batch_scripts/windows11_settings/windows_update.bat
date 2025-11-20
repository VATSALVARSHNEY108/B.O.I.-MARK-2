@echo off
setlocal EnableDelayedExpansion

:: ================================================
:: Windows 11 Update Settings Automation
:: ================================================

:menu
cls
echo ================================================
echo    Windows 11 Update Controller
echo ================================================
echo.
echo [1] Check for Updates
echo [2] Install All Updates
echo [3] Pause Updates (7 days)
echo [4] Resume Updates
echo [5] View Update History
echo [6] Advanced Update Options
echo [7] Windows Update Settings
echo [8] Back to Main Menu
echo.
set /p choice="Select option (1-8): "

if "%choice%"=="1" goto check_updates
if "%choice%"=="2" goto install_updates
if "%choice%"=="3" goto pause_updates
if "%choice%"=="4" goto resume_updates
if "%choice%"=="5" goto update_history
if "%choice%"=="6" goto advanced_options
if "%choice%"=="7" goto update_settings
if "%choice%"=="8" exit /b
goto menu

:check_updates
cls
echo ================================================
echo Check for Windows Updates
echo ================================================
echo.
echo Checking for available Windows Updates...
echo This may take a few moments...
echo.
powershell -ExecutionPolicy Bypass -Command "& { $updateSession = New-Object -ComObject Microsoft.Update.Session; $updateSearcher = $updateSession.CreateUpdateSearcher(); Write-Host 'Searching for updates...' -ForegroundColor Yellow; try { $searchResult = $updateSearcher.Search('IsInstalled=0'); if ($searchResult.Updates.Count -eq 0) { Write-Host 'Your system is up to date!' -ForegroundColor Green } else { Write-Host ('Found ' + $searchResult.Updates.Count + ' updates available:') -ForegroundColor Cyan; $searchResult.Updates | ForEach-Object { Write-Host ('  - ' + $_.Title) }; Write-Host ''; Write-Host 'Use option [2] to install these updates' -ForegroundColor Yellow } } catch { Write-Host 'Failed to check for updates. Opening Windows Update settings...' -ForegroundColor Red; Start-Process 'ms-settings:windowsupdate-action' } }"
echo.
pause
goto menu

:install_updates
cls
echo ================================================
echo Install All Updates
echo ================================================
echo.
echo Installing all available updates...
powershell -Command "Install-WindowsUpdate -AcceptAll -AutoReboot | Out-File 'C:\Windows\Temp\update_log.txt'"
echo.
echo Update installation started. Check update_log.txt for details.
pause
goto menu

:pause_updates
cls
echo ================================================
echo Pause Windows Updates
echo ================================================
echo.
echo [1] Pause for 1 week
echo [2] Pause for 2 weeks
echo [3] Pause for 3 weeks
echo [4] Pause for 4 weeks
echo [5] Pause for 5 weeks
echo.
set /p pause_choice="Select duration (1-5): "

if "%pause_choice%"=="1" set days=7
if "%pause_choice%"=="2" set days=14
if "%pause_choice%"=="3" set days=21
if "%pause_choice%"=="4" set days=28
if "%pause_choice%"=="5" set days=35

echo.
echo Pausing updates for !days! days...
reg add "HKLM\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" /v PauseUpdatesExpiryTime /t REG_SZ /d "2025-12-31T00:00:00Z" /f
echo Updates paused!
pause
goto menu

:resume_updates
cls
echo ================================================
echo Resume Windows Updates
echo ================================================
echo.
echo Resuming Windows Updates...
reg delete "HKLM\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" /v PauseUpdatesExpiryTime /f
echo Updates resumed!
pause
goto menu

:update_history
cls
echo ================================================
echo Windows Update History
echo ================================================
echo.
powershell -Command "Get-HotFix | Select-Object Description, HotFixID, InstalledOn | Format-Table -AutoSize"
echo.
pause
goto menu

:advanced_options
cls
echo ================================================
echo Advanced Update Options
echo ================================================
echo.
echo [1] Enable Automatic Updates
echo [2] Disable Automatic Updates
echo [3] Download Only (No Auto Install)
echo [4] Notify Before Download
echo.
set /p adv_choice="Select option (1-4): "

if "%adv_choice%"=="1" (
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v NoAutoUpdate /t REG_DWORD /d 0 /f
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v AUOptions /t REG_DWORD /d 4 /f
    echo Automatic updates enabled!
) else if "%adv_choice%"=="2" (
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v NoAutoUpdate /t REG_DWORD /d 1 /f
    echo Automatic updates disabled!
) else if "%adv_choice%"=="3" (
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v AUOptions /t REG_DWORD /d 3 /f
    echo Download only mode enabled!
) else if "%adv_choice%"=="4" (
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v AUOptions /t REG_DWORD /d 2 /f
    echo Notify before download enabled!
)
pause
goto menu

:update_settings
cls
echo ================================================
echo Windows Update Settings
echo ================================================
echo.
echo Opening Windows Update settings...
start ms-settings:windowsupdate
pause
goto menu
