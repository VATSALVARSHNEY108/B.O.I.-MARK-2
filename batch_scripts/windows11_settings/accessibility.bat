@echo off
setlocal EnableDelayedExpansion

:: ================================================
:: Windows 11 Accessibility Settings
:: ================================================

:menu
cls
echo ================================================
echo  Windows 11 Accessibility Settings
echo ================================================
echo.
echo [1] Narrator
echo [2] Magnifier
echo [3] High Contrast
echo [4] Keyboard Shortcuts
echo [5] Mouse Settings
echo [6] Text Size
echo [7] Color Filters
echo [8] Open Accessibility Settings
echo [9] Back to Main Menu
echo.
set /p choice="Select option (1-9): "

if "%choice%"=="1" goto narrator
if "%choice%"=="2" goto magnifier
if "%choice%"=="3" goto high_contrast
if "%choice%"=="4" goto keyboard
if "%choice%"=="5" goto mouse
if "%choice%"=="6" goto text_size
if "%choice%"=="7" goto color_filters
if "%choice%"=="8" goto accessibility_settings
if "%choice%"=="9" exit /b
goto menu

:narrator
cls
echo ================================================
echo Narrator Settings
echo ================================================
echo.
echo [1] Start Narrator
echo [2] Stop Narrator
echo [3] Narrator Settings
echo.
set /p narr_choice="Select option (1-3): "

if "%narr_choice%"=="1" (
    start narrator.exe
    echo Narrator started!
) else if "%narr_choice%"=="2" (
    taskkill /f /im narrator.exe
    echo Narrator stopped!
) else if "%narr_choice%"=="3" (
    start ms-settings:easeofaccess-narrator
)
pause
goto menu

:magnifier
cls
echo ================================================
echo Magnifier Settings
echo ================================================
echo.
echo [1] Start Magnifier
echo [2] Stop Magnifier
echo [3] Magnifier Settings
echo.
set /p mag_choice="Select option (1-3): "

if "%mag_choice%"=="1" (
    start magnify.exe
    echo Magnifier started!
) else if "%mag_choice%"=="2" (
    taskkill /f /im magnify.exe
    echo Magnifier stopped!
) else if "%mag_choice%"=="3" (
    start ms-settings:easeofaccess-magnifier
)
pause
goto menu

:high_contrast
cls
echo ================================================
echo High Contrast Settings
echo ================================================
echo.
echo [1] Enable High Contrast (Aquatic)
echo [2] Enable High Contrast (Desert)
echo [3] Enable High Contrast (Dusk)
echo [4] Enable High Contrast (Night Sky)
echo [5] Disable High Contrast
echo [6] Open High Contrast Settings
echo.
set /p hc_choice="Select option (1-6): "

if "%hc_choice%"=="1" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes" /v CurrentTheme /t REG_SZ /d "%SystemRoot%\resources\Ease of Access Themes\hcwhite.theme" /f
    echo High Contrast Aquatic enabled!
) else if "%hc_choice%"=="2" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes" /v CurrentTheme /t REG_SZ /d "%SystemRoot%\resources\Ease of Access Themes\hc1.theme" /f
    echo High Contrast Desert enabled!
) else if "%hc_choice%"=="3" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes" /v CurrentTheme /t REG_SZ /d "%SystemRoot%\resources\Ease of Access Themes\hc2.theme" /f
    echo High Contrast Dusk enabled!
) else if "%hc_choice%"=="4" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes" /v CurrentTheme /t REG_SZ /d "%SystemRoot%\resources\Ease of Access Themes\hcblack.theme" /f
    echo High Contrast Night Sky enabled!
) else if "%hc_choice%"=="5" (
    reg add "HKCU\Control Panel\Accessibility\HighContrast" /v "Flags" /t REG_SZ /d "4194" /f
    echo High Contrast disabled!
) else if "%hc_choice%"=="6" (
    start ms-settings:easeofaccess-highcontrast
)
pause
goto menu

:keyboard
cls
echo ================================================
echo Keyboard Accessibility Settings
echo ================================================
echo.
echo [1] Enable Sticky Keys
echo [2] Disable Sticky Keys
echo [3] Enable Filter Keys
echo [4] Disable Filter Keys
echo [5] Enable Toggle Keys
echo [6] Disable Toggle Keys
echo [7] Open Keyboard Settings
echo.
set /p kb_choice="Select option (1-7): "

