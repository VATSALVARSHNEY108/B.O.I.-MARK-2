@echo off
title Turn Bluetooth OFF

echo ================================================
echo    Turning Bluetooth OFF
echo ================================================
echo.

powershell -ExecutionPolicy Bypass -Command "& { try { Add-Type -AssemblyName System.Runtime.WindowsRuntime; $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation``1' })[0]; Function Await($WinRtTask, $ResultType) { $asTask = $asTaskGeneric.MakeGenericMethod($ResultType); $netTask = $asTask.Invoke($null, @($WinRtTask)); $netTask.Wait(-1) | Out-Null; $netTask.Result }; [Windows.Devices.Radios.Radio,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null; [Windows.Devices.Radios.RadioAccessStatus,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null; $radios = Await ([Windows.Devices.Radios.Radio]::GetRadiosAsync()) ([System.Collections.Generic.IReadOnlyList[Windows.Devices.Radios.Radio]]); $bluetooth = $radios | Where-Object { $_.Kind -eq 'Bluetooth' } | Select-Object -First 1; if ($bluetooth) { Await ($bluetooth.SetStateAsync('Off')) ([Windows.Devices.Radios.RadioAccessStatus]); Write-Host 'SUCCESS: Bluetooth turned OFF!' -ForegroundColor Green } else { Write-Host 'ERROR: No Bluetooth radio found!' -ForegroundColor Red } } catch { Write-Host 'ERROR: Failed to disable Bluetooth.' -ForegroundColor Red; Write-Host $_.Exception.Message -ForegroundColor Yellow; Write-Host 'Opening Bluetooth settings...' -ForegroundColor Cyan; Start-Process 'ms-settings:bluetooth' } }"

echo.
pause
