@echo off
setlocal EnableDelayedExpansion

:: ================================================
:: Windows 11 Privacy & Security Settings
:: ================================================

:menu
cls
echo ================================================
echo  Windows 11 Privacy ^& Security Settings
echo ================================================
echo.
echo [1] Camera Privacy
echo [2] Microphone Privacy
echo [3] Location Privacy
echo [4] Windows Defender
echo [5] Firewall Settings
echo [6] App Permissions
echo [7] Telemetry Settings
echo [8] User Account Control
echo [9] Back to Main Menu
echo.
set /p choice="Select option (1-9): "

if "%choice%"=="1" goto camera_privacy
if "%choice%"=="2" goto microphone_privacy
if "%choice%"=="3" goto location_privacy
if "%choice%"=="4" goto defender
if "%choice%"=="5" goto firewall
if "%choice%"=="6" goto app_permissions
if "%choice%"=="7" goto telemetry
if "%choice%"=="8" goto uac
if "%choice%"=="9" exit /b
goto menu

:camera_privacy
cls
echo ================================================
echo Camera Privacy Settings
echo ================================================
echo.
echo [1] Enable Camera Access
echo [2] Disable Camera Access
echo [3] Open Camera Settings
echo.
set /p cam_choice="Select option (1-3): "

if "%cam_choice%"=="1" (
    reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam" /v "Value" /t REG_SZ /d "Allow" /f
    echo Camera access enabled!
) else if "%cam_choice%"=="2" (
    reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam" /v "Value" /t REG_SZ /d "Deny" /f
    echo Camera access disabled!
) else if "%cam_choice%"=="3" (
    start ms-settings:privacy-webcam
)
pause
goto menu

:microphone_privacy
cls
echo ================================================
echo Microphone Privacy Settings
echo ================================================
echo.
echo [1] Enable Microphone Access
echo [2] Disable Microphone Access
echo [3] Open Microphone Settings
echo.
set /p mic_choice="Select option (1-3): "

if "%mic_choice%"=="1" (
    reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone" /v "Value" /t REG_SZ /d "Allow" /f
    echo Microphone access enabled!
) else if "%mic_choice%"=="2" (
    reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone" /v "Value" /t REG_SZ /d "Deny" /f
    echo Microphone access disabled!
) else if "%mic_choice%"=="3" (
    start ms-settings:privacy-microphone
)
pause
goto menu

:location_privacy
cls
echo ================================================
echo Location Privacy Settings
echo ================================================
echo.
echo [1] Enable Location Services
echo [2] Disable Location Services
echo [3] Open Location Settings
echo.
set /p loc_choice="Select option (1-3): "

if "%loc_choice%"=="1" (
    reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location" /v "Value" /t REG_SZ /d "Allow" /f
    echo Location services enabled!
) else if "%loc_choice%"=="2" (
    reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location" /v "Value" /t REG_SZ /d "Deny" /f
    echo Location services disabled!
) else if "%loc_choice%"=="3" (
    start ms-settings:privacy-location
)
pause
goto menu

:defender
cls
echo ================================================
echo Windows Defender Settings
echo ================================================
echo.
echo [1] Quick Scan
echo [2] Full Scan
echo [3] Custom Scan
echo [4] Update Definitions
echo [5] Enable Real-Time Protection
echo [6] Disable Real-Time Protection
echo [7] View Protection Status
echo [8] View Threat History
echo [9] Open Defender Settings
echo.
set /p def_choice="Select option (1-9): "