if "%kb_choice%"=="1" (
    reg add "HKCU\Control Panel\Accessibility\StickyKeys" /v "Flags" /t REG_SZ /d "510" /f
    echo Sticky Keys enabled!
) else if "%kb_choice%"=="2" (
    reg add "HKCU\Control Panel\Accessibility\StickyKeys" /v "Flags" /t REG_SZ /d "506" /f
    echo Sticky Keys disabled!
) else if "%kb_choice%"=="3" (
    reg add "HKCU\Control Panel\Accessibility\Keyboard Response" /v "Flags" /t REG_SZ /d "126" /f
    echo Filter Keys enabled!
) else if "%kb_choice%"=="4" (
    reg add "HKCU\Control Panel\Accessibility\Keyboard Response" /v "Flags" /t REG_SZ /d "122" /f
    echo Filter Keys disabled!
) else if "%kb_choice%"=="5" (
    reg add "HKCU\Control Panel\Accessibility\ToggleKeys" /v "Flags" /t REG_SZ /d "62" /f
    echo Toggle Keys enabled!
) else if "%kb_choice%"=="6" (
    reg add "HKCU\Control Panel\Accessibility\ToggleKeys" /v "Flags" /t REG_SZ /d "58" /f
    echo Toggle Keys disabled!
) else if "%kb_choice%"=="7" (
    start ms-settings:easeofaccess-keyboard
)
pause
goto menu

:mouse
cls
echo ================================================
echo Mouse Accessibility Settings
echo ================================================
echo.
echo [1] Enable Mouse Keys
echo [2] Disable Mouse Keys
echo [3] Change Mouse Pointer Size
echo [4] Open Mouse Settings
echo.
set /p mouse_choice="Select option (1-4): "

if "%mouse_choice%"=="1" (
    reg add "HKCU\Control Panel\Accessibility\MouseKeys" /v "Flags" /t REG_SZ /d "62" /f
    echo Mouse Keys enabled!
) else if "%mouse_choice%"=="2" (
    reg add "HKCU\Control Panel\Accessibility\MouseKeys" /v "Flags" /t REG_SZ /d "58" /f
    echo Mouse Keys disabled!
) else if "%mouse_choice%"=="3" (
    start ms-settings:easeofaccess-mouse
) else if "%mouse_choice%"=="4" (
    start ms-settings:easeofaccess-mouse
)
pause
goto menu

:text_size
cls
echo ================================================
echo Text Size Settings
echo ================================================
echo.
echo [1] Set Text Size to 100%% (Default)
echo [2] Set Text Size to 125%%
echo [3] Set Text Size to 150%%
echo [4] Set Text Size to 175%%
echo [5] Set Text Size to 200%%
echo.
set /p text_choice="Select option (1-5): "

if "%text_choice%"=="1" set size=100
if "%text_choice%"=="2" set size=125
if "%text_choice%"=="3" set size=150
if "%text_choice%"=="4" set size=175
if "%text_choice%"=="5" set size=200

echo.
echo Setting text size to !size!%%...
reg add "HKCU\SOFTWARE\Microsoft\Accessibility" /v TextScaleFactor /t REG_DWORD /d !size! /f
echo Text size updated to !size!%%!
pause
goto menu

:color_filters
cls
echo ================================================
echo Color Filters
echo ================================================
echo.
echo [1] Enable Grayscale
echo [2] Enable Inverted
echo [3] Enable Deuteranopia (Red-Green)
echo [4] Enable Protanopia (Red-Green)
echo [5] Enable Tritanopia (Blue-Yellow)
echo [6] Disable Color Filters
echo.
set /p color_choice="Select option (1-6): "

if "%color_choice%"=="1" (
    reg add "HKCU\SOFTWARE\Microsoft\ColorFiltering" /v Active /t REG_DWORD /d 1 /f
    reg add "HKCU\SOFTWARE\Microsoft\ColorFiltering" /v FilterType /t REG_DWORD /d 0 /f
    echo Grayscale color filter enabled!
) else if "%color_choice%"=="2" (
    reg add "HKCU\SOFTWARE\Microsoft\ColorFiltering" /v Active /t REG_DWORD /d 1 /f
    reg add "HKCU\SOFTWARE\Microsoft\ColorFiltering" /v FilterType /t REG_DWORD /d 4 /f
    echo Inverted color filter enabled!
) else if "%color_choice%"=="6" (
    reg add "HKCU\SOFTWARE\Microsoft\ColorFiltering" /v Active /t REG_DWORD /d 0 /f
    echo Color filters disabled!
)
pause
goto menu

:accessibility_settings
cls
echo ================================================
echo Accessibility Settings
echo ================================================
echo.
echo Opening accessibility settings...
start ms-settings:easeofaccess
pause
goto menu
