@echo off
REM Quick Test for Phone Link Auto-Call Fix
REM Tests the new auto-call functionality

echo ========================================
echo   PHONE LINK AUTO-CALL FIX TEST
echo ========================================
echo.
echo This script tests the fixed Phone Link
echo auto-call functionality.
echo.
echo Make sure:
echo  1. Phone Link is connected
echo  2. Keep Phone Link window visible
echo  3. Call should start automatically!
echo.
pause

python tests/test_phone_link_fix.py

pause
