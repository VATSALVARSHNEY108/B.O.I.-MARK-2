@echo off
setlocal EnableDelayedExpansion

:: ================================================
:: Windows 11 Network Settings Automation
:: ================================================

:menu
cls
echo ================================================
echo   Windows 11 Network Settings Controller
echo ================================================
echo.
echo [1] WiFi On/Off
echo [2] Airplane Mode On/Off
echo [3] View Network Info
echo [4] Network Adapter Settings
echo [5] Proxy Settings
echo [6] DNS Settings
echo [7] Reset Network
echo [8] VPN Settings
echo [9] Back to Main Menu
echo.
set /p choice="Select option (1-9): "

if "%choice%"=="1" goto wifi_toggle
if "%choice%"=="2" goto airplane_mode
if "%choice%"=="3" goto network_info
if "%choice%"=="4" goto adapter_settings
if "%choice%"=="5" goto proxy_settings
if "%choice%"=="6" goto dns_settings
if "%choice%"=="7" goto reset_network
if "%choice%"=="8" goto vpn_settings
if "%choice%"=="9" exit /b
goto menu

:wifi_toggle
cls
echo ================================================
echo WiFi Control
echo ================================================
echo.
echo [1] Turn WiFi ON
echo [2] Turn WiFi OFF
echo [3] Show WiFi Status
echo [4] List Available Networks
echo.
set /p wifi_choice="Select option (1-4): "

if "%wifi_choice%"=="1" (
    echo Turning WiFi ON...
    powershell -Command "Get-NetAdapter | Where-Object {$_.InterfaceDescription -like '*Wi-Fi*' -or $_.InterfaceDescription -like '*Wireless*'} | Enable-NetAdapter -Confirm:$false"
    echo WiFi enabled!
) else if "%wifi_choice%"=="2" (
    echo Turning WiFi OFF...
    powershell -Command "Get-NetAdapter | Where-Object {$_.InterfaceDescription -like '*Wi-Fi*' -or $_.InterfaceDescription -like '*Wireless*'} | Disable-NetAdapter -Confirm:$false"
    echo WiFi disabled!
) else if "%wifi_choice%"=="3" (
    echo.
    echo Current WiFi Status:
    powershell -Command "Get-NetAdapter | Where-Object {$_.InterfaceDescription -like '*Wi-Fi*' -or $_.InterfaceDescription -like '*Wireless*'} | Select-Object Name, Status, LinkSpeed | Format-Table -AutoSize"
    echo.
    echo Current Connection:
    netsh wlan show interfaces
) else if "%wifi_choice%"=="4" (
    echo.
    echo Scanning for networks...
    netsh wlan show networks mode=bssid
)
echo.
pause
goto menu

:airplane_mode
cls
echo ================================================
echo Airplane Mode Control
echo ================================================
echo.
echo [1] Enable Airplane Mode
echo [2] Disable Airplane Mode
echo.
set /p airplane_choice="Select option (1-2): "

if "%airplane_choice%"=="1" (
    echo Enabling Airplane Mode...
    reg add "HKLM\SYSTEM\CurrentControlSet\Control\RadioManagement\SystemRadioState" /v "(Default)" /t REG_DWORD /d 0 /f
    echo Airplane Mode enabled!
) else if "%airplane_choice%"=="2" (
    echo Disabling Airplane Mode...
    reg add "HKLM\SYSTEM\CurrentControlSet\Control\RadioManagement\SystemRadioState" /v "(Default)" /t REG_DWORD /d 1 /f
    echo Airplane Mode disabled!
)
echo.
pause
goto menu

:network_info
cls
echo ================================================
echo Network Information
echo ================================================
echo.
echo IP Configuration:
echo -----------------
ipconfig /all
echo.
echo.
echo Active Connections:
echo -------------------
netstat -an | findstr "ESTABLISHED"
echo.
pause
goto menu

:adapter_settings
cls
echo ================================================
echo Network Adapter Settings
echo ================================================
echo.
echo Opening Network Connections...
ncpa.cpl
pause
goto menu

:proxy_settings
cls
echo ================================================
echo Proxy Settings
echo ================================================
echo.
echo [1] Enable Proxy
echo [2] Disable Proxy
echo [3] View Current Proxy Settings
echo.
set /p proxy_choice="Select option (1-3): "

if "%proxy_choice%"=="1" (
    set /p proxy_server="Enter proxy server (IP:Port): "
    reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f
    reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d "!proxy_server!" /f
    echo Proxy enabled: !proxy_server!
) else if "%proxy_choice%"=="2" (
    reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f
    echo Proxy disabled!
) else if "%proxy_choice%"=="3" (
    echo.
    reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable
    reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer
)
echo.
pause
goto menu

:dns_settings
cls
echo ================================================
echo DNS Settings
echo ================================================
echo.
echo [1] Set Google DNS (8.8.8.8)
echo [2] Set Cloudflare DNS (1.1.1.1)
echo [3] Set OpenDNS (208.67.222.222)
echo [4] Set to Automatic (DHCP)
echo.
set /p dns_choice="Select option (1-4): "

if "%dns_choice%"=="1" (
    netsh interface ip set dns "Ethernet" static 8.8.8.8
    netsh interface ip add dns "Ethernet" 8.8.4.4 index=2
    echo Google DNS configured!
) else if "%dns_choice%"=="2" (
    netsh interface ip set dns "Ethernet" static 1.1.1.1
    netsh interface ip add dns "Ethernet" 1.0.0.1 index=2
    echo Cloudflare DNS configured!
) else if "%dns_choice%"=="3" (
    netsh interface ip set dns "Ethernet" static 208.67.222.222
    netsh interface ip add dns "Ethernet" 208.67.220.220 index=2
    echo OpenDNS configured!
) else if "%dns_choice%"=="4" (
    netsh interface ip set dns "Ethernet" dhcp
    echo DNS set to automatic!
)
echo.
pause
goto menu

:reset_network
cls
echo ================================================
echo Reset Network Settings
echo ================================================
echo.
echo WARNING: This will reset all network adapters
echo and require a system restart.
echo.
set /p confirm="Are you sure? (Y/N): "

if /i "%confirm%"=="Y" (
    echo.
    echo Resetting network settings...
    netsh winsock reset
    netsh int ip reset
    ipconfig /release
    ipconfig /renew
    ipconfig /flushdns
    echo.
    echo Network reset complete! Please restart your computer.
)
pause
goto menu

:vpn_settings
cls
echo ================================================
echo VPN Settings
echo ================================================
echo.
echo Opening VPN settings...
start ms-settings:network-vpn
pause
goto menu
