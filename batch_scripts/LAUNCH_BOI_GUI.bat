@echo off
REM BOI GUI Launcher - Desktop Application
REM Launches the main GUI application

cd /d "%~dp0\.."
python3 scripts/main.py %*
