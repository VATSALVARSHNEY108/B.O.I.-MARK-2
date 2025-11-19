@echo off
REM Quick Dial - Call a number with one click
REM Edit the PHONE_NUMBER variable below to set your default number

title Quick Dial
color 0B

REM SET YOUR PHONE NUMBER HERE
set PHONE_NUMBER=+1234567890

echo.
echo ========================================
echo  QUICK DIAL - PHONE LINK
echo ========================================
echo.
echo Dialing: %PHONE_NUMBER%
echo.

REM Run quick dial command
python -c "from modules.communication.phone_dialer import create_phone_dialer; dialer = create_phone_dialer(); result = dialer.dial_with_phone_link('%PHONE_NUMBER%'); print(result['message'])"

echo.
echo Done!
timeout /t 3 >nul
