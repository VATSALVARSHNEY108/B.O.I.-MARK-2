@echo off
setlocal EnableDelayedExpansion

:: ================================================
:: Windows 11 Sound Settings Automation
:: ================================================

:menu
cls
echo ================================================
echo    Windows 11 Sound Settings Controller
echo ================================================
echo.
echo [1] Set System Volume
echo [2] Mute/Unmute System
echo [3] List Audio Devices
echo [4] Set Default Playback Device
echo [5] Set Default Recording Device
echo [6] Enable/Disable Spatial Sound
echo [7] Sound Control Panel
echo [8] Back to Main Menu
echo.
set /p choice="Select option (1-8): "

if "%choice%"=="1" goto set_volume
if "%choice%"=="2" goto toggle_mute
if "%choice%"=="3" goto list_devices
if "%choice%"=="4" goto set_playback
if "%choice%"=="5" goto set_recording
if "%choice%"=="6" goto spatial_sound
if "%choice%"=="7" goto sound_panel
if "%choice%"=="8" exit /b
goto menu

:set_volume
cls
echo ================================================
echo Set System Volume
echo ================================================
echo.
set /p volume="Enter volume level (0-100): "

if !volume! LSS 0 set volume=0
if !volume! GTR 100 set volume=100

echo.
echo Setting volume to !volume!%%...
powershell -ExecutionPolicy Bypass -Command "& { $obj = New-Object -ComObject WScript.Shell; Add-Type -TypeDefinition @' using System.Runtime.InteropServices; [Guid(\"5CDF2C82-841E-4546-9722-0CF74078229A\"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)] interface IAudioEndpointVolume { int NotImpl1(); int NotImpl2(); int GetChannelCount(out int channelCount); int SetMasterVolumeLevelScalar(float level, ref Guid eventContext); int GetMasterVolumeLevelScalar(out float level); } '@; try { $deviceEnumerator = [System.Activator]::CreateInstance([Type]::GetTypeFromCLSID([Guid]'BCDE0395-E52F-467C-8E3D-C4579291692E')); $defaultDevice = [System.Runtime.InteropServices.Marshal]::GetObjectForIUnknown($deviceEnumerator.GetDefaultAudioEndpoint(0, 1)); $audioEndpointVolume = $defaultDevice.Activate([Guid]'5CDF2C82-841E-4546-9722-0CF74078229A', 0, [IntPtr]::Zero); $audioEndpointVolume.SetMasterVolumeLevelScalar([float](%volume%/100), [Guid]::Empty); Write-Host 'Volume set to %volume%%' -ForegroundColor Green } catch { Write-Host 'Using fallback method...' -ForegroundColor Yellow; $obj.SendKeys([char]174); Start-Sleep -Milliseconds 50; 1..50 | ForEach-Object { $obj.SendKeys([char]174) }; 1..(%volume%/2) | ForEach-Object { $obj.SendKeys([char]175) }; Write-Host 'Volume set to approximately %volume%%' -ForegroundColor Green } }"
pause
goto menu

:toggle_mute
cls
echo ================================================
echo Toggle Mute
echo ================================================
echo.
echo Toggling system mute...
powershell -Command "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"
echo Done!
pause
goto menu

:list_devices
cls
echo ================================================
echo Audio Devices List
echo ================================================
echo.
echo Playback Devices:
echo ----------------
powershell -Command "Get-CimInstance Win32_SoundDevice | Select-Object Name, Status, DeviceID | Format-Table -AutoSize"
echo.
pause
goto menu

:set_playback
cls
echo ================================================
echo Set Default Playback Device
echo ================================================
echo.
echo Opening Sound Settings...
start ms-settings:sound
echo.
echo Please manually select your default playback device
pause
goto menu

:set_recording
cls
echo ================================================
echo Set Default Recording Device
echo ================================================
echo.
echo Opening Sound Settings...
start ms-settings:sound
echo.
echo Please manually select your default recording device
pause
goto menu

:spatial_sound
cls
echo ================================================
echo Spatial Sound Settings
echo ================================================
echo.
echo [1] Enable Windows Sonic for Headphones
echo [2] Enable Dolby Atmos for Headphones
echo [3] Disable Spatial Sound
echo.
set /p spatial_choice="Select option (1-3): "

echo.
echo Opening Sound Settings...
start ms-settings:sound
echo.
echo Please manually configure spatial sound in the advanced settings
pause
goto menu

:sound_panel
cls
echo ================================================
echo Sound Control Panel
echo ================================================
echo.
echo Opening classic Sound Control Panel...
control mmsys.cpl sounds
pause
goto menu
