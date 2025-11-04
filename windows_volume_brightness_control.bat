@echo off
REM ========================================
REM Windows Volume & Brightness Control
REM ========================================
REM This batch file uses nircmd.exe to control system volume and brightness
REM Download nircmd.exe from: https://www.nirsoft.net/utils/nircmd.html
REM Place nircmd.exe in the same folder as this batch file or in your PATH

setlocal enabledelayedexpansion

:MENU
cls
echo ========================================
echo   VOLUME ^& BRIGHTNESS CONTROL
echo ========================================
echo.
echo VOLUME CONTROLS:
echo   1 - Set Volume to 0%% (Mute)
echo   2 - Set Volume to 25%%
echo   3 - Set Volume to 50%%
echo   4 - Set Volume to 75%%
echo   5 - Set Volume to 100%%
echo   6 - Increase Volume by 10%%
echo   7 - Decrease Volume by 10%%
echo   8 - Toggle Mute
echo   9 - Get Current Volume
echo.
echo BRIGHTNESS CONTROLS:
echo   A - Set Brightness to 25%%
echo   B - Set Brightness to 50%%
echo   C - Set Brightness to 75%%
echo   D - Set Brightness to 100%%
echo.
echo CUSTOM:
echo   V - Custom Volume Level
echo   W - Custom Brightness Level
echo.
echo   Q - Quit
echo.
echo ========================================
set /p choice="Enter your choice: "

if /i "%choice%"=="1" goto VOL0
if /i "%choice%"=="2" goto VOL25
if /i "%choice%"=="3" goto VOL50
if /i "%choice%"=="4" goto VOL75
if /i "%choice%"=="5" goto VOL100
if /i "%choice%"=="6" goto VOLUP
if /i "%choice%"=="7" goto VOLDOWN
if /i "%choice%"=="8" goto VOLTOGGLE
if /i "%choice%"=="9" goto VOLGET
if /i "%choice%"=="A" goto BRIGHT25
if /i "%choice%"=="B" goto BRIGHT50
if /i "%choice%"=="C" goto BRIGHT75
if /i "%choice%"=="D" goto BRIGHT100
if /i "%choice%"=="V" goto VOLCUSTOM
if /i "%choice%"=="W" goto BRIGHTCUSTOM
if /i "%choice%"=="Q" goto END
goto MENU

:VOL0
echo Setting volume to 0%% (Mute)...
nircmd.exe setsysvolume 0
echo Done!
timeout /t 2 >nul
goto MENU

:VOL25
echo Setting volume to 25%%...
nircmd.exe setsysvolume 16384
echo Done!
timeout /t 2 >nul
goto MENU

:VOL50
echo Setting volume to 50%%...
nircmd.exe setsysvolume 32768
echo Done!
timeout /t 2 >nul
goto MENU

:VOL75
echo Setting volume to 75%%...
nircmd.exe setsysvolume 49152
echo Done!
timeout /t 2 >nul
goto MENU

:VOL100
echo Setting volume to 100%%...
nircmd.exe setsysvolume 65535
echo Done!
timeout /t 2 >nul
goto MENU

:VOLUP
echo Increasing volume by 10%%...
nircmd.exe changesysvolume 6554
echo Done!
timeout /t 2 >nul
goto MENU

:VOLDOWN
echo Decreasing volume by 10%%...
nircmd.exe changesysvolume -6554
echo Done!
timeout /t 2 >nul
goto MENU

:VOLTOGGLE
echo Toggling mute...
nircmd.exe mutesysvolume 2
echo Done!
timeout /t 2 >nul
goto MENU

:VOLGET
echo Getting current volume level...
for /f "delims=" %%i in ('nircmd.exe getsysvolume') do set volraw=%%i
set /a volpercent=!volraw! / 655
echo Current Volume: !volpercent!%%
echo.
pause
goto MENU

:BRIGHT25
echo Setting brightness to 25%%...
powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,25)
echo Done!
timeout /t 2 >nul
goto MENU

:BRIGHT50
echo Setting brightness to 50%%...
powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,50)
echo Done!
timeout /t 2 >nul
goto MENU

:BRIGHT75
echo Setting brightness to 75%%...
powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,75)
echo Done!
timeout /t 2 >nul
goto MENU

:BRIGHT100
echo Setting brightness to 100%%...
powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,100)
echo Done!
timeout /t 2 >nul
goto MENU

:VOLCUSTOM
echo.
set /p customvol="Enter volume level (0-100): "
if !customvol! LSS 0 set customvol=0
if !customvol! GTR 100 set customvol=100
set /a volvalue=!customvol! * 655
echo Setting volume to !customvol!%%...
nircmd.exe setsysvolume !volvalue!
echo Done!
timeout /t 2 >nul
goto MENU

:BRIGHTCUSTOM
echo.
set /p custombright="Enter brightness level (0-100): "
if !custombright! LSS 0 set custombright=0
if !custombright! GTR 100 set custombright=100
echo Setting brightness to !custombright!%%...
powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,!custombright!)
echo Done!
timeout /t 2 >nul
goto MENU

:END
echo.
echo Thank you for using Volume ^& Brightness Control!
echo.
timeout /t 2 >nul
exit /b
