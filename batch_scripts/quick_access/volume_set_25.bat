@echo off
title Set Volume to 25%%

echo ================================================
echo    Setting Volume to 25%%
echo ================================================
echo.

powershell -Command "Add-Type -TypeDefinition @\" public class Audio { [System.Runtime.InteropServices.DllImport(\"user32.dll\")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, int dwExtraInfo); } \"@; $wshShell = New-Object -ComObject WScript.Shell; try { Add-Type -AssemblyName System.Windows.Forms; $vol = [Math]::Round([System.Windows.Forms.SendKeys]::SendWait('^')); } catch { } $volume = 0.25; $obj = New-Object -ComObject WScript.Shell; for ($i=0; $i -lt 50; $i++) { $obj.SendKeys([char]174) }; Start-Sleep -Milliseconds 100; $steps = [Math]::Round(50 * $volume); for ($i=0; $i -lt $steps; $i++) { $obj.SendKeys([char]175) }; Write-Host 'Volume set to approximately 25%%' -ForegroundColor Green"

echo.
timeout /t 2 /nobreak >nul
