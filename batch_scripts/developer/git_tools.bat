@echo off
REM ==========================================
REM GIT TOOLS
REM Quick Git commands and shortcuts
REM ==========================================

color 0E
title Git Tools

:menu
cls
echo ========================================
echo          GIT TOOLS
echo ========================================
echo.
echo 1. Git Status
echo 2. Git Log (Recent)
echo 3. Quick Commit
echo 4. Push to Remote
echo 5. Pull from Remote
echo 6. Create Branch
echo 7. Switch Branch
echo 8. View Branches
echo 9. Clone Repository
echo 10. Initialize Repository
echo 11. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto status
if "%choice%"=="2" goto log
if "%choice%"=="3" goto commit
if "%choice%"=="4" goto push
if "%choice%"=="5" goto pull
if "%choice%"=="6" goto createbranch
if "%choice%"=="7" goto switchbranch
if "%choice%"=="8" goto branches
if "%choice%"=="9" goto clone
if "%choice%"=="10" goto init
if "%choice%"=="11" exit /b

goto menu

:status
echo.
git status
echo.
pause
goto menu

:log
echo.
echo Recent Git Log:
git log --oneline -10
echo.
pause
goto menu

:commit
echo.
set /p message="Enter commit message: "
git add .
git commit -m "%message%"
echo.
echo Changes committed!
pause
goto menu

:push
echo.
set /p branch="Enter branch name (or leave blank for current): "
if "%branch%"=="" (
    git push
) else (
    git push origin %branch%
)
echo.
pause
goto menu

:pull
echo.
git pull
echo.
pause
goto menu

:createbranch
set /p branchname="Enter new branch name: "
git branch %branchname%
echo.
echo Branch '%branchname%' created!
pause
goto menu

:switchbranch
set /p branchname="Enter branch name: "
git checkout %branchname%
echo.
pause
goto menu

:branches
echo.
echo All Branches:
git branch -a
echo.
pause
goto menu

:clone
set /p repourl="Enter repository URL: "
set /p dirname="Enter directory name (optional): "
if "%dirname%"=="" (
    git clone %repourl%
) else (
    git clone %repourl% %dirname%
)
echo.
pause
goto menu

:init
echo.
git init
echo Repository initialized!
pause
goto menu
