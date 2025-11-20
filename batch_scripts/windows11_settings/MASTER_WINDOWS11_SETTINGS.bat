@echo off
setlocal EnableDelayedExpansion
color 0A

:: ================================================
:: MASTER Windows 11 Settings Controller
:: Complete Automation Suite for Windows 11
:: ================================================

:main_menu
cls
echo.
echo ========================================================
echo        MASTER WINDOWS 11 SETTINGS CONTROLLER
echo ========================================================
echo.
echo                  SYSTEM SETTINGS
echo --------------------------------------------------------
echo  [1]  Display Settings         (Resolution, Orientation, Refresh Rate)
echo  [2]  Sound Settings           (Volume, Spatial Audio, Devices)
echo  [3]  Network Settings         (WiFi, Airplane Mode, DNS, Proxy)
echo  [4]  Bluetooth Settings       (Pair/Unpair, On/Off)
echo.
echo                PRIVACY ^& SECURITY
echo --------------------------------------------------------
echo  [5]  Privacy ^& Security       (Camera, Mic, Location, Defender)
echo  [6]  Windows Update           (Check, Install, Pause Updates)
echo.
echo              PERSONALIZATION
echo --------------------------------------------------------
echo  [7]  Personalization          (Dark Mode, Themes, Wallpaper)
echo  [8]  System Settings          (Notifications, Clipboard, Storage)
echo.
echo               ACCESSIBILITY
echo --------------------------------------------------------
echo  [9]  Accessibility            (Narrator, Magnifier, High Contrast)
echo.
echo --------------------------------------------------------
echo  [10] Open ALL Settings        (Windows Settings App)
echo  [0]  Exit
echo ========================================================
echo.
set /p choice="Select an option (0-10): "

if "%choice%"=="1" call "%~dp0display_settings.bat"
if "%choice%"=="2" call "%~dp0sound_settings.bat"
if "%choice%"=="3" call "%~dp0network_settings.bat"
if "%choice%"=="4" call "%~dp0bluetooth.bat"
if "%choice%"=="5" call "%~dp0privacy_security.bat"
if "%choice%"=="6" call "%~dp0windows_update.bat"
if "%choice%"=="7" call "%~dp0personalization.bat"
if "%choice%"=="8" call "%~dp0system_settings.bat"
if "%choice%"=="9" call "%~dp0accessibility.bat"
if "%choice%"=="10" goto all_settings
if "%choice%"=="0" goto exit_program

goto main_menu

:all_settings
cls
echo.
echo Opening Windows 11 Settings...
start ms-settings:
timeout /t 2 /nobreak >nul
goto main_menu

:exit_program
cls
echo.
echo ========================================================
echo   Thank you for using Windows 11 Settings Controller!
echo ========================================================
echo.
timeout /t 2 /nobreak >nul
exit /b
