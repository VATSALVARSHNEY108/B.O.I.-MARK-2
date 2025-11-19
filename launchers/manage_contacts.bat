@echo off
REM Contact Manager Launcher
REM Add, edit, delete, and manage your contacts

title Contact Manager
color 0C

echo.
echo ========================================
echo  CONTACT MANAGER
echo ========================================
echo.
echo Manage your phone contacts here
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from python.org
    pause
    exit /b 1
)

REM Run the contact manager
python manage_contacts.py

REM Keep window open if there was an error
if %errorlevel% neq 0 (
    echo.
    echo ERROR: The program encountered an error
    pause
)
