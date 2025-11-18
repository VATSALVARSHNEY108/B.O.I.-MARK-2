@echo off
REM ==========================================
REM NODE.JS DEVELOPER TOOLS
REM Quick Node.js utilities
REM ==========================================

color 0E
title Node.js Developer Tools

:menu
cls
echo ========================================
echo    NODE.JS DEVELOPER TOOLS
echo ========================================
echo.
echo 1. Check Node Version
echo 2. Check npm Version
echo 3. Initialize npm Project
echo 4. Install Package
echo 5. Install Package (Dev)
echo 6. Uninstall Package
echo 7. List Installed Packages
echo 8. Update All Packages
echo 9. Clear npm Cache
echo 10. Run npm Audit
echo 11. Fix Vulnerabilities
echo 12. Start Project (npm start)
echo 13. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto nodeversion
if "%choice%"=="2" goto npmversion
if "%choice%"=="3" goto init
if "%choice%"=="4" goto install
if "%choice%"=="5" goto installdev
if "%choice%"=="6" goto uninstall
if "%choice%"=="7" goto list
if "%choice%"=="8" goto update
if "%choice%"=="9" goto clearcache
if "%choice%"=="10" goto audit
if "%choice%"=="11" goto fix
if "%choice%"=="12" goto start
if "%choice%"=="13" exit /b

goto menu

:nodeversion
echo.
node --version
echo.
pause
goto menu

:npmversion
echo.
npm --version
echo.
pause
goto menu

:init
echo.
npm init -y
echo.
echo package.json created!
pause
goto menu

:install
set /p package="Enter package name: "
npm install %package%
echo.
pause
goto menu

:installdev
set /p package="Enter package name: "
npm install %package% --save-dev
echo.
pause
goto menu

:uninstall
set /p package="Enter package name: "
npm uninstall %package%
echo.
pause
goto menu

:list
echo.
npm list --depth=0
echo.
pause
goto menu

:update
echo.
npm update
echo.
pause
goto menu

:clearcache
echo.
npm cache clean --force
echo.
echo npm cache cleared!
pause
goto menu

:audit
echo.
npm audit
echo.
pause
goto menu

:fix
echo.
npm audit fix
echo.
pause
goto menu

:start
npm start
pause
goto menu
