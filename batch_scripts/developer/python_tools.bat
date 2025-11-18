@echo off
REM ==========================================
REM PYTHON DEVELOPER TOOLS
REM Quick Python utilities
REM ==========================================

color 0E
title Python Developer Tools

:menu
cls
echo ========================================
echo     PYTHON DEVELOPER TOOLS
echo ========================================
echo.
echo 1. Check Python Version
echo 2. Check pip Version
echo 3. List Installed Packages
echo 4. Install Package
echo 5. Uninstall Package
echo 6. Upgrade pip
echo 7. Create Virtual Environment
echo 8. Generate requirements.txt
echo 9. Install from requirements.txt
echo 10. Python Shell
echo 11. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto pyversion
if "%choice%"=="2" goto pipversion
if "%choice%"=="3" goto listpkg
if "%choice%"=="4" goto install
if "%choice%"=="5" goto uninstall
if "%choice%"=="6" goto upgradepip
if "%choice%"=="7" goto venv
if "%choice%"=="8" goto freeze
if "%choice%"=="9" goto installreq
if "%choice%"=="10" goto shell
if "%choice%"=="11" exit /b

goto menu

:pyversion
echo.
python --version
echo.
pause
goto menu

:pipversion
echo.
pip --version
echo.
pause
goto menu

:listpkg
echo.
echo Installed Packages:
pip list
echo.
pause
goto menu

:install
set /p package="Enter package name: "
pip install %package%
echo.
pause
goto menu

:uninstall
set /p package="Enter package name: "
pip uninstall %package% -y
echo.
pause
goto menu

:upgradepip
echo.
python -m pip install --upgrade pip
echo.
pause
goto menu

:venv
set /p venvname="Enter virtual environment name: "
python -m venv %venvname%
echo.
echo Virtual environment created!
echo To activate: %venvname%\Scripts\activate
pause
goto menu

:freeze
pip freeze > requirements.txt
echo.
echo requirements.txt generated!
pause
goto menu

:installreq
if exist requirements.txt (
    pip install -r requirements.txt
    echo.
    echo Packages installed from requirements.txt
) else (
    echo requirements.txt not found!
)
pause
goto menu

:shell
python
goto menu
