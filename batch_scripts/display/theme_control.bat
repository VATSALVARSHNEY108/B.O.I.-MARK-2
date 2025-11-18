@echo off
REM ==========================================
REM THEME CONTROL
REM Switch between Dark/Light themes
REM ==========================================

color 0B
title Theme Control

:menu
cls
echo ========================================
echo         THEME CONTROL
echo ========================================
echo.
echo 1. Dark Mode
echo 2. Light Mode
echo 3. Dark Apps, Light System
echo 4. Light Apps, Dark System
echo 5. Open Personalization Settings
echo 6. Open Color Settings
echo 7. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto dark
if "%choice%"=="2" goto light
if "%choice%"=="3" goto darkapps
if "%choice%"=="4" goto lightapps
if "%choice%"=="5" start ms-settings:personalization & goto menu
if "%choice%"=="6" start ms-settings:colors & goto menu
if "%choice%"=="7" exit /b

goto menu

:dark
echo Switching to Dark Mode...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 0 /f >nul
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v SystemUsesLightTheme /t REG_DWORD /d 0 /f >nul
echo Dark Mode activated!
timeout /t 2 >nul
goto menu

:light
echo Switching to Light Mode...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v SystemUsesLightTheme /t REG_DWORD /d 1 /f >nul
echo Light Mode activated!
timeout /t 2 >nul
goto menu

:darkapps
echo Setting Dark Apps with Light System...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 0 /f >nul
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v SystemUsesLightTheme /t REG_DWORD /d 1 /f >nul
echo Theme applied!
timeout /t 2 >nul
goto menu

:lightapps
echo Setting Light Apps with Dark System...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v SystemUsesLightTheme /t REG_DWORD /d 0 /f >nul
echo Theme applied!
timeout /t 2 >nul
goto menu
