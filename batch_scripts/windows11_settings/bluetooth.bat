@echo off
setlocal EnableDelayedExpansion

:: ================================================
:: Windows 11 Bluetooth Settings Automation
:: ================================================

:menu
cls
echo ================================================
echo    Windows 11 Bluetooth Controller
echo ================================================
echo.
echo [1] Turn Bluetooth ON
echo [2] Turn Bluetooth OFF
echo [3] List Paired Devices
echo [4] Add Bluetooth Device
echo [5] Remove Bluetooth Device
echo [6] Bluetooth Settings
echo [7] Back to Main Menu
echo.
set /p choice="Select option (1-7): "

if "%choice%"=="1" goto bluetooth_on
if "%choice%"=="2" goto bluetooth_off
if "%choice%"=="3" goto list_devices
if "%choice%"=="4" goto add_device
if "%choice%"=="5" goto remove_device
if "%choice%"=="6" goto bt_settings
if "%choice%"=="7" exit /b
goto menu

:bluetooth_on
cls
echo ================================================
echo Turn Bluetooth ON
echo ================================================
echo.
echo Turning Bluetooth ON...
powershell -ExecutionPolicy Bypass -Command "& { try { Get-Service bthserv | Start-Service -ErrorAction Stop; Start-Sleep -Seconds 1; Add-Type -AssemblyName System.Runtime.WindowsRuntime; $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation``1' })[0]; Function Await($WinRtTask, $ResultType) { $asTask = $asTaskGeneric.MakeGenericMethod($ResultType); $netTask = $asTask.Invoke($null, @($WinRtTask)); $netTask.Wait(-1) | Out-Null; $netTask.Result }; [Windows.Devices.Radios.Radio,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null; [Windows.Devices.Radios.RadioAccessStatus,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null; $radios = Await ([Windows.Devices.Radios.Radio]::GetRadiosAsync()) ([System.Collections.Generic.IReadOnlyList[Windows.Devices.Radios.Radio]]); $bluetooth = $radios | Where-Object { $_.Kind -eq 'Bluetooth' } | Select-Object -First 1; if ($bluetooth) { Await ($bluetooth.SetStateAsync('On')) ([Windows.Devices.Radios.RadioAccessStatus]); Write-Host 'Bluetooth turned ON successfully!' -ForegroundColor Green } else { Write-Host 'No Bluetooth radio found!' -ForegroundColor Red } } catch { Write-Host 'Failed to enable Bluetooth. Opening Bluetooth settings...' -ForegroundColor Red; Start-Process 'ms-settings:bluetooth' } }"
pause
goto menu

:bluetooth_off
cls
echo ================================================
echo Turn Bluetooth OFF
echo ================================================
echo.
echo Turning Bluetooth OFF...
powershell -ExecutionPolicy Bypass -Command "& { try { Add-Type -AssemblyName System.Runtime.WindowsRuntime; $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation``1' })[0]; Function Await($WinRtTask, $ResultType) { $asTask = $asTaskGeneric.MakeGenericMethod($ResultType); $netTask = $asTask.Invoke($null, @($WinRtTask)); $netTask.Wait(-1) | Out-Null; $netTask.Result }; [Windows.Devices.Radios.Radio,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null; [Windows.Devices.Radios.RadioAccessStatus,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null; $radios = Await ([Windows.Devices.Radios.Radio]::GetRadiosAsync()) ([System.Collections.Generic.IReadOnlyList[Windows.Devices.Radios.Radio]]); $bluetooth = $radios | Where-Object { $_.Kind -eq 'Bluetooth' } | Select-Object -First 1; if ($bluetooth) { Await ($bluetooth.SetStateAsync('Off')) ([Windows.Devices.Radios.RadioAccessStatus]); Write-Host 'Bluetooth turned OFF successfully!' -ForegroundColor Green } else { Write-Host 'No Bluetooth radio found!' -ForegroundColor Red } } catch { Write-Host 'Failed to disable Bluetooth. Opening Bluetooth settings...' -ForegroundColor Red; Start-Process 'ms-settings:bluetooth' } }"
pause
goto menu

:list_devices
cls
echo ================================================
echo List Paired Bluetooth Devices
echo ================================================
echo.
echo Listing paired devices...
powershell -Command "Get-PnpDevice | Where-Object {$_.Class -eq 'Bluetooth'} | Select-Object FriendlyName, Status | Format-Table -AutoSize"
echo.
pause
goto menu

:add_device
cls
echo ================================================
echo Add Bluetooth Device
echo ================================================
echo.
echo Opening Bluetooth settings to add a device...
start ms-settings:bluetooth
echo.
echo Please pair your device using the settings window.
pause
goto menu

:remove_device
cls
echo ================================================
echo Remove Bluetooth Device
echo ================================================
echo.
echo Opening Bluetooth settings to remove a device...
start ms-settings:bluetooth
echo.
echo Please remove your device using the settings window.
pause
goto menu

:bt_settings
cls
echo ================================================
echo Bluetooth Settings
echo ================================================
echo.
echo Opening Bluetooth settings...
start ms-settings:bluetooth
pause
goto menu
