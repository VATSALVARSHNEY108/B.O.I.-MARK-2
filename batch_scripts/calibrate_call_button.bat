@echo off
REM Calibrate Phone Link Call Button Position
REM Finds the exact position of the Call button on your screen

echo ==================================
echo   PHONE LINK CALL BUTTON CALIBRATION
echo ==============================================
echo.
echo This tool will help you find the exact
echo position of the Call button so auto-
echo calling works perfectly!
echo.
pause

python scripts/calibrate_phone_link_button.py

pause
