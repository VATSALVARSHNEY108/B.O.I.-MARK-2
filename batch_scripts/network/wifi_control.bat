@echo off
REM ==========================================
REM WiFi Control
REM Manage WiFi connections
REM ==========================================

title WiFi Control

:menu
cls
echo ========================================
echo          WIFI CONTROL
echo ========================================
echo.
echo 1. Show Available Networks
echo 2. Show Current Connection
echo 3. Disconnect WiFi
echo 4. Connect to Network
echo 5. Show Saved Networks
echo 6. Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto show
if "%choice%"=="2" goto current
if "%choice%"=="3" goto disconnect
if "%choice%"=="4" goto connect
if "%choice%"=="5" goto saved
if "%choice%"=="6" exit
goto menu

:show
cls
echo Available WiFi Networks:
echo.
netsh wlan show networks
echo.
pause
goto menu

:current
cls
echo Current WiFi Connection:
echo.
netsh wlan show interfaces
echo.
pause
goto menu

:disconnect
echo Disconnecting WiFi...
netsh wlan disconnect
echo WiFi disconnected
timeout /t 2 >nul
goto menu

:connect
cls
echo Saved WiFi Networks:
netsh wlan show profiles
echo.
set /p ssid="Enter network name to connect: "
netsh wlan connect name="%ssid%"
echo Connecting to %ssid%...
timeout /t 3 >nul
goto menu

:saved
cls
echo Saved WiFi Networks:
echo.
netsh wlan show profiles
echo.
pause
goto menu
