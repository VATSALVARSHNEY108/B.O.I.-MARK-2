@echo off
REM Quick Call Test with Calibrated Position
REM Uses exact coordinates: X=1670, Y=893

echo ========================================
echo   PHONE LINK - QUICK CALL TEST
echo ========================================
echo.
echo Using calibrated call button position:
echo    X = 1670
echo    Y = 893
echo.
echo Make sure Phone Link is connected!
echo.
pause

python tests/test_exact_call.py

pause
