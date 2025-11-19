@echo off
REM AI Phone Link Controller Launcher
REM This batch file launches the AI-powered Phone Link controller

title AI Phone Link Controller
color 0A

echo.
echo ========================================
echo  AI PHONE LINK CONTROLLER
echo ========================================
echo.
echo Starting AI-powered phone control...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from python.org
    pause
    exit /b 1
)

REM Run the AI Phone Link Controller
python ai_phone_link_controller.py

REM Keep window open if there was an error
if %errorlevel% neq 0 (
    echo.
    echo ERROR: The program encountered an error
    pause
)
