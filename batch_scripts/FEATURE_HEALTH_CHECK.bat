@echo off
REM BOI Feature Health Check - Tests all features individually
REM This script ensures all 410+ features work independently

setlocal enabledelayedexpansion
cd /d "%~dp0\.."

echo ================================================================================
echo                    BOI FEATURE HEALTH CHECK
echo ================================================================================
echo.

python3 scripts/test_individual_features.py

echo.
echo ================================================================================
echo Test complete. Check results above.
echo ================================================================================
pause
