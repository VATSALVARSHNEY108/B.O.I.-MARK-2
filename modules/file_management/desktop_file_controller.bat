@echo off
REM Desktop File Controller - Batch Automation
REM Controls desktop file operations and sync management

setlocal enabledelayedexpansion
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..\..\
set PYTHON_SCRIPT=%PROJECT_ROOT%modules\file_management\desktop_sync_manager.py

cls
echo.
echo ============================================================
echo   DESKTOP FILE CONTROLLER
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Run the desktop sync manager
echo [INFO] Starting Desktop Sync Manager...
cd /d "%PROJECT_ROOT%"
python "%PYTHON_SCRIPT%"

if errorlevel 1 (
    echo [ERROR] Failed to run Desktop Sync Manager
    echo Please check the Python environment and try again
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Desktop File Controller completed
echo.
pause
