@echo off
setlocal EnableDelayedExpansion

:: ================================================
:: Windows 11 Display Settings Automation
:: ================================================

:menu
cls
echo ================================================
echo    Windows 11 Display Settings Controller
echo ================================================
echo.
echo [1] Set Resolution
echo [2] Set Display Orientation
echo [3] Set Refresh Rate
echo [4] Set Display Scaling
echo [5] Toggle Night Light
echo [6] Get Display Info
echo [7] Set Multiple Monitors
echo [8] Back to Main Menu
echo.
set /p choice="Select option (1-8): "

if "%choice%"=="1" goto set_resolution
if "%choice%"=="2" goto set_orientation
if "%choice%"=="3" goto set_refresh_rate
if "%choice%"=="4" goto set_scaling
if "%choice%"=="5" goto toggle_night_light
if "%choice%"=="6" goto display_info
if "%choice%"=="7" goto multiple_monitors
if "%choice%"=="8" exit /b
goto menu

:set_resolution
cls
echo ================================================
echo Set Display Resolution
echo ================================================
echo.
echo Common Resolutions:
echo [1] 1920x1080 (Full HD)
echo [2] 2560x1440 (2K)
echo [3] 3840x2160 (4K)
echo [4] 1366x768
echo [5] 1600x900
echo [6] Custom
echo.
set /p res_choice="Select resolution (1-6): "

if "%res_choice%"=="1" (
    set width=1920
    set height=1080
) else if "%res_choice%"=="2" (
    set width=2560
    set height=1440
) else if "%res_choice%"=="3" (
    set width=3840
    set height=2160
) else if "%res_choice%"=="4" (
    set width=1366
    set height=768
) else if "%res_choice%"=="5" (
    set width=1600
    set height=900
) else if "%res_choice%"=="6" (
    set /p width="Enter width: "
    set /p height="Enter height: "
)

echo.
echo Setting resolution to !width!x!height!...
powershell -ExecutionPolicy Bypass -Command "& { Add-Type -TypeDefinition @' using System; using System.Runtime.InteropServices; public class Display { [DllImport(\"user32.dll\")] public static extern int EnumDisplaySettings(string lpszDeviceName, int iModeNum, ref DEVMODE lpDevMode); [DllImport(\"user32.dll\")] public static extern int ChangeDisplaySettingsEx(string lpszDeviceName, ref DEVMODE lpDevMode, IntPtr hwnd, int dwflags, IntPtr lParam); [StructLayout(LayoutKind.Sequential)] public struct DEVMODE { [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)] public string dmDeviceName; public short dmSpecVersion; public short dmDriverVersion; public short dmSize; public short dmDriverExtra; public int dmFields; public int dmPositionX; public int dmPositionY; public int dmDisplayOrientation; public int dmDisplayFixedOutput; public short dmColor; public short dmDuplex; public short dmYResolution; public short dmTTOption; public short dmCollate; [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)] public string dmFormName; public short dmLogPixels; public int dmBitsPerPel; public int dmPelsWidth; public int dmPelsHeight; public int dmDisplayFlags; public int dmDisplayFrequency; } } '@; $devMode = New-Object Display+DEVMODE; $devMode.dmSize = [System.Runtime.InteropServices.Marshal]::SizeOf($devMode); [Display]::EnumDisplaySettings($null, -1, [ref]$devMode) | Out-Null; $devMode.dmPelsWidth = %width%; $devMode.dmPelsHeight = %height%; $devMode.dmFields = 0x180000; $result = [Display]::ChangeDisplaySettingsEx($null, [ref]$devMode, [IntPtr]::Zero, 0, [IntPtr]::Zero); if ($result -eq 0) { Write-Host 'Resolution changed successfully to %width%x%height%!' -ForegroundColor Green } else { Write-Host 'Failed to change resolution. Error code:' $result -ForegroundColor Red } }"

pause
goto menu

:set_orientation
cls
echo ================================================
echo Set Display Orientation
echo ================================================
echo.
echo [1] Landscape (0°)
echo [2] Portrait (90°)
echo [3] Landscape Flipped (180°)
echo [4] Portrait Flipped (270°)
echo.
set /p orient_choice="Select orientation (1-4): "

if "%orient_choice%"=="1" set orientation=0
if "%orient_choice%"=="2" set orientation=1
if "%orient_choice%"=="3" set orientation=2
if "%orient_choice%"=="4" set orientation=3

echo.
echo Rotating display to orientation %orientation%...
echo Opening display settings for manual adjustment...
start ms-settings:display
pause
goto menu

:set_refresh_rate
cls
echo ================================================
echo Set Refresh Rate
echo ================================================
echo.
echo Common Refresh Rates:
echo [1] 60 Hz
echo [2] 75 Hz
echo [3] 120 Hz
echo [4] 144 Hz
echo [5] 165 Hz
echo [6] 240 Hz
echo.
set /p hz_choice="Select refresh rate (1-6): "

if "%hz_choice%"=="1" set hz=60
if "%hz_choice%"=="2" set hz=75
if "%hz_choice%"=="3" set hz=120
if "%hz_choice%"=="4" set hz=144
if "%hz_choice%"=="5" set hz=165
if "%hz_choice%"=="6" set hz=240

echo.
echo Setting refresh rate to !hz! Hz...
start ms-settings:display-advancedgraphics
pause
goto menu

:set_scaling
cls
echo ================================================
echo Set Display Scaling
echo ================================================
echo.
echo [1] 100%% (Default)
echo [2] 125%%
echo [3] 150%%
echo [4] 175%%
echo [5] 200%%
echo.
set /p scale_choice="Select scaling (1-5): "

if "%scale_choice%"=="1" set scale=100
if "%scale_choice%"=="2" set scale=125
if "%scale_choice%"=="3" set scale=150
if "%scale_choice%"=="4" set scale=175
if "%scale_choice%"=="5" set scale=200

echo.
echo Setting display scaling to !scale!%%...
reg add "HKCU\Control Panel\Desktop" /v LogPixels /t REG_DWORD /d !scale! /f
reg add "HKCU\Control Panel\Desktop" /v Win8DpiScaling /t REG_DWORD /d 1 /f
echo Display scaling updated. Sign out and sign in for changes to take effect.
pause
goto menu

:toggle_night_light
cls
echo ================================================
echo Toggle Night Light
echo ================================================
echo.
powershell -Command "Get-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Current\default$windows.data.bluelightreduction.settings\windows.data.bluelightreduction.settings' -ErrorAction SilentlyContinue"
echo.
echo Opening Night Light settings...
start ms-settings:nightlight
pause
goto menu

:display_info
cls
echo ================================================
echo Display Information
echo ================================================
echo.
powershell -Command "Add-Type -AssemblyName System.Windows.Forms; $screens = [System.Windows.Forms.Screen]::AllScreens; foreach($screen in $screens) { Write-Host 'Device:' $screen.DeviceName; Write-Host 'Resolution:' $screen.Bounds.Width 'x' $screen.Bounds.Height; Write-Host 'Primary:' $screen.Primary; Write-Host '---' }"
echo.
pause
goto menu

:multiple_monitors
cls
echo ================================================
echo Multiple Monitor Settings
echo ================================================
echo.
echo [1] Extend displays
echo [2] Duplicate displays
echo [3] Show only on primary
echo [4] Show only on secondary
echo.
set /p mon_choice="Select option (1-4): "

echo.
echo Opening display settings...
start ms-settings:display
pause
goto menu
