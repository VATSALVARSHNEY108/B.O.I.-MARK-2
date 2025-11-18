@echo off
REM ==========================================
REM Browser Cache Cleaner
REM Clear cache for all major browsers
REM ==========================================

title Browser Cache Cleaner

echo ========================================
echo      BROWSER CACHE CLEANER
echo ========================================
echo.
echo This will clear cache for:
echo - Google Chrome
echo - Microsoft Edge
echo - Firefox
echo - Opera
echo - Brave
echo.
echo WARNING: Close all browsers before continuing!
echo.
pause

echo.
echo Cleaning browser caches...
echo.

REM Chrome
echo [1/5] Cleaning Chrome cache...
taskkill /F /IM chrome.exe >nul 2>&1
rd /s /q "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache" >nul 2>&1
rd /s /q "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Code Cache" >nul 2>&1
rd /s /q "%LOCALAPPDATA%\Google\Chrome\User Data\Default\GPUCache" >nul 2>&1

REM Edge
echo [2/5] Cleaning Edge cache...
taskkill /F /IM msedge.exe >nul 2>&1
rd /s /q "%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache" >nul 2>&1
rd /s /q "%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Code Cache" >nul 2>&1

REM Firefox
echo [3/5] Cleaning Firefox cache...
taskkill /F /IM firefox.exe >nul 2>&1
for /d %%x in ("%APPDATA%\Mozilla\Firefox\Profiles\*") do (
    rd /s /q "%%x\cache2" >nul 2>&1
)

REM Opera
echo [4/5] Cleaning Opera cache...
taskkill /F /IM opera.exe >nul 2>&1
rd /s /q "%APPDATA%\Opera Software\Opera Stable\Cache" >nul 2>&1

REM Brave
echo [5/5] Cleaning Brave cache...
taskkill /F /IM brave.exe >nul 2>&1
rd /s /q "%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Cache" >nul 2>&1

echo.
echo ========================================
echo Browser caches cleared!
echo ========================================
pause