if "%def_choice%"=="1" (
    echo.
    echo Starting Windows Defender Quick Scan...
    echo This may take a few minutes...
    powershell -ExecutionPolicy Bypass -Command "Start-MpScan -ScanType QuickScan; if ($?) { Write-Host 'Quick scan completed successfully!' -ForegroundColor Green } else { Write-Host 'Scan failed or was interrupted.' -ForegroundColor Red }"
) else if "%def_choice%"=="2" (
    echo.
    echo Starting Windows Defender Full Scan...
    echo WARNING: This may take 30+ minutes depending on your system.
    set /p confirm="Continue? (Y/N): "
    if /i "!confirm!"=="Y" (
        powershell -ExecutionPolicy Bypass -Command "Start-MpScan -ScanType FullScan; if ($?) { Write-Host 'Full scan completed successfully!' -ForegroundColor Green } else { Write-Host 'Scan failed or was interrupted.' -ForegroundColor Red }"
    )
) else if "%def_choice%"=="3" (
    set /p scan_path="Enter path to scan: "
    echo.
    echo Scanning !scan_path!...
    powershell -ExecutionPolicy Bypass -Command "Start-MpScan -ScanType CustomScan -ScanPath '!scan_path!'; if ($?) { Write-Host 'Custom scan completed!' -ForegroundColor Green } else { Write-Host 'Scan failed.' -ForegroundColor Red }"
) else if "%def_choice%"=="4" (
    echo.
    echo Updating Windows Defender virus definitions...
    powershell -ExecutionPolicy Bypass -Command "Update-MpSignature; if ($?) { Write-Host 'Virus definitions updated successfully!' -ForegroundColor Green; Get-MpComputerStatus | Select-Object AntivirusSignatureLastUpdated, AntispywareSignatureLastUpdated | Format-List } else { Write-Host 'Update failed.' -ForegroundColor Red }"
) else if "%def_choice%"=="5" (
    echo.
    echo Enabling Real-Time Protection...
    powershell -ExecutionPolicy Bypass -Command "Set-MpPreference -DisableRealtimeMonitoring $false; if ($?) { Write-Host 'Real-Time Protection enabled!' -ForegroundColor Green } else { Write-Host 'Failed to enable. Run as Administrator.' -ForegroundColor Red }"
) else if "%def_choice%"=="6" (
    echo.
    echo WARNING: Disabling Real-Time Protection leaves your system vulnerable!
    set /p confirm="Are you sure? (Y/N): "
    if /i "!confirm!"=="Y" (
        powershell -ExecutionPolicy Bypass -Command "Set-MpPreference -DisableRealtimeMonitoring $true; if ($?) { Write-Host 'Real-Time Protection disabled.' -ForegroundColor Yellow } else { Write-Host 'Failed. Run as Administrator.' -ForegroundColor Red }"
    )
) else if "%def_choice%"=="7" (
    echo.
    echo Windows Defender Protection Status:
    echo ====================================
    powershell -Command "Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, IoavProtectionEnabled, OnAccessProtectionEnabled, BehaviorMonitorEnabled, AntivirusSignatureLastUpdated | Format-List"
) else if "%def_choice%"=="8" (
    echo.
    echo Recent Threat Detections:
    echo =========================
    powershell -Command "Get-MpThreatDetection | Select-Object -First 10 | Format-Table ThreatID, InitialDetectionTime, Resources -AutoSize"
) else if "%def_choice%"=="9" (
    start windowsdefender:
)
pause
goto menu

:firewall
cls
echo ================================================
echo Windows Firewall Settings
echo ================================================
echo.
echo [1] Enable Firewall (All Profiles)
echo [2] Disable Firewall (All Profiles)
echo [3] View Firewall Status
echo [4] Open Firewall Settings
echo.
set /p fw_choice="Select option (1-4): "

if "%fw_choice%"=="1" (
    netsh advfirewall set allprofiles state on
    echo Firewall enabled for all profiles!
) else if "%fw_choice%"=="2" (
    netsh advfirewall set allprofiles state off
    echo Firewall disabled for all profiles!
) else if "%fw_choice%"=="3" (
    netsh advfirewall show allprofiles
) else if "%fw_choice%"=="4" (
    firewall.cpl
)
pause
goto menu

:app_permissions
cls
echo ================================================
echo App Permissions
echo ================================================
echo.
echo Opening Privacy Settings...
start ms-settings:privacy
pause
goto menu

:telemetry
cls
echo ================================================
echo Telemetry Settings
echo ================================================
echo.
echo [1] Set Telemetry to Security (Minimal)
echo [2] Set Telemetry to Basic
echo [3] Set Telemetry to Enhanced
echo [4] Set Telemetry to Full
echo.
set /p tel_choice="Select option (1-4): "

if "%tel_choice%"=="1" (
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f
    echo Telemetry set to Security!
) else if "%tel_choice%"=="2" (
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 1 /f
    echo Telemetry set to Basic!
) else if "%tel_choice%"=="3" (
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 2 /f
    echo Telemetry set to Enhanced!
) else if "%tel_choice%"=="4" (
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 3 /f
    echo Telemetry set to Full!
)
pause
goto menu

:uac
cls
echo ================================================
echo User Account Control (UAC)
echo ================================================
echo.
echo [1] Enable UAC (Recommended)
echo [2] Disable UAC
echo [3] Open UAC Settings
echo.
set /p uac_choice="Select option (1-3): "

if "%uac_choice%"=="1" (
    reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 1 /f
    echo UAC enabled!
) else if "%uac_choice%"=="2" (
    reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 0 /f
    echo UAC disabled! (Restart required)
) else if "%uac_choice%"=="3" (
    UserAccountControlSettings.exe
)
pause
goto menu
