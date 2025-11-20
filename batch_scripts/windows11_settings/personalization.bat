@echo off
setlocal EnableDelayedExpansion

:: ================================================
:: Windows 11 Personalization Settings
:: ================================================

:menu
cls
echo ================================================
echo  Windows 11 Personalization Settings
echo ================================================
echo.
echo [1] Dark/Light Mode
echo [2] Accent Color
echo [3] Desktop Wallpaper
echo [4] Taskbar Settings
echo [5] Start Menu Settings
echo [6] Lock Screen
echo [7] Themes
echo [8] Back to Main Menu
echo.
set /p choice="Select option (1-8): "

if "%choice%"=="1" goto theme_mode
if "%choice%"=="2" goto accent_color
if "%choice%"=="3" goto wallpaper
if "%choice%"=="4" goto taskbar
if "%choice%"=="5" goto start_menu
if "%choice%"=="6" goto lock_screen
if "%choice%"=="7" goto themes
if "%choice%"=="8" exit /b
goto menu

:theme_mode
cls
echo ================================================
echo Dark/Light Mode Settings
echo ================================================
echo.
echo [1] Enable Dark Mode (System + Apps)
echo [2] Enable Light Mode (System + Apps)
echo [3] Dark System, Light Apps
echo [4] Light System, Dark Apps
echo.
set /p mode_choice="Select option (1-4): "

if "%mode_choice%"=="1" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v SystemUsesLightTheme /t REG_DWORD /d 0 /f
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 0 /f
    echo Dark mode enabled for system and apps!
) else if "%mode_choice%"=="2" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v SystemUsesLightTheme /t REG_DWORD /d 1 /f
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 1 /f
    echo Light mode enabled for system and apps!
) else if "%mode_choice%"=="3" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v SystemUsesLightTheme /t REG_DWORD /d 0 /f
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 1 /f
    echo Dark system, light apps enabled!
) else if "%mode_choice%"=="4" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v SystemUsesLightTheme /t REG_DWORD /d 1 /f
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 0 /f
    echo Light system, dark apps enabled!
)
pause
goto menu

:accent_color
cls
echo ================================================
echo Accent Color Settings
echo ================================================
echo.
echo [1] Enable Automatic Accent Color
echo [2] Show Accent Color on Start/Taskbar
echo [3] Hide Accent Color on Start/Taskbar
echo [4] Open Color Settings
echo.
set /p accent_choice="Select option (1-4): "

if "%accent_choice%"=="1" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v ColorPrevalence /t REG_DWORD /d 1 /f
    reg add "HKCU\SOFTWARE\Microsoft\Windows\DWM" /v ColorPrevalence /t REG_DWORD /d 1 /f
    echo Automatic accent color enabled!
) else if "%accent_choice%"=="2" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v ColorPrevalence /t REG_DWORD /d 1 /f
    echo Accent color shown on Start and Taskbar!
) else if "%accent_choice%"=="3" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v ColorPrevalence /t REG_DWORD /d 0 /f
    echo Accent color hidden from Start and Taskbar!
) else if "%accent_choice%"=="4" (
    start ms-settings:colors
)
pause
goto menu

:wallpaper
cls
echo ================================================
echo Desktop Wallpaper Settings
echo ================================================
echo.
echo [1] Set Solid Color Background
echo [2] Browse for Wallpaper
echo [3] Open Personalization
echo.
set /p wall_choice="Select option (1-3): "

if "%wall_choice%"=="1" (
    set /p color="Enter color (black/white/blue/red/green): "
    reg add "HKCU\Control Panel\Colors" /v Background /t REG_SZ /d "0 0 0" /f
    echo Solid color background set!
) else if "%wall_choice%"=="2" (
    start ms-settings:personalization-background
) else if "%wall_choice%"=="3" (
    start ms-settings:personalization
)
pause
goto menu

:taskbar
cls
echo ================================================
echo Taskbar Settings
echo ================================================
echo.
echo [1] Auto-hide Taskbar ON
echo [2] Auto-hide Taskbar OFF
echo [3] Taskbar Alignment - Center
echo [4] Taskbar Alignment - Left
echo [5] Show/Hide Task View Button
echo [6] Show/Hide Widgets Button
echo [7] Open Taskbar Settings
echo.
set /p task_choice="Select option (1-7): "

if "%task_choice%"=="1" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3" /v Settings /t REG_BINARY /d 30000000feffffff7af400000300000033000000300000000000000000000000080700008004000078040000 /f
    echo Auto-hide taskbar enabled! (Restart Explorer)
) else if "%task_choice%"=="2" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3" /v Settings /t REG_BINARY /d 30000000feffffff7af400000300000033000000300000000000000000000000080700008004000078040000 /f
    echo Auto-hide taskbar disabled! (Restart Explorer)
) else if "%task_choice%"=="3" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v TaskbarAl /t REG_DWORD /d 1 /f
    taskkill /f /im explorer.exe & start explorer.exe
    echo Taskbar aligned to center!
) else if "%task_choice%"=="4" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v TaskbarAl /t REG_DWORD /d 0 /f
    taskkill /f /im explorer.exe & start explorer.exe
    echo Taskbar aligned to left!
) else if "%task_choice%"=="5" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v ShowTaskViewButton /t REG_DWORD /d 0 /f
    taskkill /f /im explorer.exe & start explorer.exe
    echo Task View button toggled!
) else if "%task_choice%"=="6" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v TaskbarDa /t REG_DWORD /d 0 /f
    taskkill /f /im explorer.exe & start explorer.exe
    echo Widgets button toggled!
) else if "%task_choice%"=="7" (
    start ms-settings:taskbar
)
pause
goto menu

:start_menu
cls
echo ================================================
echo Start Menu Settings
echo ================================================
echo.
echo [1] Show More Pins
echo [2] Show More Recommendations
echo [3] Show Recently Added Apps
echo [4] Open Start Settings
echo.
set /p start_choice="Select option (1-4): "

if "%start_choice%"=="1" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v Start_Layout /t REG_DWORD /d 1 /f
    echo Start menu set to show more pins!
) else if "%start_choice%"=="2" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v Start_Layout /t REG_DWORD /d 0 /f
    echo Start menu set to show more recommendations!
) else if "%start_choice%"=="3" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v Start_TrackProgs /t REG_DWORD /d 1 /f
    echo Recently added apps will be shown!
) else if "%start_choice%"=="4" (
    start ms-settings:personalization-start
)
pause
goto menu

:lock_screen
cls
echo ================================================
echo Lock Screen Settings
echo ================================================
echo.
echo Opening lock screen settings...
start ms-settings:lockscreen
pause
goto menu

:themes
cls
echo ================================================
echo Themes
echo ================================================
echo.
echo Opening themes settings...
start ms-settings:themes
pause
goto menu
