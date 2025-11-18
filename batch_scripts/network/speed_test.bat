@echo off
REM ==========================================
REM Network Speed & Diagnostics
REM Test network speed and connectivity
REM ==========================================

title Network Speed Test

:menu
cls
echo ========================================
echo    NETWORK SPEED & DIAGNOSTICS
echo ========================================
echo.
echo 1. Ping Test (Google)
echo 2. Ping Test (Custom)
echo 3. Trace Route
echo 4. DNS Lookup
echo 5. Network Adapter Info
echo 6. Flush DNS Cache
echo 7. Reset Network
echo 8. Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto ping_google
if "%choice%"=="2" goto ping_custom
if "%choice%"=="3" goto traceroute
if "%choice%"=="4" goto nslookup
if "%choice%"=="5" goto adapter
if "%choice%"=="6" goto flush
if "%choice%"=="7" goto reset
if "%choice%"=="8" exit
goto menu

:ping_google
cls
echo Pinging Google (8.8.8.8)...
echo.
ping 8.8.8.8 -n 10
echo.
pause
goto menu

:ping_custom
cls
set /p host="Enter host to ping (IP or domain): "
echo.
ping %host% -n 10
echo.
pause
goto menu

:traceroute
cls
set /p host="Enter host to trace: "
echo.
tracert %host%
echo.
pause
goto menu

:nslookup
cls
set /p domain="Enter domain for DNS lookup: "
echo.
nslookup %domain%
echo.
pause
goto menu

:adapter
cls
echo Network Adapter Information:
echo.
ipconfig /all
echo.
pause
goto menu

:flush
echo Flushing DNS cache...
ipconfig /flushdns
echo DNS cache flushed!
timeout /t 2 >nul
goto menu

:reset
echo Resetting network adapters...
echo This will reset all network adapters and settings
echo.
pause
netsh winsock reset
netsh int ip reset
ipconfig /release
ipconfig /renew
ipconfig /flushdns
echo.
echo Network reset complete! Restart your computer for changes to take effect.
pause
goto menu
