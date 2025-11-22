# Bluetooth Control Troubleshooting Guide

## Quick Test

Run this command in your Windows terminal to test the Bluetooth fix:

```bash
python test_bluetooth_control.py
```

This will show you exactly what's happening when trying to control Bluetooth.

## Common Issues & Solutions

### Issue 1: "No Bluetooth radio found"
**Cause:** Your computer doesn't have Bluetooth hardware, or it's disabled in BIOS/Device Manager

**Solutions:**
1. Check Device Manager → Bluetooth → Make sure Bluetooth adapter is present
2. Check BIOS settings (restart → F2/Del) → Enable Bluetooth
3. If using desktop PC, you may need a Bluetooth USB dongle

### Issue 2: "Access denied" or "RadioAccessStatus != Allowed"
**Cause:** Windows is blocking the PowerShell script from controlling Bluetooth

**Solutions:**
1. **Run as Administrator:** Right-click on your BOI app → "Run as Administrator"
2. **Check Execution Policy:** Open PowerShell as Admin and run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. **Check Windows Settings:** Settings → Privacy → Bluetooth → Make sure apps can access Bluetooth

### Issue 3: "Bluetooth service not running"
**Cause:** The Windows Bluetooth service (bthserv) is disabled or stopped

**Solutions:**
1. Press Win+R, type `services.msc`, press Enter
2. Find "Bluetooth Support Service"
3. Right-click → Properties → Set "Startup type" to "Automatic"
4. Click "Start" if it's stopped
5. Click "OK" and try again

### Issue 4: PowerShell errors or timeouts
**Cause:** PowerShell execution issues or system restrictions

**Solutions:**
1. Open PowerShell as Administrator and run:
   ```powershell
   Get-ExecutionPolicy -List
   ```
2. If it shows "Restricted", run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
   ```
3. Test manually:
   ```powershell
   Add-Type -AssemblyName System.Runtime.WindowsRuntime
   [Windows.Devices.Radios.Radio,Windows.Devices.Radios,ContentType=WindowsRuntime] | Out-Null
   $radios = ([Windows.Devices.Radios.Radio]::GetRadiosAsync() | Get-Awaiter).GetResult()
   $bluetooth = $radios | Where-Object { $_.Kind -eq 'Bluetooth' } | Select-Object -First 1
   if ($bluetooth) { "Bluetooth found: " + $bluetooth.Name } else { "No Bluetooth" }
   ```

## Alternative Methods

If the automatic method still doesn't work, you have these options:

### Option 1: Use the Batch Files (RECOMMENDED)
Navigate to `batch_scripts/quick_access/` and run:
- `bluetooth_off.bat` - Turn Bluetooth OFF
- `bluetooth_on.bat` - Turn Bluetooth ON
- `bluetooth_status.bat` - Check Bluetooth status

These use the exact same PowerShell commands but run independently.

### Option 2: Manual PowerShell Commands
Open PowerShell as Administrator and paste this command to turn Bluetooth OFF:

```powershell
Get-Service bthserv | Start-Service
Start-Sleep -Seconds 1
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Devices.Radios.Radio,Windows.Devices.Radios,ContentType=WindowsRuntime] | Out-Null
[Windows.Devices.Radios.RadioAccessStatus,Windows.Devices.Radios,ContentType=WindowsRuntime] | Out-Null
$radiosAsync = [Windows.Devices.Radios.Radio]::GetRadiosAsync()
$radiosTask = [System.WindowsRuntimeSystemExtensions]::AsTask($radiosAsync)
$radios = $radiosTask.GetAwaiter().GetResult()
$bluetooth = $radios | Where-Object { $_.Kind -eq 'Bluetooth' } | Select-Object -First 1
if ($bluetooth) {
    $setStateAsync = $bluetooth.SetStateAsync('Off')
    $setStateTask = [System.WindowsRuntimeSystemExtensions]::AsTask($setStateAsync)
    $accessStatus = $setStateTask.GetAwaiter().GetResult()
    if ($accessStatus -eq [Windows.Devices.Radios.RadioAccessStatus]::Allowed) {
        Write-Host "SUCCESS: Bluetooth turned OFF" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Access denied - $accessStatus" -ForegroundColor Red
    }
} else {
    Write-Host "ERROR: No Bluetooth radio found" -ForegroundColor Red
}
```

### Option 3: Windows Settings
1. Press Win+I to open Settings
2. Go to Bluetooth & devices
3. Toggle Bluetooth switch manually

## What Changed in the Fix

The original code used `Enable-PnpDevice` / `Disable-PnpDevice` which is unreliable on many systems.

The new code uses **Windows Runtime Radio API** which:
1. ✅ Starts the Bluetooth service first
2. ✅ Uses the official Windows.Devices.Radios API
3. ✅ Properly handles async operations
4. ✅ Checks access permissions explicitly
5. ✅ Returns detailed error messages

This is the same method Windows Settings uses internally.

## Getting Detailed Error Information

If you see "generic error message" in BOI:

1. Run the test script: `python test_bluetooth_control.py`
2. Check the full error output
3. Match the error to the solutions above

## Still Not Working?

If none of these solutions work:

1. **Verify Bluetooth hardware:**
   ```powershell
   Get-PnpDevice | Where-Object {$_.Class -eq 'Bluetooth'}
   ```

2. **Check Windows version:**
   - This requires Windows 10 version 1803 or later
   - Run: `winver` to check your version

3. **Use the batch file workaround:**
   - The batch files in `batch_scripts/quick_access/` work independently
   - Create desktop shortcuts for quick access

4. **Report the issue:**
   - Run `test_bluetooth_control.py` and save the output
   - Note your Windows version and Bluetooth adapter model
   - This helps diagnose the specific issue with your system

## Success Checklist

- [ ] Bluetooth hardware is present and enabled in Device Manager
- [ ] Bluetooth Support Service is running
- [ ] Running BOI as Administrator (or PowerShell execution policy allows scripts)
- [ ] Windows 10 version 1803 or later
- [ ] test_bluetooth_control.py shows SUCCESS

If all checks pass and it still doesn't work, use the batch files as a reliable fallback!
